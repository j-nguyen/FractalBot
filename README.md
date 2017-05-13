# FractalBot

[![Build Status](https://travis-ci.org/j-nguyen/FractalBot.svg?branch=staging)](https://travis-ci.org/j-nguyen/FractalBot) [![Discord](https://discordapp.com/api/guilds/267645106377457665/widget.png)](https://discord.gg/uzNg2uH)

A multi-purpose discord bot that is designed to several tasks. Some tasks include, but not limited to: overwatch/cs:go stats, moderation management, and fun commands.

This bot's purpose is to help manage your server in Discord. Feel free to add in any requests you'd like.

## Requirements

* Python 3.5
* `aiohttp` library
* `websockets` library
* `discord` library

## Installing

You will need to the install the discord library

`$ python3 -m pip install -U discord.py`

Afterwards, you'll need to configure `config.json` for to direct to your token and client id. (You may use mine I guess, but I prefer you not to. Discord has it for free)

```json
{
	"token": "",
	"client_id": "",
	"mod_log": ""
}
```

Finally, execute by doing:

`$ python bot.py`

## Credits

* https://github.com/Rapptz/discord.py

## Author

* Johnny Nguyen (j-nguyen)

## License

[Apache License](https://github.com/j-nguyen/FractalBot/blob/master/LICENSE)
