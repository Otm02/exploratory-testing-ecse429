import unittest
import random
from test_todos_documented import TestTodosDocumented
from test_todos_undocumented import TestTodosUndocumented
from test_projects_documented import TestProjectsDocumented
from test_projects_undocumented import TestProjectsUndocumented
from test_bugs import TestBugs
from test_malformed_payloads import TestMalformedPayloads
from test_invalid_operations import TestInvalidOperations


def load_tests(loader, standard_tests, pattern):
    """Load tests and shuffle them to run in random order."""
    test_classes = [
        TestTodosDocumented,
        TestTodosUndocumented,
        TestProjectsDocumented,
        TestProjectsUndocumented,
        TestBugs,
        TestMalformedPayloads,
        TestInvalidOperations,
    ]

    all_tests = []
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        all_tests.extend(tests)

    # Print the list of tests before shuffling in a more readable format
    print("========== Tests before shuffling ==========")
    for i, test in enumerate(all_tests, 1):
        print(f"{i}. {test}")

    random.shuffle(all_tests)

    # Print the list of tests after shuffling
    print("\n========== Tests after shuffling ==========")
    for i, test in enumerate(all_tests, 1):
        print(f"{i}. {test}")

    suite = unittest.TestSuite(all_tests)
    return suite


if __name__ == "__main__":
    unittest.main()
