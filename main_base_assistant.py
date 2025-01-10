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
    """Start a chat session with the plain assistant"""
    # Create session and logging
    session_id = create_session_logger_id()
    logger = setup_logging(session_id)
    logger.info(f"🚀 Starting chat session {session_id}")

    # Create assistant
    assistant = PlainAssistant(logger, session_id)

    try:
        while True:
            # Get user input
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            # Process input
            response = assistant.process_text(user_input)
            print(f"Assistant: {response}")

    except KeyboardInterrupt:
        logger.info("👋 Session ended by user")
    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    app()
