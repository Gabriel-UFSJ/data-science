import streamlit as st
from management_system import ManagementSystem, Employee, Shift

management_system = ManagementSystem()

def main():
    st.title("Employee Management System")
    choice = st.sidebar.selectbox("Select an action", ["Register Employee", "Edit Employee", "Delete Employee", "Filter Employees"])

    if choice == "Register Employee":
        st.header("Register Employee")
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=18, max_value=100)
        degree = st.text_input('Degree')
        role = st.text_input('Role')
        shift = st.selectbox('Shift', [Shift.MORNING, Shift.AFTERNOON, Shift.NIGHT])
        date_of_entry = st.text_input('Date of Entry', help='YYYY-MM-DD')
        enrolled_in_optional_class = st.checkbox('Enrolled in Optional Class?')
        active_weekdays = st.multiselect('Active Weekdays', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        if st.button('Register'):
            employee = Employee(name, age, degree, role, shift, date_of_entry, enrolled_in_optional_class, active_weekdays)
            management_system.register_employee(employee)
            st.success('Employee registered successfully.')

    elif choice == "Edit Employee":
        st.header("Edit Employee")
        employees = management_system._read_file()
        employee_index = st.selectbox('Select an employee', range(len(employees)))
        employee = employees[employee_index]
        name = st.text_input('Name', value=employee.name)
        age = st.number_input('Age', value=employee.age, min_value=18, max_value=100)
        degree = st.text_input('Degree', value=employee.degree)
        role = st.text_input('Role', value=employee.role)
        shift = st.selectbox('Shift', [Shift.MORNING, Shift.AFTERNOON, Shift.NIGHT], index=employee.shift.value-1)
        date_of_entry = st.text_input('Date of Entry', value=employee.date_of_entry, help='YYYY-MM-DD')
        enrolled_in_optional_class = st.checkbox('Enrolled in Optional Class?', value=employee.enrolled_in_optional_class)
        active_weekdays = st.multiselect('Active Weekdays', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], default=employee.active_weekdays)
        if st.button('Update'):
            employee = Employee(name, age, degree, role, shift, date_of_entry, enrolled_in_optional_class, active_weekdays)
            management_system.edit_employee(employee_index, employee)
            st.success('Employee updated successfully.')

    elif choice == "Delete Employee":
        st.header("Delete Employee")
        employees = management_system._read_file()
        employee_index = st.selectbox('Select an employee', range(len(employees)))
        if st.button('Delete'):
            management_system.delete_employee(employee_index)
            st.success('Employee deleted successfully.')

    elif choice == "Filter Employees":
        st.header("Filter Employees")
        shift = st.selectbox('Select a shift', [Shift.MORNING, Shift.AFTERNOON, Shift.NIGHT])
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        selected_weekdays = st.multiselect('Select weekdays', weekdays)
        employees = management_system.filter(shift=shift, weekdays=selected_weekdays)
        if employees:
            st.write(f"{len(employees)} employees found:")
            for employee in employees:
                st.write(employee)
        else:
            st.warning('No employees found for the selected filters.')

if __name__ == '__main__':
    main()
