import requests
import os
from langsmith import Client

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

client = Client()

# Define the API URL
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"

def get_response_from_api(prompt):
    # ✅ FIX: Added `run_type`
    run = client.create_run(name="API Query", inputs={"query": prompt}, run_type="chain")

    try:
        # Define the payload
        payload = {"query": prompt}

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            full_response = response.json()
            gpt_response = full_response.get("gpt_response", "No response from API.")
            vectara_response = full_response.get("vectara_response", "No Vectara response.")

            # ✅ Log output to LangSmith
            client.end_run(run["id"], outputs={"gpt_response": gpt_response, "vectara_response": vectara_response})

            return gpt_response, vectara_response
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            client.end_run(run["id"], error=error_msg)
            return error_msg, None

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        client.end_run(run["id"], error=error_msg)
        return error_msg, None

if __name__ == "__main__":
    prompt = "What are the legal rights of employees in Brazil?"
    gpt_response, vectara_response = get_response_from_api(prompt)
    print("GPT Response:", gpt_response)
    print("Vectara Response:", vectara_response)
