# MicroCurrency

A discord bot that allows currency control/trades/exchanges within micronations.

# To-Do:
- [ ] Remove inconsistencies
- [ ] Polish commands in order for them to be nicely formatted in embeds
- [ ] Make command names better
- [ ] API documentation

# How to install

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

# How to run
To run the bot, you just need to run `poetry run bot`.

If you would like to create money for a currency, use `poetry run create_money`.
If you would like to view all transactions, use `poetry run get_transactions`.
Please view the `pyproject.toml` file to see any other undocumented dev scripts.

# Would you like to contribute?

We are always accepting pull requests and we will listen to suggestions.
If you have a question, suggestion or issue, please make a [github issue](https://github.com/CrescentFlower-Inc/MicroCurrency/issues) or join our [discord support server](https://discord.gg/5qarCfy5de).
