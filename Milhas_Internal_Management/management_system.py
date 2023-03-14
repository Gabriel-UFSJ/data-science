import csv
from enum import Enum
from typing import List

class Shift(Enum):
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    NIGHT = 'Night'

class Employee:
    def __init__(self, name: str, age: int, degree: str, role: str, shift: Shift, date_of_entry: str, enrolled_in_optional_class: bool, active_weekdays: List[str]):
        self.name = name
        self.age = age
        self.degree = degree
        self.role = role
        self.shift = shift
        self.date_of_entry = date_of_entry
        self.enrolled_in_optional_class = enrolled_in_optional_class
        self.active_weekdays = active_weekdays

    def __str__(self):
        return f"{self.name} ({self.shift.value})"

class ManagementSystem:
    def __init__(self):
        self.filename = 'employees.csv'

    def _write_file(self, employees: List[Employee]):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Age', 'Degree', 'Role', 'Shift', 'Date of Entry', 'Enrolled in Optional Class', 'Active Weekdays'])
            for employee in employees:
                writer.writerow([employee.name, employee.age, employee.degree, employee.role, employee.shift.value, employee.date_of_entry, employee.enrolled_in_optional_class, ', '.join(employee.active_weekdays)])

    def _read_file(self) -> List[Employee]:
        employees = []
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    active_weekdays = row['Active Weekdays'].split(', ')
                    shift = Shift(row['Shift'])
                    employee = Employee(row['Name'], int(row['Age']), row['Degree'], row['Role'], shift, row['Date of Entry'], row['Enrolled in Optional Class'] == 'True', active_weekdays)
                    employees.append(employee)
        except FileNotFoundError:
            pass
        return employees

    def register_employee(self, employee: Employee):
        employees = self._read_file()
        employees.append(employee)
        self._write_file(employees)

    def edit_employee(self, index: int, employee: Employee):
        employees = self._read_file()
        employees[index] = employee
        self._write_file(employees)

    def delete_employee(self, index: int):
        employees = self._read_file()
        del employees[index]
        self._write_file(employees)

    def filter(self, shift: Shift, weekdays: List[str]) -> List[Employee]:
        employees = self._read_file()
        filtered_employees = [employee for employee in employees if employee.shift == shift and set(weekdays).issubset(set(employee.active_weekdays))]
        return filtered_employees
