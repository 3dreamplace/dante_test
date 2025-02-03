import streamlit as st
import requests

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

# Button to generate response
if st.button("Generate Response"):
    with st.spinner('Generating response...'):
        # Fetching response from the REST API
        response, vectara_response = get_response_from_api(prompt)
        # Displaying the GPT response in Streamlit
        st.write(response)

        # Displaying the Vectara response (all chunks) below the GPT response
        if vectara_response:
            st.subheader("Vectara Response (Chunks):")
            st.write(vectara_response)
