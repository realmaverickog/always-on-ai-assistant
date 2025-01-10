# Deepseek AI Assistant
> A powerful typer based Deepseek AI Assistant you can use to engineer TODAY.

## Setup
- `cp .env.sample .env`
  - Update with your keys
- `uv sync`


## Assistant Architecture
- 🧠 Brain: `Deepseek V3`
- 📝 Job (Prompt(s)): `prompts/typer-commands.xml`
- 💻 Active Memory (Dynamic Variables): `scratchpad.txt` + `commands/template.py`
- 👂 Ears (STT): `OpenAI Whisper v3` 
- 🎤 Mouth (TTS): `ElevenLabs Turbo`


## Commands

### Assistant Conversational Commands

```bash
python main_stt.py deep --typer-file commands/template.py --scratchpad scratchpad.txt
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
- [] add minimal mouth (TTS) to summarize what was done (no need for brain here just a simple conversational, short summary)
- [] add a minimal barebones stt, brain, tts personal ai assistant.
- [defer] add previous command map history. 1. 'deep go ahead and backup the db' -> 'backup-data db/'\n2. '...'
  - this lets us say refer to previous commands.

## Resources
- LOCAL SPEECH TO TEXT: https://github.com/KoljaB/RealtimeSTT
- faster whisper (support for RealtimeSTT) https://github.com/SYSTRAN/faster-whisper
- examples https://github.com/KoljaB/RealtimeSTT/blob/master/tests/realtimestt_speechendpoint_binary_classified.py