import streamlit as st

# import the Project class and its methods
from project import Project


# create a Streamlit app with a title and a sidebar
st.set_page_config(page_title="Project Price Calculator", page_icon=":money_with_wings:")
st.sidebar.title("Project Parameters")


# define a function to get the project parameters from the user
def get_project_parameters():
    complexity = st.sidebar.selectbox("Select the complexity of the project:", ["low", "mid", "high"])
    time_frame = st.sidebar.slider("Select the time frame (in months) for the project:", 1, 6, 3)
    members = st.sidebar.slider("Select the number of assigned members for the project:", 1, 5, 3)

    return complexity, time_frame, members


# get the user credentials from the user
def get_credentials():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    return username, password


# check if the entered credentials match the expected values
def authenticate(username, password):
    if username == "admin" and password == "linklink":
        return True
    else:
        return False


# get the project parameters from the user
username, password = get_credentials()

if authenticate(username, password):
    complexity, time_frame, members = get_project_parameters()

    # create a Project object with the user's chosen parameters
    my_project = Project(complexity, time_frame, members)

    # calculate the price of the project using the calculate_price() method
    price = my_project.calculate_price()

    # display the project parameters and the calculated price
    st.write(f"Project parameters: Complexity = {complexity}, Time frame = {time_frame} months, Members = {members}")
    st.write(f"Price: {price:.2f} Brazilian reals")
else:
    st.write("Invalid username or password")
