#!/env/python

import json
import requests

import configuration


HEADERS = {'Authorization':'token %s' % configuration.git_token}
URL = "https://api.github.com/%s/repos" % configuration.git_name

def create_repo(repo_name):
    """
    Creates repo in git if repo with name has not already exist.
    Repo name is mandatory. All other repo options are set automaticky just for HW.

    @param repo_name: desired name of repository

    """
    post_data = json.dumps({'name':repo_name, 'private':False})
    req = requests.post(URL, post_data, headers=HEADERS)
    req.raise_for_status()


