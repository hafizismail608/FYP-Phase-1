import google.generativeai as genai
import logging
from dotenv import load_dotenv

class GeminiService:
    def __init__(self, api_key):
        self.model = None
        self.chat = None
        self.logger = logging.getLogger(__name__)
        load_dotenv()
        self._initialize(api_key)

    def _initialize(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-1.5-flash')
            self.chat = self.model.start_chat(history=[])
            self.logger.info("Gemini service initialized successfully with Gemini 1.5 Flash")
        except Exception as e:
            self.logger.error(f"Error initializing Gemini service: {str(e)}")
            self.model = None
            self.chat = None

    def send_message(self, message):
        if not self.model or not self.chat:
            self.logger.error("Gemini model or chat not initialized")
            return "AI service is not properly initialized. Please check the configuration."
        try:
            # Check if the message is about formatting correction
            if ("correct the formating" in message.lower() or 
                "format the response" in message.lower() or
                "new paragraph" in message.lower() or
                "new line" in message.lower()):
                # Add system instruction for proper formatting
                formatting_instruction = (
                    "Format your response with proper headings and paragraphs. Follow these rules:\n"
                    "1. Use bold for headings without asterisks or other symbols in the final output\n"
                    "2. Each heading should be on its own line\n"
                    "3. Each paragraph should start on a new line\n"
                    "4. Use clean formatting with proper spacing between elements"
                )
                response = self.chat.send_message(formatting_instruction + "\n\n" + message)
            else:
                response = self.chat.send_message(message)
            
            # Process response to ensure proper formatting
            response_text = response.text
            
            # Replace markdown-style headings with HTML bold tags for better display
            import re
            # Replace patterns like '* **Heading:**' with '<strong>Heading:</strong>'
            response_text = re.sub(r'\*\s*\*\*([^*]+)\*\*', r'<strong>\1</strong>', response_text)
            # Replace patterns like '**Heading:**' with '<strong>Heading:</strong>'
            response_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', response_text)
            
            # Ensure paragraphs are properly separated with <p> tags
            # First, normalize newlines
            response_text = response_text.replace('\r\n', '\n')
            
            # Replace double newlines with paragraph breaks
            response_text = re.sub(r'\n\s*\n', '</p><p>', response_text)
            
            # Ensure headings are on their own line
            response_text = re.sub(r'([.!?])\s*<strong>', r'\1</p><p><strong>', response_text)
            response_text = re.sub(r'</strong>\s*([A-Z])', r'</strong></p><p>\1', response_text)
            
            # Wrap the entire content in paragraph tags if not already
            if not response_text.startswith('<p>'):
                response_text = '<p>' + response_text
            if not response_text.endswith('</p>'):
                response_text = response_text + '</p>'
            
            return response_text
        except Exception as e:
            self.logger.error(f"Error in chat: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."