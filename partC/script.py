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
from queue import Queue
from collections import deque
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from partA import util

BASE_URL = "http://localhost:4567"
JAR_PATH = r"runTodoManagerRestAPI-1.5.5.jar"


def start_server():
    print("Starting backend server...")

    jvm_args = ["java", "-Xmx6g", "-jar", JAR_PATH]
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
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)])
    print("Server stopped.")


class ResourceMonitor(threading.Thread):
    def __init__(self, process, sample_interval=0.1):
        super().__init__()
        self.process = psutil.Process(process.pid)
        self.sample_interval = sample_interval
        self.cpu_samples = deque()
        self.mem_samples = deque()
        self.running = False
        self.sample_queue = Queue()
        self.last_cpu_times = {}
        self.daemon = True

    def run(self):
        self.running = True
        while self.running:
            try:
                self._collect_sample()
                time.sleep(self.sample_interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break

        self._process_queue_samples()

    def _collect_sample(self):
        try:
            processes = [self.process] + self.process.children(recursive=True)
            cpu_total = 0
            memory_total = 0

            for proc in processes:
                try:
                    cpu_times = proc.cpu_times()
                    proc_id = proc.pid
                    
                    if proc_id in self.last_cpu_times:
                        last_times = self.last_cpu_times[proc_id]
                        cpu_percent = (
                            ((cpu_times.user - last_times.user) + 
                             (cpu_times.system - last_times.system)) * 100 /
                            self.sample_interval
                        )
                        cpu_total += cpu_percent / psutil.cpu_count()
                    
                    self.last_cpu_times[proc_id] = cpu_times
                    memory_total += proc.memory_info().rss / (1024 * 1024)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            self.sample_queue.put((cpu_total, memory_total))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return

    def _process_queue_samples(self):
        while not self.sample_queue.empty():
            cpu, mem = self.sample_queue.get()
            self.cpu_samples.append(cpu)
            self.mem_samples.append(mem)

    def stop(self):
        self.running = False
        self.join()
        self._process_queue_samples()

    def get_metrics(self):
        if not self.cpu_samples or not self.mem_samples:
            return 0, 0

        avg_cpu = self._get_filtered_mean()
        avg_mem = sum(self.mem_samples) / len(self.mem_samples)

        return avg_cpu, avg_mem

    def _get_filtered_mean(self):
        if not self.cpu_samples:
            return 0

        non_zero_samples = [sample for sample in self.cpu_samples if sample > 0]
        return sum(non_zero_samples) / len(non_zero_samples) if non_zero_samples else 0


def measure_operation(server_process, operation, operation_name):
    print(f"Starting operation: {operation_name}")
    monitor = ResourceMonitor(server_process)
    monitor.start()

    start_time = time.time()
    result = operation()
    duration = time.time() - start_time

    monitor.stop()
    cpu_usage, mem_usage = monitor.get_metrics()
    print(f"Completed operation: {operation_name} in {duration:.2f} seconds")
    return result, duration, cpu_usage, mem_usage


def perform_test_sequence(max_objects):
    print(f"\nStarting test sequence with {max_objects} objects")
    results = {"operations": []}
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
                f"Creating and Connecting Todo {i}",
            )
            todos.append(result)
            results["operations"].append(
                {
                    "type": "Create & Update",
                    "count": i,
                    "duration": duration,
                    "cpu": cpu,
                    "mem": mem,
                }
            )

            def create_and_connect_project():
                project_id = util.create_project()
                if todos:
                    util.post_on_projects_id(project_id, todos)
                return project_id

            result, duration, cpu, mem = measure_operation(
                server_process,
                create_and_connect_project,
                f"Creating and Connecting Project {i}",
            )
            projects.append(result)
            results["operations"].append(
                {
                    "type": "Create & Update",
                    "count": i,
                    "duration": duration,
                    "cpu": cpu,
                    "mem": mem,
                }
            )

        print("\n=== Starting deletion phase ===")
        for i, (project_id, todo_id) in enumerate(list(zip(projects, todos))):
            def delete_todo():
                util.delete_todo(todo_id)
    
            _, duration, cpu, mem = measure_operation(
                server_process,
                delete_todo,
                f"Deleting Todo {max_objects - i + 1}",
            )
            results["operations"].append(
                {
                    "type": "Delete",
                    "count": max_objects - i + 1,
                    "duration": duration,
                    "cpu": cpu,
                    "mem": mem,
                }
            )
            
            def delete_project():
                util.delete_project(project_id)

            _, duration, cpu, mem = measure_operation(
                server_process,
                delete_project,
                f"Deleting Project {max_objects - i + 1}",
            )
            results["operations"].append(
                {
                    "type": "Delete",
                    "count": max_objects - i + 1,
                    "duration": duration,
                    "cpu": cpu,
                    "mem": mem,
                }
            )

    finally:
        stop_server(server_process)

    return results


def plot_results(results):
    todo_operations = {"Create & Update", "Delete"}
    project_operations = {"Create & Update", "Delete"}

    metrics = {
        "duration": "Execution Time (seconds)",
        "cpu": "CPU Usage (%)",
        "mem": "Memory Usage (MB)",
    }

    for metric, ylabel in metrics.items():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        for op_type in todo_operations:
            data = [
                (op["count"], op[metric])
                for op in results["operations"]
                if op["type"] == op_type
            ]
            if data:
                x, y = zip(*data)
                ax1.scatter(x, y, label=op_type, alpha=0.5)

                if len(x) > 1:
                    z = np.polyfit(x, y, 2)
                    p = np.poly1d(z)
                    x_smooth = np.linspace(min(x), max(x), 100)
                    ax1.plot(x_smooth, p(x_smooth), "-", linewidth=1)

        ax1.set_xlabel("Number of Objects")
        ax1.set_ylabel(ylabel)
        ax1.set_title(f"Todo Operations - {ylabel} vs Number of Objects")
        ax1.grid(True)
        ax1.legend()

        for op_type in project_operations:
            data = [
                (op["count"], op[metric])
                for op in results["operations"]
                if op["type"] == op_type
            ]
            if data:
                x, y = zip(*data)
                ax2.scatter(x, y, label=op_type, alpha=0.5)

                if len(x) > 1:
                    z = np.polyfit(x, y, 2)
                    p = np.poly1d(z)
                    x_smooth = np.linspace(min(x), max(x), 100)
                    ax2.plot(x_smooth, p(x_smooth), "-", linewidth=1)

        ax2.set_xlabel("Number of Objects")
        ax2.set_ylabel(ylabel)
        ax2.set_title(f"Project Operations - {ylabel} vs Number of Objects")
        ax2.grid(True)
        ax2.legend()

        plt.tight_layout()
        plt.savefig(f"{metric}_separated_charts.png")
        plt.close()


if __name__ == "__main__":
    results = perform_test_sequence(1000)
    plot_results(results)
    with open("performance_results.json", "w") as f:
        json.dump(results, f, indent=2)