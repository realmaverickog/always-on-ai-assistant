from RealtimeSTT import AudioToTextRecorder
from modules.typer_assistant import TyperAssistant
from modules.utils import create_session_logger_id, setup_logging
import logging
import typer
from typing import List
import os

app = typer.Typer()

@app.command()
def stt(
    typer_file: str = typer.Option(
        ..., "--typer-file", "-f", help="Path to typer commands file"
    ),
    scratchpad: List[str] = typer.Option(
        ..., "--scratchpad", "-s", help="List of scratchpad files"
    ),
):
    """Run STT interface that processes speech into typer commands"""
    assistant, typer_file, scratchpad = TyperAssistant.build_assistant(typer_file, scratchpad)
    
    print("🎤 Speak now... (press Ctrl+C to exit)")
    recorder = AudioToTextRecorder()

    def process_text(text):
        print(f"\n🎤 Heard: {text}")
        try:
            output = assistant.process_text(text, typer_file, scratchpad)
            print(f"🤖 Response:\n{output}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    while True:
        recorder.text(process_text)

if __name__ == "__main__":
    app()
