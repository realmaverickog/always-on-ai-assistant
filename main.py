from modules.data_types import MockDataType
from modules.deepseek import prefix_prompt
from modules.execute_python import execute_uv_python
from modules.utils import create_session_logger_id, build_file_name_session
import typer
import logging
import os

app = typer.Typer()

def setup_logging(session_id: str):
    """Configure logging with session-specific log file"""
    log_file = build_file_name_session("session.log", session_id)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

@app.command()
def main(
    typer_file: str = typer.Argument(..., help="Path to typer commands file"),
    scratchpad: str = typer.Argument(..., help="Path to scratchpad file"),
    prompt_text: str = typer.Argument(..., help="Prompt text"),
):
    # Create session ID and setup logging
    session_id = create_session_logger_id()
    setup_logging(session_id)
    logging.info(f"Starting session {session_id}")
    
    try:
        # Load files
        logging.info("Loading files...")
        with open(typer_file, "r") as f:
            typer_content = f.read()
        with open(scratchpad, "r") as f:
            scratchpad_content = f.read()
        
        # Load and format prompt template
        logging.info("Loading prompt template...")
        with open("prompts/typer-commands.xml", "r") as f:
            prompt_template = f.read()
        
        # Replace template placeholders
        formatted_prompt = prompt_template.replace("{{typer-commands}}", typer_content)\
                                         .replace("{{scratch_pad}}", scratchpad_content)\
                                         .replace("{{natural_language_request}}", prompt_text)
        
        # Generate command using DeepSeek
        logging.info("Generating command with DeepSeek...")
        command = prefix_prompt(
            prompt=formatted_prompt,
            prefix=f"python {typer_file} "
        )
        
        # Execute the generated command
        logging.info(f"Executing command: {command}")
        output = execute_uv_python(command, typer_file)
        
        # Print and log results
        print(output)
        logging.info("Command execution completed successfully")
        logging.info(f"Output:\n{output}")
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    app()
