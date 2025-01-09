from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)


def prompt(prompt: str, model: str = "deepseek-chat") -> str:
    """
    Send a prompt to DeepSeek and get detailed benchmarking response.
    """
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}], stream=False
    )
    return response.choices[0].message.content


def fill_in_the_middle_prompt(
    prompt: str, suffix: str, model: str = "deepseek-chat"
) -> str:
    """
    Send a fill-in-the-middle prompt to DeepSeek and get response.

    example:
        prompt="def fib(a):",
        suffix="    return fib(a-1) + fib(a-2)",
    """
    response = client.completions.create(model=model, prompt=prompt, suffix=suffix)
    return response.choices[0].text


def json_prompt(prompt: str, model: str = "deepseek-chat") -> dict:
    """
    Send a prompt to DeepSeek and get JSON response.

    Args:
        prompt: The user prompt to send
        system_prompt: Optional system prompt to set context
        model: The model to use, defaults to deepseek-chat

    Returns:
        dict: The parsed JSON response
    """
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model, messages=messages, response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def prefix_prompt(prompt: str, prefix: str, model: str = "deepseek-chat") -> str:
    """
    Send a prompt to DeepSeek with a prefix constraint and get response.

    Args:
        prompt: The user prompt to send
        prefix: The required prefix for the response
        model: The model to use, defaults to deepseek-chat

    Returns:
        str: The model's response constrained by the prefix
    """
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": prefix, "prefix": True},
    ]

    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def prefix_suffix_prompt(
    prompt: str, prefix: str, suffix: str, model: str = "deepseek-chat"
) -> str:
    """
    Send a prompt to DeepSeek with a prefix and suffix constraint and get response.

    Args:
        prompt: The user prompt to send
        prefix: The required prefix for the response
        suffix: The required suffix for the response
        model: The model to use, defaults to deepseek-chat

    Returns:
        str: The model's response constrained by the prefix and suffix
    """
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": prefix, "prefix": True},
    ]
    response = client.chat.completions.create(
        model=model, messages=messages, stop=[suffix]
    )
    return response.choices[0].message.content
