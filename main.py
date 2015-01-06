## keeping track of outside collaborators to COS projects

import os

import github3
from gdata.spreadsheet.service import SpreadsheetsService


USER = 'CenterForOpenScience'
TOKEN = os.environ['GITHUB_TOKEN']
DOC_KEY = '1w-WuKwE_8lSa4iSSUc5s39381Da3BpiGhyTbFp9PrVo'
COL_ROW_NAME = 'githubids'


def get_repos():
    ''' returns a github iterator object with a list of
    repos that are from the user specified '''

    gh = github3.GitHub(token=TOKEN)
    repos = gh.iter_user_repos(USER)

    return repos


def get_cos_contributors():
    ''' returns a list of contribtors from a google spreadsheet 
    specified by spreadsheet ID '''

    client = SpreadsheetsService()

    feed = client.GetWorksheetsFeed(DOC_KEY, visibility='public', wksht_id='1')
    sheet_key = feed.id.text.rsplit('/',1)[1]

    list_of_rows = client.GetListFeed(DOC_KEY, sheet_key, visibility='public').entry

    cos_users = []
    for row in list_of_rows:
        row_dict = row.custom
        cos_users.append(row_dict[COL_ROW_NAME].text)

    return cos_users
    

def get_non_cos_contributors():
    ''' returns a list of contributors that aren't in the COS spreadsheet 
    but have contributed to COS projects on github '''

    cos_repos = get_repos()
    cos_contributors = get_cos_contributors()
    non_cos_contributors = []
    non_cos_names = []
    for repo in cos_repos:
        print repo
        contributors =  repo.iter_contributors()
        for person in contributors:
            if str(person) not in cos_contributors:
                non_cos_contributors.append(str(person))
                non_cos_names.append(person.name)

    return list(set(non_cos_contributors)), list(set(non_cos_names))


if __name__ == "__main__":
    non_cos_contributor_usernames, names = get_non_cos_contributors()
    print 'Here are the {} Non-COS Contributors: '.format(str(len(non_cos_contributor_usernames)))
    print non_cos_contributor_usernames
    print names
