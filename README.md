# Deepseek AI Assistant

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

## Setup

- `git remote remove origin`
- `git remote add origin <your-repo-url>`
- `cp .env.sample .env`
  - Update with your keys
- `uv sync`
- `uv run python main.py`
- Start AI Coding!

## Aider

- `cp .template.aider.conf.yml .aider.conf.yml`
  - Update to fit your needs

## PAIC tooling

### Specs

- `aider`
- `/editor`
- paste in your spec from `specs/`

### ADWs 

- `uv run python adw/adw_bump_version.template.py`
  - use this as a template for your own ADWs
  - review this before you use it

### Director

- `uv run python director.py --config spec/*.yaml`
  - use the `director_template.example.yaml` as a template for director configs
