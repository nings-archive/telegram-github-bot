#! /usr/bin/env python3
''' quick and dirty bot to facillitate usp does aoc '''

import json, telegram
from github import Github
from telegram import Bot
from config import *
from config import \
    GIT_TOKEN, TELE_TOKEN, AOC_CHAT_ID, JSON_PATH, LEADERBOARD_CODE

# Initialisation for github api, telgeram api, and dict repositories
with open(JSON_PATH, 'r') as file:
    repositories = json.loads(file.read())
github_api = Github(login_or_token=GIT_TOKEN)
telegram_api = Bot(token=TELE_TOKEN)

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
update_message = '''\
<b>It's 1pm, a new puzzle is out!</b>\nhttps://adventofcode.com\n
'''
for repo, new_commits in new_updates.items():
    if len(new_commits) != 0:
        update_message += '<b>{}</b>\n{}\n'.format(
            repo, 'https://github.com/'+repo
        )
        for commit in new_commits:
            try:
                update_message += '  {}\n'.format(
                    commit.message.split('\n')[0]
                        .replace('>', '')  # lazy sanitise html #TODO regex
                )
            except IndexError:
                # ...for empty commit messages
                # git gud pls have a commit message
                pass

update_message += """\nJoin the our private leaderboard \
(http://adventofcode.com/2017/leaderboard/private) with the code {} \
to see everyone's progress so far!""".format(LEADERBOARD_CODE)

# send message
print(update_message)
telegram_api.send_message(
    chat_id=AOC_CHAT_ID,
    text=update_message,
    parse_mode=telegram.ParseMode.HTML
)

# finally, update the commit_history json file
with open(JSON_PATH, 'w') as file:
    file.write(json.dumps(repositories, indent=4))
