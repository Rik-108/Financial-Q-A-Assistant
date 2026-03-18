from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
WATSON_API_KEY = os.getenv("WATSONX_API_KEY")
WATSON_URL = os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Extract region from URL (e.g., "eu-de.ml.cloud.ibm.com" -> "eu-de")
region = WATSON_URL.split("//")[-1].split(".ml.cloud.ibm.com")[0] if WATSON_URL else None

# Log environment variables for debugging
logger.debug(f"Loaded WATSONX_API_KEY: {'<set>' if WATSON_API_KEY else 'None'}")
logger.debug(f"Loaded WATSONX_URL: {WATSON_URL}")
logger.debug(f"Loaded Region: {region}")
logger.debug(f"Loaded WATSONX_PROJECT_ID: {PROJECT_ID}")

# Validate environment variables
if not WATSON_API_KEY:
    logger.error("WATSONX_API_KEY is not set in .env file")
if not WATSON_URL:
    logger.error("WATSONX_URL is not set in .env file")
if not PROJECT_ID:
    logger.error("WATSONX_PROJECT_ID is not set in .env file")

# Initialize Watsonx credentials
creds = None
if WATSON_API_KEY and WATSON_URL:
    try:
        creds = Credentials(
            url=WATSON_URL,
            api_key=WATSON_API_KEY
        )
        logger.debug("Credentials initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Credentials: {str(e)}")
else:
    logger.error("Cannot initialize Credentials: Missing API key or URL")

# Initialize ModelInference
model = None
if creds and PROJECT_ID:
    try:
        logger.debug("Initializing ModelInference with credentials")
        model = ModelInference(
            model_id="meta-llama/llama-3-3-70b-instruct",
            credentials=creds,
            project_id=PROJECT_ID
        )
        logger.debug("ModelInference initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ModelInference: {str(e)}")
else:
    logger.error("Cannot initialize ModelInference: Missing credentials or project ID")

# Route to serve index.html
@app.route("/")
def serve_index():
    try:
        return send_file("index.html")
    except FileNotFoundError:
        return jsonify({"error": "index.html not found"}), 404

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()
        question = data.get("question")
        if not question:
            logger.error("No question provided in request")
            return jsonify({"error": "No question provided"}), 400

        # Validate model initialization
        if not model:
            error_msg = "ModelInference not initialized. Check credentials and project ID."
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 500

        # Prepare prompt for Watsonx
        prompt = f"You are a financial literacy expert. Provide a simple and accurate answer to this question for beginners: {question}"
        logger.debug(f"Sending prompt to Watsonx API: {prompt}")
        logger.debug(f"Prompt length: {len(prompt)} characters")

        # Generate response using Watsonx
        response = model.generate_text(
            prompt,
            params={
                GenParams.MAX_NEW_TOKENS: 1000,
                GenParams.TEMPERATURE: 0.7,
                GenParams.DECODING_METHOD: "greedy"
                # Removed STOP_SEQUENCES to prevent premature truncation
            }
        )
        logger.debug("Successfully received response from Watsonx API")
        logger.debug(f"Raw response (length: {len(str(response))}): '{response}'")

        # Handle response
        if isinstance(response, str):
            logger.info("Response is a string")
            if not response.strip():
                logger.error("Watsonx returned an empty response")
                return jsonify({"error": "Watsonx returned an empty response"}), 500

            # Check if the prompt is in the response and remove it
            cleaned_response = response
            if prompt in response:
                logger.warning("Response contains prompt; attempting to extract answer")
                cleaned_response = response.replace(prompt, "").strip()
                logger.debug(f"Cleaned response (length: {len(cleaned_response)}): '{cleaned_response}'")

            # Final validation of the cleaned response
            if not cleaned_response:
                logger.error("No valid answer found after cleaning response")
                return jsonify({"error": "Model failed to generate a valid answer"}), 500

            return jsonify({"answer": cleaned_response})
        elif isinstance(response, dict):
            logger.info("Response is a dictionary")
            generated_text = response.get("results", [{}])[0].get("generated_text", "")
            logger.debug(f"Generated text from dict (length: {len(generated_text)}): '{generated_text}'")
            if not generated_text.strip():
                logger.error("Generated text is empty in response")
                return jsonify({"error": "Model failed to generate an answer"}), 500
            return jsonify({"answer": generated_text.strip()})
        else:
            logger.error(f"Unsupported response type: {type(response)}")
            return jsonify({"error": f"Unsupported response type: {type(response)}"}), 500

    except Exception as e:
        error_msg = f"Watsonx API call failed: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == "__main__":
    app.run(debug=True)