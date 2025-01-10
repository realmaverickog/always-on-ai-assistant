from RealtimeSTT import AudioToTextRecorder
from typing import List
from modules.base_assistant import PlainAssistant
from modules.utils import create_session_logger_id, setup_logging
import typer
import logging

app = typer.Typer()


@app.command()
def ping():
    print("pong")


@app.command()
def chat():
    """Start a chat session with the plain assistant using speech input"""
    # Create session and logging
    session_id = create_session_logger_id()
    logger = setup_logging(session_id)
    logger.info(f"🚀 Starting chat session {session_id}")

    # Create assistant
    assistant = PlainAssistant(logger, session_id)

    # Configure STT recorder
    recorder = AudioToTextRecorder(
        spinner=True,
        compute_type="float32",
        model="tiny.en",
        language="en",
        print_transcription_time=True,
    )

    def process_text(text):
        """Process user speech input"""
        try:
            logger.info(f"🎤 Heard: {text}")

            # Check for exit commands
            if text.lower() in ["exit", "quit"]:
                logger.info("👋 Exiting chat session")
                return False

            # Process input and get response
            response = assistant.process_text(text)
            logger.info(f"🤖 Response: {response}")

            return True

        except Exception as e:
            logger.error(f"❌ Error occurred: {str(e)}")
            raise

    try:
        print("🎤 Speak now... (say 'exit' or 'quit' to end)")
        while True:
            recorder.text(process_text)

    except KeyboardInterrupt:
        logger.info("👋 Session ended by user")
    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    app()
