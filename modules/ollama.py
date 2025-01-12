from ollama import chat
from typing import List, Dict


def conversational_prompt(
    messages: List[Dict[str, str]],
    system_prompt: str = "You are a helpful conversational assistant. Respond in a short, concise, friendly manner.",
    model: str = "phi4",
) -> str:
    """
    Send a conversational prompt to Ollama with message history.

    Args:
        messages: List of message dicts with 'role' and 'content' keys
        system_prompt: Optional system prompt to set context
        model: The model to use, defaults to llama2

    Returns:
        str: The model's response
    """
    try:
        # Add system prompt as first message
        full_messages = [{"role": "system", "content": system_prompt}, *messages]

        response = chat(
            model=model,
            messages=full_messages,
        )
        return response.message.content

    except Exception as e:
        raise Exception(f"Error in conversational prompt: {str(e)}")
