import requests
import time
import psutil
import threading
import sys
import os
import json
import matplotlib.pyplot as plt
import subprocess
import numpy as np

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from partA import util

BASE_URL = 'http://localhost:4567'
JAVA_PATH = r"C:\Users\alect\.jdks\openjdk-23\bin\java.exe"
JAR_PATH = r"C:\Users\alect\dev\ECSE-429\software-validation-project-ecse-429\partB\runTodoManagerRestAPI-1.5.5.jar"

def start_server():
    print("Starting backend server...")

    jvm_args = [JAVA_PATH, "-Xmx6g", "-jar", JAR_PATH]
    process = subprocess.Popen(jvm_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        response = requests.get(f"{BASE_URL}/todos")
        if response.status_code == 200:
            print("Server is ready!")
            return process
    except requests.exceptions.ConnectionError:
        raise Exception("Server failed to start within timeout period")

def stop_server(process):
    print("Stopping backend server...")
    subprocess.run(['taskkill', '/F', '/T', '/PID', str(process.pid)])
    print("Server stopped.")

class ResourceMonitor(threading.Thread):
    def __init__(self, process):
        super().__init__()
        self.process = psutil.Process(process.pid)
        self.cpu_samples = []
        self.mem_samples = []
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                cpu_percent = self.process.cpu_percent(interval=None) / psutil.cpu_count()
                memory_usage = self.process.memory_info().rss / (1024 * 1024)
                
                for child in self.process.children(recursive=True):
                    try:
                        cpu_percent += child.cpu_percent(interval=None) / psutil.cpu_count()
                        memory_usage += child.memory_info().rss / (1024 * 1024)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                self.cpu_samples.append(cpu_percent)
                self.mem_samples.append(memory_usage)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
                
            time.sleep(0.1)

    def stop(self):
        self.running = False

    def get_metrics(self):
        if not self.cpu_samples or not self.mem_samples:
            return 0, 0
        
        avg_cpu = get_trimmed_mean(self)
        avg_mem = sum(self.mem_samples) / len(self.mem_samples)
        
        return avg_cpu, avg_mem

def get_trimmed_mean(self, lower_percentile=10, upper_percentile=90):
    if not self.cpu_samples:
        return 0
    
    sorted_samples = sorted(self.cpu_samples)
    lower_idx = int(len(sorted_samples) * (lower_percentile / 100))
    upper_idx = int(len(sorted_samples) * (upper_percentile / 100))
    
    trimmed_samples = sorted_samples[lower_idx:upper_idx]
    return sum(trimmed_samples) / len(trimmed_samples) if trimmed_samples else 0
    
def measure_operation(server_process, operation, operation_name):
    print(f"Starting operation: {operation_name}")
    monitor = ResourceMonitor(server_process)
    monitor.start()
    
    start_time = time.time()
    result = operation()
    duration = time.time() - start_time
    
    monitor.stop()
    monitor.join()
    cpu_usage, mem_usage = monitor.get_metrics()
    print(f"Completed operation: {operation_name} in {duration:.2f} seconds")
    return result, duration, cpu_usage, mem_usage

def perform_test_sequence(max_objects):
    print(f"\nStarting test sequence with {max_objects} objects")
    results = {'operations': []}
    server_process = start_server()
    
    try:
        projects = []
        todos = []
        
        for i in range(1, max_objects + 1):
            print(f"\n=== Processing iteration {i}/{max_objects} ===")
            
            def create_and_connect_todo():
                todo_id = util.create_todo()
                if projects:
                    util.post_on_todos_id(todo_id, projects)
                return todo_id
            
            result, duration, cpu, mem = measure_operation(
                server_process,
                create_and_connect_todo,
                f"Creating and Connecting Todo {i}"
            )
            todos.append(result)
            results['operations'].append({
                'type': 'todo_operations',
                'count': i,
                'duration': duration,
                'cpu': cpu,
                'mem': mem
            })
            
            def create_and_connect_project():
                project_id = util.create_project()
                if todos:
                    util.post_on_projects_id(project_id, todos)
                return project_id
            
            result, duration, cpu, mem = measure_operation(
                server_process,
                create_and_connect_project,
                f"Creating and Connecting Project {i}"
            )
            projects.append(result)
            results['operations'].append({
                'type': 'project_operations',
                'count': i,
                'duration': duration,
                'cpu': cpu,
                'mem': mem
            })
        
        print("\n=== Starting deletion phase ===")
        for i, (project_id, todo_id) in enumerate(reversed(list(zip(projects, todos))), 1):
            _, duration, cpu, mem = measure_operation(
                server_process,
                lambda: util.delete_todo(todo_id),
                f"Deleting Todo {max_objects - i + 1}"
            )
            results['operations'].append({
                'type': 'delete_todo',
                'count': max_objects - i + 1,
                'duration': duration,
                'cpu': cpu,
                'mem': mem
            })
            
            _, duration, cpu, mem = measure_operation(
                server_process,
                lambda: util.delete_project(project_id),
                f"Deleting Project {max_objects - i + 1}"
            )
            results['operations'].append({
                'type': 'delete_project',
                'count': max_objects - i + 1,
                'duration': duration,
                'cpu': cpu,
                'mem': mem
            })
            
    finally:
        stop_server(server_process)
        
    return results

def plot_results(results):
    todo_operations = {'todo_operations', 'delete_todo'}
    project_operations = {'project_operations', 'delete_project'}
    
    metrics = {
        'duration': 'Execution Time (seconds)',
        'cpu': 'CPU Usage (%)',
        'mem': 'Memory Usage (MB)'
    }
    
    for metric, ylabel in metrics.items():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        for op_type in todo_operations:
            data = [(op['count'], op[metric]) 
                   for op in results['operations'] 
                   if op['type'] == op_type]
            if data:
                x, y = zip(*data)
                ax1.scatter(x, y, label=op_type, alpha=0.5)
                
                if len(x) > 1:
                    z = np.polyfit(x, y, 2)
                    p = np.poly1d(z)
                    x_smooth = np.linspace(min(x), max(x), 100)
                    ax1.plot(x_smooth, p(x_smooth), '-', linewidth=1)
        
        ax1.set_xlabel('Number of Objects')
        ax1.set_ylabel(ylabel)
        ax1.set_title(f'Todo Operations - {ylabel} vs Number of Objects')
        ax1.grid(True)
        ax1.legend()
        
        for op_type in project_operations:
            data = [(op['count'], op[metric]) 
                   for op in results['operations'] 
                   if op['type'] == op_type]
            if data:
                x, y = zip(*data)
                ax2.scatter(x, y, label=op_type, alpha=0.5)
                
                if len(x) > 1:
                    z = np.polyfit(x, y, 2)
                    p = np.poly1d(z)
                    x_smooth = np.linspace(min(x), max(x), 100)
                    ax2.plot(x_smooth, p(x_smooth), '-', linewidth=1)
        
        ax2.set_xlabel('Number of Objects')
        ax2.set_ylabel(ylabel)
        ax2.set_title(f'Project Operations - {ylabel} vs Number of Objects')
        ax2.grid(True)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(f'{metric}_separated_charts.png')
        plt.close()

if __name__ == '__main__':
    results = perform_test_sequence(500)
    plot_results(results)
    with open('performance_results.json', 'w') as f:
        json.dump(results, f, indent=2)