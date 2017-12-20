#! /usr/bin/env python3

import re, json
from github import Github
from telegram import Bot, ParseMode
from config import (
    GIT_TOKEN, TELE_TOKEN, CHAT_ID, JSON_PATH, 
    UPDATE_HEADER, UPDATE_FOOTER, 
    ONLY_SEND_UPDATES, INCLUDE_AUTHOR
)

html_pattern = '<[^>]*>'

# Initialisation---repositories, github_api, telegram_api
with open(JSON_PATH, 'r') as file:
    repositories = json.loads(file.read())
github_api = Github(login_or_token=GIT_TOKEN)
telegram_api = Bot(token=TELE_TOKEN)

''' iterate through all commits polled from github_api, then
    if the commit is new, i.e. not in commit_hist
      (i)  add to new_updates 
      (ii) add to commit_hist '''
new_updates = {}
for repo, commit_hist in repositories.items():
    ''' .get_repo returns github.Repository.Repository
        .get_commits() returns 
            github.PaginatedList.PagniatedList<github.Commit.Commit>
        We want github.GitCommit.GitCommit, which are attributes of
            github.Commit.Commit with identifier 'commit', i.e.
            github_api.get_repo(repo).get_commits()[n].commit '''
    all_commits = [ 
        c.commit for c in github_api.get_repo(repo).get_commits() ] 
    new_updates[repo] = []
    for commit in all_commits:
        if commit.sha not in commit_hist:
            new_updates[repo].append(commit)  # to append to update_message
            commit_hist.append(commit.sha)  # to update the json file

# construct the update message
update_message = ''
for repo, new_commits in new_updates.items():
    has_new_commit = len(new_commits) != 0
    if has_new_commit:
        update_message += ('<b>{}</b>\n{}\n'
            .format(repo, 'https://github.com/'+repo))
        for commit in new_commits:
            try:
                sub_update_message = '  {}: {}\n'.format(
                    commit.author.name,
                    commit.message.splitlines()[0])
                 # sanitise for ParseMode.HTML
                sub_update_message = re.sub(
                    html_pattern, '', sub_update_message)
                update_message += sub_update_message
            except IndexError:
                ''' empty commit messages are empty strings,
                    splitlines() returns an empty list, and
                    accessing with [0] gives IndexError
                    ...this error has not been observed,
                    and hopefully never will '''
                pass

print(update_message)
# send message
has_update = not update_message is ''
if has_update or not ONLY_SEND_UPDATES:
    telegram_api.send_message(
        chat_id=CHAT_ID, parse_mode=ParseMode.HTML,
        text='{}\n\n{}\n\n{}'.format(UPDATE_HEADER, update_message, UPDATE_FOOTER)
    )

# finally, update the commit_history json file
with open(JSON_PATH, 'w') as file:
    file.write(json.dumps(repositories, indent=4))
