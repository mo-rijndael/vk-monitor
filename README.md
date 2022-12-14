# VK Tracker
This bot allows you to set rules, and get every single post in VKontakte, which match them. In real time. Under the hood uses [Streaming API](https://dev.vk.com/api/streaming/getting-started)

# Requirements
## Access token
To get full access to data, you should create "Standalone" app in VKontakte, and (important!) write to tech support, to unlock 100% data access. Without it, you'll get less than 1% of public data.
After approvment, use your app "service" token in `config.json`

## Python, pip, (optional) venv
3.7 and higher should work ig. Any modern enough distro has it. Some distros doesn't have venv module in python package, so you need to install something like "python3-venv".
But this is completely optional, you can use global package location

# Installation

## (optional) install and activate venv
`python3 -m venv venv && source ./venv/bin/activate`

## required libraries
This includes websocket, pydantic, and aiohttp
`pip3 install -r requirements.txt`

## configuration
Open config.example.json in <s>vim</s> your preferred text editor, and paste your tokens, chat\_ids and rules

## pushing your rules to vk server
`python3 bot.py --config config.example.json --overwrite`. This should delete all previously set rules and exit

## production!
`python3 bot.py --config config.example.json`

Pro tip: if you use supervisor like systemd for your services, instead of activating venv just replace `python3` with `/absolute/path/to/venv/bin/python3`. Python will load your venv automatically.
