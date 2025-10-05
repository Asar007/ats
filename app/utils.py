import PyPDF2
import io
import openai
import os
from dotenv import load_dotenv

# --- Best Practice: Load environment variables and initialize the client once ---
# This client will be reused for all API calls.
# The OpenAI() constructor automatically reads the "OPENAI_API_KEY" from the environment.
load_dotenv()
client = openai.OpenAI()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file provided as bytes."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text.strip()
    except Exception as e:
        # Handle potential PyPDF2 errors, e.g., for corrupted PDFs
        print(f"Error extracting PDF text: {e}")
        return ""

def call_openai(prompt: str) -> str:
    """Calls the OpenAI Chat Completions API with a given prompt."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        # Handle API errors (e.g., rate limits, server issues)
        print(f"OpenAI API Error: {e}")
        return "Error: Could not get a response from the API."

# Example Usage (optional)
# if __name__ == "__main__":
#     sample_prompt = "Summarize the following text: ..."
#     summary = call_openai(sample_prompt)
#     print(summary)