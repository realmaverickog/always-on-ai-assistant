import datetime
import json
import os
from typing import Union, Dict, List
import uuid

OUTPUT_DIR = "output"


def build_file_path(name: str):
    session_dir = f"{OUTPUT_DIR}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def build_file_name_session(name: str, session_id: str):
    session_dir = f"{OUTPUT_DIR}/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def to_json_file_pretty(name: str, content: Union[Dict, List]):
    def default_serializer(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    with open(f"{name}.json", "w") as outfile:
        json.dump(content, outfile, indent=2, default=default_serializer)


def current_date_time_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def current_date_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def dict_item_diff_by_set(
    previous_list: List[Dict], current_list: List[Dict], set_key: str
) -> List[str]:
    previous_set = {item[set_key] for item in previous_list}
    current_set = {item[set_key] for item in current_list}
    return list(current_set - previous_set)


def create_session_logger_id() -> str:
    return (
        datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    )


import logging
import sys


def setup_logging(session_id: str):
    """Configure logging with session-specific log file and stdout"""
    log_file = build_file_name_session("session.log", session_id)
    
    # Create a new logger specific to our application
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter with emoji mapping
    class EmojiFormatter(logging.Formatter):
        EMOJI_MAP = {
            logging.INFO: "ℹ️",
            logging.WARNING: "⚠️",
            logging.ERROR: "❌",
            logging.CRITICAL: "🔥",
            logging.DEBUG: "🐛"
        }
        
        def format(self, record):
            # Skip stdout for messages with skip_stdout flag
            if hasattr(record, 'skip_stdout') and record.skip_stdout:
                return ""
                
            emoji = self.EMOJI_MAP.get(record.levelno, "📝")
            self._style._fmt = f"{emoji} %(asctime)s - %(levelname)s - %(message)s"
            return super().format(record)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(EmojiFormatter())
    
    # Create stdout handler with filter
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_formatter = EmojiFormatter()
    stdout_handler.setFormatter(stdout_formatter)
    
    # Add filter to skip messages with skip_stdout flag
    stdout_handler.addFilter(lambda record: not getattr(record, 'skip_stdout', False))
    
    # Add both handlers
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    
    return logger


def parse_markdown_backticks(str) -> str:
    if "```" not in str:
        return str.strip()
    # Remove opening backticks and language identifier
    str = str.split("```", 1)[-1].split("\n", 1)[-1]
    # Remove closing backticks
    str = str.rsplit("```", 1)[0]
    # Remove any leading or trailing whitespace
    return str.strip()
