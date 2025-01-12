# Personal AI Assistant Scratchpad

## Ada Executed Command (2025-01-11 13:31:51)

> Request: Ada, list users that are viewers.

**Ada's Command:** 
```bash
uv run python commands/template.py list-users --role viewer
```

**Output:** 
```
Users:
- Tim (Role: viewer, Created: 2025-01-11T11:10:00.857285)
- user_11 (Role: viewer, Created: 2025-01-11T10:14:21.118499)
- user_17 (Role: viewer, Created: 2025-01-11T10:14:21.118514)
- user_21 (Role: viewer, Created: 2025-01-11T10:14:21.118524)
- user_22 (Role: viewer, Created: 2025-01-11T10:14:21.118526)
- user_4 (Role: viewer, Created: 2025-01-11T10:14:21.118476)
- user_9 (Role: viewer, Created: 2025-01-11T10:14:21.118494)

```

## Update User Block

### Create User Block
Alex - viewer
Mary - editor
Steve - admin

### Delete User Block
user_11
user_22
user_4

## Ada Executed Command (2025-01-11 13:34:50)

> Request: Ada, go ahead and look at the update user block and run the respective create user and delete user commands.

**Ada's Command:** 
```bash
uv run python commands/template.py create-user Alex --role viewer && uv run python commands/template.py create-user Mary --role editor && uv run python commands/template.py create-user Steve --role admin && uv run python commands/template.py delete-user user_11 --confirm && uv run python commands/template.py delete-user user_22 --confirm && uv run python commands/template.py delete-user user_4 --confirm
```

**Output:** 
```
User 'Alex' created with role 'viewer'.
User 'Mary' created with role 'editor'.
User 'Steve' created with role 'admin'.
No user found with ID user_11.
No user found with ID user_22.
No user found with ID user_4.
```

## Ada Executed Command (2025-01-11 13:35:51)

> Request: Okay, so let's check this out. So this is really cool, right? So she created the command. She created this giant execution statement and we got a couple of outputs here. We have, you know, our creatives, our creative commands and then we also have our delete commands that failed. So something went wrong here and I think it's because let me look at exactly how this delete user works. user ID might just be a single ID. So yeah, that looks right. So what I'm going to do is I'm just going to ask Ada to correct this for us, right? So I'll say Ada, rerun the delete commands, but only use the actual user ID. So not the user underscore prefix. Just use the numbers for the deletion.

**Ada's Command:** 
```bash
uv run python commands/template.py delete-user 11 --confirm && uv run python commands/template.py delete-user 22 --confirm && uv run python commands/template.py delete-user 4 --confirm
```

**Output:** 
```
User with ID 11 deleted.
User with ID 22 deleted.
User with ID 4 deleted.
```

## Ada Executed Command (2025-01-11 13:43:27)

> Request: Get some content here for Ada to transcribe for a personal AI assistant to transcribe. It's coming in the ears, which is powered by real-time speech-to-text. And then if we pause for a moment, the transcription process will actually kick off. And notice how much slower this is than our previous executions.

**Ada's Command:** 
```bash
uv run python commands/template.py list-users --role viewer
```

**Output:** 
```
Users:
- Alex (Role: viewer, Created: 2025-01-11T13:34:50.762624)
- Tim (Role: viewer, Created: 2025-01-11T11:10:00.857285)
- user_11 (Role: viewer, Created: 2025-01-11T10:14:21.118499)
- user_17 (Role: viewer, Created: 2025-01-11T10:14:21.118514)
- user_22 (Role: viewer, Created: 2025-01-11T10:14:21.118526)
- user_4 (Role: viewer, Created: 2025-01-11T10:14:21.118476)
- user_9 (Role: viewer, Created: 2025-01-11T10:14:21.118494)

```

## Ada Executed Command (2025-01-12 12:39:28)

> Request: ADA, ping the server.

**Ada's Command:** 
```bash
uv run python commands/template.py ping-server
```

**Output:** 
```
Server pinged. Response time: 276 ms.
```

## Ada Executed Command (2025-01-12 12:46:24)

> Request: Hello, ADA, ping the server, wait for a response.

**Ada's Command:** 
```bash
uv run python commands/template.py ping-server --wait
```

**Output:** 
```
Server pinged. Response time: 211 ms. (Waited for a response.)
```