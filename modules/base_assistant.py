from typing import List, Dict
import logging
import os
from modules.deepseek import conversational_prompt
from modules.utils import build_file_name_session
from RealtimeTTS import TextToAudioStream, SystemEngine, ElevenlabsEngine
import time


class PlainAssistant:
    def __init__(self, logger: logging.Logger, session_id: str):
        self.logger = logger
        self.session_id = session_id
        self.conversation_history = []
        self.engine = SystemEngine()  # Can be replaced with other engines
        self.stream = TextToAudioStream(self.engine)

    def process_text(self, text: str) -> str:
        """Process text input and generate response"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": text})

            # Generate response using DeepSeek
            self.logger.info("🤖 Processing text with DeepSeek...")
            response = conversational_prompt(self.conversation_history)

            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response})

            # Speak the response
            self.speak(response)

            return response

        except Exception as e:
            self.logger.error(f"❌ Error occurred: {str(e)}")
            raise

    def speak(self, text: str):
        """Convert text to speech and play it"""
        try:
            self.logger.info(f"🔊 Speaking: {text}")
            self.stream.feed(text)
            self.stream.play()

        except Exception as e:
            self.logger.error(f"❌ Error in speech synthesis: {str(e)}")
            raise
