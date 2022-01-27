
import unittest
from unittest.mock import patch
from employee_manage import Employee
#  module "test_employee_manage.py"
class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.database_return = True
        self.emp_email = "me@email.com"
        self.report1 = "done"
        self.report2 = "in_progress"
        self.report3 = "start"
        self.task_list = [1, 2, 3]

    def tearDown(self):
        pass

    @patch("employee_manage.Employee.call_database")
    def test_check_employee_Return_true_when_employee_added(self, mock_call_database):
        emp = Employee()
        mock_call_database.return_value = self.database_return
        print("Test 1 executed")
        self.assertEqual(emp.check_employee(self.emp_email), True)

    @patch("employee_manage.Employee.call_database")
    def test_check_employee_Passes_correct_parameters_to_call_database(self, mock_call_database):
        emp = Employee()
        mock_call_database.return_value = self.database_return
        print("Test 2 executed")
        emp.check_employee(self.emp_email)
        mock_call_database.assert_called_once_with(self.emp_email)

    @patch("employee_manage.Employee.get_report")
    def test_add_task_Returns_true_with_correct_parameters(
        self, mock_get_report
    ):
        emp = Employee()
        list_of_values = [self.report3, self.report2, self.report1]

        def side_effect(self):
            return list_of_values.pop()
        mock_get_report.side_effect = side_effect
        print("Test 3 executed")
        self.assertEqual(emp.add_task(self.task_list), True)

if __name__ == "__main__":

    unittest.main()