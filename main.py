from typing import List
from modules.data_types import MockDataType
from modules.deepseek import prefix_prompt
from modules.execute_python import execute_uv_python
from modules.utils import (
    create_session_logger_id,
    build_file_name_session,
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
    log_file = build_file_name_session("session.log", session_id)
    logger.info(f"📂 Session log file: {log_file}")
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

    try:
        # Load typer file
        logger.info("📂 Loading typer file...")
        with open(typer_file, "r") as f:
            typer_content = f.read()

        # Load all scratchpad files
        logger.info("📝 Loading scratchpad files...")
        scratchpad_content = ""
        for file_path in scratchpad:
            if not os.path.exists(file_path):
                logger.error(f"📄 Scratchpad file {file_path} does not exist")
                raise typer.Exit(1)
            
            with open(file_path, "r") as f:
                file_content = f.read()
                file_name = os.path.basename(file_path)
                scratchpad_content += f'<scratchpad name="{file_name}">\n{file_content}\n</scratchpad>\n\n'

        # Load and format prompt template
        logger.info("📝 Loading prompt template...")
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
        logger.info("🤖 Generating command with DeepSeek...")
        command = prefix_prompt(prompt=formatted_prompt, prefix=f"python {typer_file}")
        logger.info(f"💡 Generated command: `{command}`")

        # Execute the generated command
        logger.info(f"⚡ Executing command: `{command}`")
        output = execute_uv_python(command, typer_file)

        # Print and log results
        logger.info("✅ Command execution completed successfully")
        logger.info(f"📄 Output:\n{output}")

    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    app()
