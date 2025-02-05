from dotenv import load_dotenv
import os
import requests
import logging
from langsmith import Client

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Get API Key correctly
LANGCHAIN_API_KEY = os.getenv("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")
if not LANGCHAIN_API_KEY:
    raise ValueError("LANGCHAIN_API_KEY environment variable is not set.")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# ✅ Pass API Key explicitly
client = Client(api_key=LANGCHAIN_API_KEY)

# Define the API URL
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"

def get_response_from_api(prompt):
    """
    Sends a prompt to the API and logs the response to LangSmith.
    """
    try:
        # Start a run in LangSmith
        with client.run_on(project_name="Brazilian-Laws-Chatbot", inputs={"query": prompt}, run_type="chain") as run:
            # Define the payload
            payload = {"query": prompt}

            # Make the API request
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                full_response = response.json()
                gpt_response = full_response.get("gpt_response", "No response from API.")
                vectara_response = full_response.get("vectara_response", "No Vectara response.")

                # Log output to LangSmith
                run.log_outputs({"gpt_response": gpt_response, "vectara_response": vectara_response})

                return gpt_response, vectara_response
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                run.log_error(error_msg)
                return error_msg, None

    except requests.exceptions.RequestException as e:
        error_msg = f"Request Error: {str(e)}"
        logger.error(error_msg)
        run.log_error(error_msg)
        return error_msg, None
    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        logger.error(error_msg)
        run.log_error(error_msg)
        return error_msg, None

if __name__ == "__main__":
    prompt = "What are the legal rights of employees in Brazil?"
    gpt_response, vectara_response = get_response_from_api(prompt)
    print("GPT Response:", gpt_response)
    print("Vectara Response:", vectara_response)