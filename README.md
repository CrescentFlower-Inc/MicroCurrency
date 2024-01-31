# MicroCurrency

A discord bot that allows currency control/trades/exchanges within micronations.

# HOW TO INSTALL
~~This bot so far only works on linux. So if you are on windows, i recommend getting WSL or a virtual machine~~

Windows now works too i think!

To install this bot you need:

	- Atleast python 3.9 (but other versions probably would work too)
	- Poetry
	- Git


Once you have installed those things, run the following commands:
```bash
git clone https://github.com/CrescentFlower-Inc/MicroCurrency/
cd MicroCurrency
poetry install
```
Then also rename `config.json.example` back to `config.json` and configure your bot!

# HOW TO RUN
To run the bot, you just need to run `poetry run bot`.

If you would like to create money for a currency, use `poetry run create_money`.
