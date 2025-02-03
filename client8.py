import streamlit as st
import requests
import time

# Streamlit app title
st.title("Professional Guidance for Real Estate Registry Offices")

# Define the API URL
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"
# # Define the API URL
# api_url = "http://127.0.0.1:5000/query-llm"

# Prompt input
prompt = st.text_input("Enter your Text:")

# Function to call the REST API and return the response
def get_response_from_api(prompt):
    try:
        # Define the payload
        payload = {"query": prompt}
        # Make a POST request to the API
        response = requests.post(api_url, json=payload)
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the full response JSON
            full_response = response.json()
            # Extract gpt_response and vectara_response
            gpt_response = full_response.get("gpt_response", "No response from API.")
            vectara_response = full_response.get("vectara_response", "No Vectara response.")
            return gpt_response, vectara_response
        else:
            return f"Error: {response.status_code} - {response.text}", None
    except Exception as e:
        return f"An error occurred: {str(e)}", None

# Initialize session state for vectara_response if it doesn't exist
if "vectara_response" not in st.session_state:
    st.session_state["vectara_response"] = "No Vectara response."

# Button to generate response
if st.button("Generate Response"):
    with st.spinner('Generating response...'):
        # Fetching response from the REST API
        response, vectara_response = get_response_from_api(prompt)
        # Displaying the GPT response in Streamlit
        st.write(response)

        # Update the session state for vectara_response
        st.session_state["vectara_response"] = vectara_response

# Box displaying the value of the 'vida' variable at the bottom of the page
st.subheader("Variable 'vida':")
vida = "viva"
st.info(f"The value of 'vida' is: {vida}")

# Box displaying the value of the 'vectara_response' variable
st.subheader("Variable 'vectara_response':")
st.info(f"The value of 'vectara_response' is: {st.session_state['vectara_response']}")

# Check variable functionality
st.subheader("Check Variable")
variable_name = st.text_input("Enter the variable name to check:")
if variable_name:
    if variable_name in globals():
        st.success(f"The value of '{variable_name}' is: {globals()[variable_name]}")
    elif variable_name in st.session_state:
        st.success(f"The value of '{variable_name}' is: {st.session_state[variable_name]}")
    else:
        st.error(f"Variable '{variable_name}' is not defined.")

# Development Dashboard: Auto-refresh for debugging variables
st.subheader("Development Dashboard")
def auto_refresh():
    while True:
        st.write("Refreshing Debug Panel...")
        st.write("Current values:")
        st.json({
            "vida": vida,
            "vectara_response": st.session_state["vectara_response"]
        })
        time.sleep(1)

placeholder = st.empty()
if st.button("Start Auto-Refresh"):
    with placeholder.container():
        auto_refresh()
