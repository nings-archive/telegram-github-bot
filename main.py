#! /usr/bin/env python3
''' quick and dirty bot to facillitate usp does aoc '''

import json, telegram
from github import Github
from telegram import Bot
from config import *

# Initialisation for github api, telgeram api, and dict repositories
JSON_PATH = './commit_history.json'
with open(JSON_PATH, 'r') as file:
    repositories = json.loads(file.read())
github_api = Github(login_or_token=github_api_token)
telegram_api = Bot(token=telegram_api_token)

new_updates = {}

# iterate through all commits polled from github_api, then
# if the commit is new, i.e. not in commit_hist
#   (i)  add to new_updates 
#   (ii) add to commit_hist
for repo, commit_hist in repositories.items():
    print(repo)
    all_commits = [ c.commit for c in github_api.get_repo(repo).get_commits() ] 
    new_updates[repo] = []
    for commit in all_commits:
        if commit.sha not in commit_hist:
            new_updates[repo].append(commit)
            commit_hist.append(commit.sha)

# construct the update message
update_message = ''
for repo, new_commits in new_updates.items():
    if len(new_commits) != 0:
        update_message += '*{}*\n{}\n'
            .format(repo, 'https://github.com/'+repo)
        for commit in new_commits:
            try:
                update_message += '  {}\n'.format(
                    commit.message.split('\n')[0]
                        .replace('*', '')
                        .replace('_', '')
                        .replace('`', '')
                )
            except IndexError:
                # ...for empty commit messages
                # git gud pls have a commit message
                pass

# send message only if there has been updates (update_message is non-empty)
if update_message != '':
    telegram_api.send_message(
        chat_id=aoc_chat_id,
        text=update_message,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

# finally, update the commit_history json file
with open(JSON_PATH, 'w') as file:
    file.write(json.dumps(repositories, indent=4))
