import unittest
import test_trip_checklist_models

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.makeSuite(test_trip_checklist_models.TripChecklistModelsTest))

    print("Test Summary:")
    print("-" * 30)
    print(f"{'Test':<20} {'Result':<10}")
    print("-" * 30)

    for test, outcome in zip(result.errors + result.failures, ['Error', 'Failure']):
        if test:
            test_name = test[1][0].id().split('.')[-1]
            print(f"{test_name:<20} {outcome:<10}")

    print("-" * 30)
    print(f"{'Total Tests':<20} {result.testsRun:<10}")
    print(f"{'Errors':<20} {len(result.errors):<10}")
    print(f"{'Failures':<20} {len(result.failures):<10}")
