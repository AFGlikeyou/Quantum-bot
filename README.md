# Quantum Bot

A Discord bot that copies text from a designated channel and reposts it when the `!key` command is used.

## Features

- Responds to `!key` command
- Fetches the latest message from "🔑〡mod-key" channel
- Posts the retrieved text in the channel where command was executed
- Role-based permissions (🎓〡Staff role required)
- Comprehensive error handling for missing channels or permissions
- Keep-alive system for 24/7 operation
- Detailed logging for debugging

## Setup

### Prerequisites

- Python 3.11 or higher
- Discord.py library
- python-dotenv library
- flask library

### Installation

1. Install required packages:
```bash
pip install discord.py python-dotenv flask
