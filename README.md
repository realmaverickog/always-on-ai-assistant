# Deepseek AI Assistant
> A powerful typer based Deepseek AI Assistant you can use to engineer TODAY.

## Setup
- `cp .env.sample .env`
  - Update with your keys
- `uv sync`

## Commands
```bash
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "Ping the server"
```

## Assistant Architecture
- 🧠 Brain: `Deepseek V3`
- 📝 Job (Prompt(s)): `prompts/typer-commands.xml`
- 💻 Active Memory (Dynamic Variables): `scratchpad.txt` + `commands/template.py`
- 👂 Ears (STT): `OpenAI Whisper v3` 
- 🎤 Mouth (TTS): `ElevenLabs Turbo`

## Improvements
- [] add arbitrary 'scratchpad' files (make it a list)
- [] add ears (STT)
- [] add mouth (TTS)