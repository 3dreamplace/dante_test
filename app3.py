from dotenv import load_dotenv
import os
import requests
import logging
from langsmith import Client


load_dotenv()  # Loads variables from a .env file in the current directory


print("LANGCHAIN_API_KEY:", os.getenv("LANGCHAIN_API_KEY"))
print("LANGCHAIN_TRACING_V2:", os.getenv("LANGCHAIN_TRACING_V2", "true"))
print("LANGCHAIN_ENDPOINT:", os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"))

# Retrieve and verify API key
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
if not LANGCHAIN_API_KEY:
    raise ValueError("LANGCHAIN_API_KEY environment variable is not set.")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Client(api_key=LANGCHAIN_API_KEY)

# -------------------------------
api_url = "https://brazilian-laws-chatbot.onrender.com/query-llm"



def get_response_from_api(prompt):
    """
    Sends a prompt to the API and logs the response to LangSmith.
    """
    try:
        # Create a run in LangSmith
        run = client.create_run(
            name="API Query",
            project_name="Brazilian-Laws-Chatbot",
            inputs={"query": prompt},
            run_type="chain",
        )


        run_id = run.get("id") if isinstance(run, dict) else getattr(run, "id", None)
        if not run_id:
            error_msg = "Error: Run creation did not return an ID."
            logger.error(error_msg)
            return error_msg, None

        print(f"Run created successfully. Run ID: {run_id}")

        payload = {"query": prompt}

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            full_response = response.json()
            gpt_response = full_response.get("gpt_response", "No response from API.")
            vectara_response = full_response.get("vectara_response", "No Vectara response.")

            # Log the successful output to LangSmith
            client.end_run(
                run_id=run_id,
                outputs={"gpt_response": gpt_response, "vectara_response": vectara_response},
            )
            print(f"Run ended successfully. Outputs logged: {gpt_response}, {vectara_response}")
            return gpt_response, vectara_response
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            client.end_run(run_id=run_id, error=error_msg)
            print(f"Run ended with error: {error_msg}")
            return error_msg, None

    except requests.exceptions.RequestException as e:
        error_msg = f"Request Error: {str(e)}"
        logger.error(error_msg)
        if 'run_id' in locals() and run_id:
            client.end_run(run_id=run_id, error=error_msg)
        print(f"Run ended with error: {error_msg}")
        return error_msg, None

    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        logger.error(error_msg)
        if 'run_id' in locals() and run_id:
            client.end_run(run_id=run_id, error=error_msg)
        print(f"Run ended with error: {error_msg}")
        return error_msg, None



if __name__ == "__main__":
    prompt = "What are the legal rights of employees in Brazil?"
    gpt_response, vectara_response = get_response_from_api(prompt)
    print("GPT Response:", gpt_response)
    print("Vectara Response:", vectara_response)
