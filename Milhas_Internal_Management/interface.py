import streamlit as st
from management_system import User, ManagementSystem

# Create a new management system
ms = ManagementSystem()

# Define Streamlit app layout
st.title("Internal Management System")
menu_options = ["Add User", "Search User", "Update User", "Delete User"]
menu_choice = st.sidebar.selectbox("Select an option", menu_options)

# Define Streamlit app functionality
if menu_choice == "Add User":
    st.header("Add User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    age = st.number_input("Age", min_value=0)
    photo = st.file_uploader("Photo")
    course = st.text_input("Course")
    sector = st.text_input("Working Sector")
    points = 0
    project = st.text_input("Assigned Project")
    if st.button("Add"):
        ms.add_user(name, email, phone, age, photo, course, sector, points, project)
        st.success("User added successfully.")

elif menu_choice == "Search User":
    st.header("Search User")
    name = st.text_input("Name")
    user = ms.search_user(name)
    if user:
        st.subheader("User Found:")
        st.write(user)
        st.image(user.photo)
    else:
        st.warning("User not found.")

elif menu_choice == "Update User":
    st.header("Update User")
    name = st.text_input("Name")
    user = ms.search_user(name)
    if user:
        st.subheader("Current Information:")
        st.write(user)
        st.image(user.photo)
        st.subheader("Update Information:")
        new_name = st.text_input("Name", value=user.name)
        new_email = st.text_input("Email", value=user.email)
        new_phone = st.text_input("Phone", value=user.phone)
        new_age = st.number_input("Age", min_value=0, value=user.age)
        new_photo = st.file_uploader("Photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
        new_course = st.text_input("Course", value=user.course)
        new_sector = st.text_input("Working Sector", value=user.sector)
        new_points = st.number_input("Points", min_value=0, value=user.points)
        new_project = st.text_input("Assigned Project", value=user.project)
        if st.button("Update"):
            ms.update_user_info(user, new_name, new_email, new_phone, new_age, new_photo, new_course, new_sector, new_points, new_project)
            st.success("User updated successfully.")
    else:
        st.warning("User not found.")

elif menu_choice == "Delete User":
    st.header("Delete User")
    name = st.text_input("Name")
    user = ms.search_user(name)
    if user:
        st.subheader("User to be deleted:")
        st.write(user)
        st.image(user.photo)
        if st.button("Delete"):
            ms.remove_user(user)
            st.success("User deleted successfully.")
    else:
        st.warning("User not found.")
