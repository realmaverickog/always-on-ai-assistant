# Deepseek AI Assistant
> A powerful typer based Deepseek AI Assistant you can use to engineer TODAY.

## Setup
- `cp .env.sample .env`
  - Update with your keys `DEEPSEEK_API_KEY` and `ELEVEN_API_KEY`
- `uv sync`
- (optional) install python 3.11 (`uv python install 3.11`)


## Assistant Architecture

### Typer Assistant
> See `assistant_config.yml` for more details.
- 🧠 Brain: `Deepseek V3`
- 📝 Job (Prompt(s)): `prompts/typer-commands.xml`
- 💻 Active Memory (Dynamic Variables): `scratchpad.txt`
- 👂 Ears (STT): `RealtimeSTT`
- 🎤 Mouth (TTS): `ElevenLabs`

### Base Assistant
> See `assistant_config.yml` for more details.
- 🧠 Brain: `Deepseek V3`
- 📝 Job (Prompt(s)): `None`
- 💻 Active Memory (Dynamic Variables): `scratchpad.txt`
- 👂 Ears (STT): `RealtimeSTT`
- 🎤 Mouth (TTS): `RealtimeTTS`


## Commands

### Base Assistant Chat Interface

Start a conversational chat session with the base assistant:

```bash
uv run python main_base_assistant.py chat
```

This will start an interactive chat session where you can:
- Type messages to the assistant
- Get spoken responses using TTS
- Type 'exit' or 'quit' to end the session
- Use Ctrl+C to gracefully exit

The base assistant features:
- 🧠 Brain: Deepseek V3
- 🎤 Mouth: System TTS (can be replaced with Azure/11Labs)
- 📝 Memory: Maintains full conversation history
- 📊 Logging: Detailed session logs in output/ directory

### Typer Assistant Conversational Commands

```bash
# in a python env
python main_typer_assistant.py awaken --typer-file commands/template.py --scratchpad scratchpad.md --mode execute

# raw
uv run python main_typer_assistant.py awaken --typer-file commands/template.py --scratchpad scratchpad.md --mode execute
```

### One shot shell commands
> These commands mirror a single text command to the Deepseek AI Assistant, execute it and returns the output of the command.

```bash
# Basic commands
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "Ping the server"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "Ping the server be sure to wait"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "show config verbose"

# User management
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "new user for tim role is admin"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "delete user 12345 --confirm"

# File operations
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "backup data from db/ dir"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "download file from http://test.com output to sessions dir retry 8 times"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "upload changes to our source_dir"

# Logs and debugging
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "search logs for 'focus cat off re john' case sensitive"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "summarize logs from /var/logs lines=500"

# Data operations
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "filter records from users.csv query='active=true' limit=100"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "transform data input.csv format=json columns=name,email"

# System operations
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "health check auth_service timeout=60 alert"
python main.py deep --typer-file commands/template.py --scratchpad scratchpad.txt --prompt "sync remotes production --force"
```



## Improvements
- [x] add arbitrary 'scratchpad' files (make it a list)
- [x] add ears (STT)
- [x] add minimal mouth (TTS) to summarize what was done (no need for brain here just a simple conversational, short summary)
- [] add a minimal barebones stt, brain, tts personal ai assistant.
- [defer] add previous command map history. 1. 'deep go ahead and backup the db' -> 'backup-data db/'\n2. '...'
  - this lets us say refer to previous commands.

## Resources
- LOCAL SPEECH TO TEXT: https://github.com/KoljaB/RealtimeSTT
- faster whisper (support for RealtimeSTT) https://github.com/SYSTRAN/faster-whisper
- examples https://github.com/KoljaB/RealtimeSTT/blob/master/tests/realtimestt_speechendpoint_binary_classified.py
- elevenlabs voice models: https://elevenlabs.io/docs/developer-guides/models#older-models