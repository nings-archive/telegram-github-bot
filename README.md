# Telegram-Github Bot
Telegram-Github Bot is a simple script that fetches new commits from a predefined list of github repositories, and pushes them to a telegram chat.

## Set-Up
First, install the dependencies,
```
$ sudo pip3 install -U python-telegram-bot PyGithub
```

Clone this repository (or fork it, if you want to make changes),
```
$ git clone https://github.com/ningyuansg/telegram-github-bot.git
```

Then, set-up the config and commit_history files.
1. Add the name of the repositories to track in `commit_history.json`
2. In `config.py`, add your [github access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/), [telegram bot token](https://core.telegram.org/bots#generating-an-authorization-token), the chat_id for the bot to post to, and the absolute path to the above `commit_history.json`.
3. The other variables are optional.

You may want to use the [convenience script provided](get_chat_id.py) to retrieve the chat_id. Run the script, then send any command to the bot through any chat, to get that chat's id.

## Contributing
If you have any features you'd like to add to the bot, feel free to create and maintain a fork or clone of this bot. This project is provided with no warranty, and you can do whatever you want.

However, please do not submit PRs for new features. Telegram-Github bot is meant to be a simple and minimal template with which you can built and customise upon. Rather, PRs should improve or optimise the current state of the project (see [issues](https://github.com/ningyuansg/telegram-github-bot/issues)).
