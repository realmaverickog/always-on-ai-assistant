from typing import List
from modules.data_types import MockDataType
from modules.typer_assistant import TyperAssistant
from modules.utils import (
    create_session_logger_id,
    setup_logging,
)
import typer
import logging
import os

app = typer.Typer()


@app.command()
def ping():
    print("pong")


@app.command()
def deep(
    typer_file: str = typer.Option(
        ..., "--typer-file", "-f", help="Path to typer commands file"
    ),
    scratchpad: List[str] = typer.Option(
        ..., "--scratchpad", "-s", help="List of scratchpad files"
    ),
    prompt_text: str = typer.Option(..., "--prompt", "-p", help="Prompt text"),
):
    # Create session ID and setup logging
    session_id = create_session_logger_id()
    logger = setup_logging(session_id)
    logger.info(f"🚀 Starting session {session_id}")

    # ensure both files exist
    if not os.path.exists(typer_file):
        logger.error(f"📂 Typer file {typer_file} does not exist")
        raise typer.Exit(1)
    
    # Check each scratchpad file individually
    for file_path in scratchpad:
        if not os.path.exists(file_path):
            logger.error(f"📄 Scratchpad file {file_path} does not exist")
            raise typer.Exit(1)

    # Create and use TyperAssistant
    assistant = TyperAssistant(logger)
    return assistant.deep(typer_file, scratchpad, prompt_text, session_id)


if __name__ == "__main__":
    app()


if __name__ == "__main__":
    app()
