import os
import json
import streamlit as st
from typing import Optional, Dict, Any, List
import requests
import base64

# Import AI libraries
try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False

# OpenAI removed as requested
OPENAI_AVAILABLE = False


class AIClient:
    """Unified AI client for multiple providers"""

    def __init__(self):
        self.gemini_client = None
        self._init_clients()

    def _init_clients(self):
        """Initialize AI clients with API keys"""
        # Initialize Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and GEMINI_AVAILABLE and genai:
            try:
                genai.configure(api_key=gemini_key)
                self.gemini_client = genai
            except Exception as e:
                print(f"Failed to initialize Gemini: {str(e)}")

        # OpenAI support removed

    def generate_text(self, prompt: str, model: str = "gemini", max_tokens: int = 1000) -> str:
        """Generate text using specified AI model"""
        try:
            if model == "gemini" and self.gemini_client:
                model_instance = self.gemini_client.GenerativeModel("gemini-1.5-flash")
                response = model_instance.generate_content(prompt)
                return response.text if hasattr(response, 'text') and response.text else "No response generated"

            else:
                return "Gemini model not available. Please check your Gemini API key."

        except Exception as e:
            return f"Error generating text: {str(e)}"

    def analyze_image(self, image_data: bytes, prompt: str = "Analyze this image") -> str:
        """Analyze image using AI"""
        try:
            if self.gemini_client:
                import PIL.Image
                import io
                image = PIL.Image.open(io.BytesIO(image_data))
                model_instance = self.gemini_client.GenerativeModel("gemini-1.5-flash")
                response = model_instance.generate_content([prompt, image])
                return response.text if response.text else "No analysis available"

            else:
                return "Image analysis only available with Gemini. Please check your Gemini API key."

        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def generate_image(self, prompt: str, model: str = "gemini") -> Optional[bytes]:
        """Generate image using AI"""
        try:
            # Note: Gemini image generation is currently not available in this setup
            if model == "gemini" and self.gemini_client:
                return None

            elif model == "openai" and self.openai_client:
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                )

                # Download image from URL
                if response.data and len(response.data) > 0:
                    image_url = response.data[0].url
                    if image_url:
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            return img_response.content

            return None

        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if self.gemini_client:
                prompt = f"""
                Analyze the sentiment of the following text and provide:
                1. Overall sentiment (positive/negative/neutral)
                2. Confidence score (0-1)
                3. Key emotional indicators
                4. Brief explanation

                Text: {text}

                Respond in JSON format.
                """

                model_instance = self.gemini_client.GenerativeModel("gemini-1.5-flash")
                response = model_instance.generate_content(prompt)

                if response.text:
                    return json.loads(response.text)

            return {"error": "Sentiment analysis only available with Gemini. Please check your Gemini API key."}

        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        try:
            prompt = f"Translate the following text to {target_language}: {text}"
            return self.generate_text(prompt)
        except Exception as e:
            return f"Translation failed: {str(e)}"

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize text to specified number of sentences"""
        try:
            prompt = f"Summarize the following text in {max_sentences} sentences: {text}"
            return self.generate_text(prompt)
        except Exception as e:
            return f"Summarization failed: {str(e)}"

    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        models = []
        if self.gemini_client:
            models.append("gemini")
        return models


# Global AI client instance
ai_client = AIClient()
