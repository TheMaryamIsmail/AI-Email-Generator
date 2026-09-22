import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def generate_email_content(recipient: str, tone: str, purpose: str, key_points: str) -> str:
    """
    Calls the Google Gemini API to generate a professional email.
    """
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

    # Using the standard recommended model for text generation tasks
    model = genai.GenerativeModel("gemini-3.5-flash")

    prompt = f"""
    You are an expert AI copywriter and professional communications assistant. 
    Write a complete, well-formatted email based on the following parameters:

    - Recipient: {recipient}
    - Tone: {tone}
    - Purpose/Subject: {purpose}
    - Key Points to Include: {key_points}

    Guidelines:
    - Provide a clear subject line at the very top.
    - Keep the formatting clean with proper salutations, body paragraphs, and professional sign-offs.
    - Do not include any meta-commentary or conversational filler outside the email draft itself.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to generate email via Gemini API: {str(e)}")
print("done")