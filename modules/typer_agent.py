from typing import List
import os
import logging
from modules.utils import (
    build_file_name_session,
    create_session_logger_id,
    setup_logging,
)
from modules.deepseek import prefix_prompt
from modules.execute_python import execute_uv_python


class TyperAgent:
    def __init__(self, logger: logging.Logger, session_id: str):
        self.logger = logger
        self.session_id = session_id
        self.log_file = build_file_name_session("session.log", session_id)

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
        self, typer_file: str, scratchpad: List[str], prompt_text: str
    ) -> str:
        """Build and format the prompt template with current state"""
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
                    scratchpad_content += f'\t<scratchpad name="{file_name}">\n{file_content}\n</scratchpad>\n\n'

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
            with open(self.log_file, "a") as log:
                log.write("\n📝 Filled prompt template:\n")
                log.write(formatted_prompt)
                log.write("\n\n")

            return formatted_prompt

        except Exception as e:
            self.logger.error(f"❌ Error building prompt: {str(e)}")
            raise

    def process_text(self, text: str, typer_file: str, scratchpad: List[str]) -> str:
        """Process text input and execute as typer command"""
        try:
            # Build fresh prompt with current state
            formatted_prompt = self.build_prompt(typer_file, scratchpad, text)

            # Generate command using DeepSeek
            self.logger.info("🤖 Processing text with DeepSeek...")
            prefix = f"python {typer_file}"
            command = prefix_prompt(prompt=formatted_prompt, prefix=prefix)

            if command == prefix.strip():
                self.logger.info(f"🤖 Command not found for '{text}'")
                return "Command not found"

            # Execute the generated command
            self.logger.info(f"⚡ Executing command: `{command}`")
            output = execute_uv_python(command, typer_file)

            # Log results
            self.logger.info("✅ Command execution completed successfully")
            self.logger.info(f"📄 Output:\n{output}")

            return output

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

    def speak(self, text: str):
        """Speak the text"""
        print(text)
