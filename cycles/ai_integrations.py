import os
import google.generativeai as genai

# IMPORTANT: Set up your API key
# Create a .env file in the root of your project and add the following line:
# GOOGLE_API_KEY="YOUR_API_KEY"
# Then, uncomment the following lines to load the API key:
from dotenv import load_dotenv
load_dotenv()

# Or, for development, you can set it directly (not recommended for production)
# genai.configure(api_key="YOUR_API_KEY")

def get_ai_interpretation(cycle_name, period_name, user_dob):
    """
    Generates a personalized interpretation for a given cycle period using the Gemini API.
    """
    try:
        # Configure the API key from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == 'YOUR_API_KEY':
            return "Error: GOOGLE_API_KEY not found. Please set it in your .env file."
        genai.configure(api_key=api_key)

        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(m.name)

        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Create the prompt
        prompt = f"""
        You are an expert astrologer and life coach, interpreting the cycles of life based on the teachings of H. Spencer Lewis.
        A user, born on {user_dob}, is currently in the '{period_name}' of their '{cycle_name}' cycle.

        Provide a personalized, encouraging, and insightful interpretation for them.
        The interpretation should be about 100 words long and should offer actionable advice.
        Focus on the opportunities and challenges of this specific period.
        Do not repeat the cycle or period name in your response.
        """

        # Generate the content
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating AI interpretation: {e}"
