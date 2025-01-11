from typing import List
import os
import logging
from datetime import datetime
from modules.assistant_config import get_config
from modules.utils import (
    build_file_name_session,
    create_session_logger_id,
    setup_logging,
)
from modules.deepseek import prefix_prompt
from modules.execute_python import execute_uv_python
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import time


class TyperAgent:
    def __init__(self, logger: logging.Logger, session_id: str):
        self.logger = logger
        self.session_id = session_id
        self.log_file = build_file_name_session("session.log", session_id)
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))
        self.previous_successful_requests = []
        self.previous_responses = []

    @classmethod
    def build_agent(cls, typer_file: str, scratchpad: List[str]):
        """Create and configure a new TyperAssistant instance"""
        # Create session and logging
        session_id = create_session_logger_id()
        logger = setup_logging(session_id)
        logger.info(f"🚀 Starting STT session {session_id}")

        # Verify files exist
        if not os.path.exists(typer_file):
            logger.error(f"📂 Typer file {typer_file} does not exist")
            raise FileNotFoundError(f"Typer file {typer_file} does not exist")

        for file_path in scratchpad:
            if not os.path.exists(file_path):
                logger.error(f"📄 Scratchpad file {file_path} does not exist")
                raise FileNotFoundError(f"Scratchpad file {file_path} does not exist")

        # Create and return assistant
        return cls(logger, session_id), typer_file, scratchpad

    def build_prompt(
        self, typer_file: str, scratchpad: str, context_files: List[str], prompt_text: str
    ) -> str:
        """Build and format the prompt template with current state"""
        try:
            # Load typer file
            self.logger.info("📂 Loading typer file...")
            with open(typer_file, "r") as f:
                typer_content = f.read()

            # Load scratchpad file
            self.logger.info("📝 Loading scratchpad file...")
            if not os.path.exists(scratchpad):
                self.logger.error(f"📄 Scratchpad file {scratchpad} does not exist")
                raise FileNotFoundError(f"Scratchpad file {scratchpad} does not exist")

            with open(scratchpad, "r") as f:
                scratchpad_content = f.read()

            # Load context files
            context_content = ""
            for file_path in context_files:
                if not os.path.exists(file_path):
                    self.logger.error(f"📄 Context file {file_path} does not exist")
                    raise FileNotFoundError(f"Context file {file_path} does not exist")

                with open(file_path, "r") as f:
                    file_content = f.read()
                    file_name = os.path.basename(file_path)
                    context_content += f'\t<context name="{file_name}">\n{file_content}\n</context>\n\n'

            # Load and format prompt template
            self.logger.info("📝 Loading prompt template...")
            with open("prompts/typer-commands.xml", "r") as f:
                prompt_template = f.read()

            # Replace template placeholders
            formatted_prompt = (
                prompt_template.replace("{{typer-commands}}", typer_content)
                .replace("{{scratch_pad}}", scratchpad_content)
                .replace("{{context_files}}", context_content)
                .replace("{{natural_language_request}}", prompt_text)
            )

            # Log the filled prompt template to file only (not stdout)
            with open(self.log_file, "a") as log:
                log.write("\n📝 Filled prompt template:\n")
                log.write(formatted_prompt)
                log.write("\n\n")

            return formatted_prompt

        except Exception as e:
            self.logger.error(f"❌ Error building prompt: {str(e)}")
            raise

    def process_text(self, text: str, typer_file: str, scratchpad: str, context_files: List[str], mode: str) -> str:
        """Process text input and handle based on execution mode"""
        try:
            # Build fresh prompt with current state
            formatted_prompt = self.build_prompt(typer_file, scratchpad, context_files, text)
            
            # Generate command using DeepSeek
            self.logger.info("🤖 Processing text with DeepSeek...")
            prefix = f"python {typer_file}"
            command = prefix_prompt(prompt=formatted_prompt, prefix=prefix)

            if command == prefix.strip():
                self.logger.info(f"🤖 Command not found for '{text}'")
                self.speak("I couldn't find that command")
                return "Command not found"

            # Handle different modes
            assistant_name = get_config("typer_assistant.assistant_name")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if mode == "default":
                result = f"---\n{command}\n---"
                append_text = f"\n\n{timestamp} - {assistant_name} generated:\n{result}"
                with open(scratchpad, "a") as f:
                    f.write(append_text)
                return result

            elif mode == "execute":
                self.logger.info(f"⚡ Executing command: `{command}`")
                output = execute_uv_python(command, typer_file)
                
                result = f"---\n{command}\n{output}\n---"
                append_text = f"\n\n{timestamp} - {assistant_name} executed and generated:\n{result}"
                with open(scratchpad, "a") as f:
                    f.write(append_text)
                return output

            elif mode == "execute-no-scratch":
                self.logger.info(f"⚡ Executing command: `{command}`")
                output = execute_uv_python(command, typer_file)
                return output

            else:
                raise ValueError(f"Invalid mode: {mode}")

        except Exception as e:
            self.logger.error(f"❌ Error occurred: {str(e)}")
            raise

    def deep(
        self,
        typer_file: str,
        scratchpad: List[str],
        prompt_text: str,
        session_id: str,
    ) -> str:
        """Execute the deep command logic"""
        log_file = build_file_name_session("session.log", session_id)

        try:
            # Load typer file
            self.logger.info("📂 Loading typer file...")
            with open(typer_file, "r") as f:
                typer_content = f.read()

            # Load all scratchpad files
            self.logger.info("📝 Loading scratchpad files...")
            scratchpad_content = ""
            for file_path in scratchpad:
                if not os.path.exists(file_path):
                    self.logger.error(f"📄 Scratchpad file {file_path} does not exist")
                    raise FileNotFoundError(
                        f"Scratchpad file {file_path} does not exist"
                    )

                with open(file_path, "r") as f:
                    file_content = f.read()
                    file_name = os.path.basename(file_path)
                    scratchpad_content += f'<scratchpad name="{file_name}">\n{file_content}\n</scratchpad>\n\n'

            # Load and format prompt template
            self.logger.info("📝 Loading prompt template...")
            with open("prompts/typer-commands.xml", "r") as f:
                prompt_template = f.read()

            # Replace template placeholders
            formatted_prompt = (
                prompt_template.replace("{{typer-commands}}", typer_content)
                .replace("{{scratch_pad}}", scratchpad_content)
                .replace("{{natural_language_request}}", prompt_text)
            )

            # Log the filled prompt template to file only (not stdout)
            with open(log_file, "a") as log:
                log.write("\n📝 Filled prompt template:\n")
                log.write(formatted_prompt)
                log.write("\n\n")

            # Generate command using DeepSeek
            self.logger.info("🤖 Generating command with DeepSeek...")
            command = prefix_prompt(
                prompt=formatted_prompt, prefix=f"python {typer_file}"
            )
            self.logger.info(f"💡 Generated command: `{command}`")

            # Execute the generated command
            self.logger.info(f"⚡ Executing command: `{command}`")
            output = execute_uv_python(command, typer_file)

            # Print and log results
            self.logger.info("✅ Command execution completed successfully")
            self.logger.info(f"📄 Output:\n{output}")

            return output

        except Exception as e:
            self.logger.error(f"❌ Error occurred: {str(e)}")
            raise

    def think_speak(self, text: str):
        response_prompt_base = ""
        with open("prompts/concise-assistant-response.xml", "r") as f:
            response_prompt_base = f.read()

        assistant_name = get_config("typer_assistant.assistant_name")
        human_companion_name = get_config("typer_assistant.human_companion_name")

        response_prompt = response_prompt_base.replace("{{latest_action}}", text)
        response_prompt = response_prompt.replace(
            "{{human_companion_name}}", human_companion_name
        )
        response_prompt = response_prompt.replace(
            "{{personal_ai_assistant_name}}", assistant_name
        )
        prompt_prefix = f"Your Conversational Response: "
        response = prefix_prompt(
            prompt=response_prompt, prefix=prompt_prefix, no_prefix=True
        )
        self.logger.info(f"🤖 Response: '{response}'")
        self.speak(response)

    def speak(self, text: str):

        start_time = time.time()
        model = "eleven_flash_v2_5"
        # model="eleven_flash_v2"
        # model = "eleven_turbo_v2"
        # model = "eleven_turbo_v2_5"
        # model="eleven_multilingual_v2"
        voice = get_config("typer_assistant.elevenlabs_voice")

        audio_generator = self.elevenlabs_client.generate(
            text=text,
            voice=voice,
            model=model,
            stream=False,
        )
        audio_bytes = b"".join(list(audio_generator))
        duration = time.time() - start_time
        self.logger.info(f"Model {model} completed tts in {duration:.2f} seconds")
        play(audio_bytes)
