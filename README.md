# FractalBot

[![Build Status](https://travis-ci.org/j-nguyen/FractalBot.svg?branch=staging)](https://travis-ci.org/j-nguyen/FractalBot) [![license](https://img.shields.io/github/license/j-nguyen/fractalbot.svg)]() [![GitHub (pre-)release](https://img.shields.io/github/release/j-nguyen/fractalbot/all.svg)]() [![Discord](https://discordapp.com/api/guilds/267645106377457665/widget.png)](https://discord.gg/uzNg2uH) 

A multi-purpose discord bot that is designed to several tasks. Some tasks include, but not limited to: overwatch/cs:go stats, moderation management, and fun commands.

This bot's purpose is to help manage your server in Discord. Feel free to add in any requests you'd like.

## Requirements

* Python 3.5
* `aiohttp` library
* `websockets` library
* `discord` library
* `sqlalchemy` library
* `psycopg2` library

## Installing

You will need to the install the discord library, and the libraries listed above.

`$ python3 -m pip install -U discord.py`
`$ python3 -m pip install sqlalchemy`
`$ python3 -m pip install psycopg2`

### Config.json

Afterwards, you'll need to create a `config.json` for to direct to your token and client id. (You may use mine I guess, but I prefer you not to. Discord has it for free)

```json
{
  "token": "",
  "client_id": "",
  "mod_log": ""
}
```


### Database Configuration

You'll need to edit for the database configuration. Create `postgresql.json` on the current directory.

Here is an example:

```json
{
  "hostname": "localhost",
  "user": "",
  "password": "",
  "database": ""
}
```

Afterwards, finish run the setup py to create the tables.

`$ python setup.py`

Finally, execute by doing:

`$ python bot.py`

## Credits

* https://github.com/Rapptz/discord.py

## Author

* Johnny Nguyen (j-nguyen)

## License

[Apache License](https://github.com/j-nguyen/FractalBot/blob/master/LICENSE)
