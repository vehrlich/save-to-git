#!/env/python

import json
import requests
import base64
import argparse


class GitSaver(object):

    api_url = "https://api.github.com"

    def __init__(self, git_name, git_token, repo_name, repo_file_path, content):
        self.git_name = git_name
        self.git_token = git_token
        self.repo_name = repo_name
        self.repo_file_path = repo_file_path
        self.content = content
        self.headers = {'Authorization':'token %s' % git_token}

    def repo_exists(self):
        """
        Check if repo exists.

        @param repo_name: name of seeking repo
        @return True if repo exits. Otherwise False
        """
        # GET /repos/:owner/:repo
        url = "/".join([self.api_url, 'repos', self.git_name, self.repo_name])
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            return True
        elif req.status_code == 404:
            return False
        else:
            # others errors handled elsewhere
            return req.raise_for_status()

    def create_repo(self):
        """
        Creates repo in git if repo with name has not already exist.
        Repo name is mandatory. All other repo options are set automaticky just for HW.

        @param repo_name: desired name of repository

        """
        url = "/".join([self.api_url, 'user', 'repos'])
        post_data = json.dumps({'name':self.repo_name, 'private':False})
        req = requests.post(url, post_data, headers=self.headers)
        req.raise_for_status()


    def get_file(self):
        """
        Return file info from git. Return None if file does not exist.

        @return sha of file or None if doesn't exists
        """
        # GET /repos/:owner/:repo/contents/:path
        url = "/".join([self.api_url,
                        'repos',
                        self.git_name,
                        self.repo_name,
                        'contents',
                        self.repo_file_path])
        post_data = json.dumps({'path': self.repo_file_path})
        req = requests.get(url, post_data, headers=self.headers)
        if req.status_code == 200:
            return json.loads(req.content)['sha']
        else:
            return None


    def create_file(self):
        """
        Creates file on repo_file_path in repo_name.

        @return sha of file commit
        """
        # POST /repos/:owner/:repo/contents/:path
        url = "/".join([self.api_url,
                        'repos',
                        self.git_name,
                        self.repo_name,
                        'contents',
                        self.repo_file_path])
        post_data = json.dumps({'path': self.repo_file_path,
                                'message': 'created with faith',
                                'content': self.content})
        req = requests.put(url, post_data, headers=self.headers)
        req.raise_for_status()
        return json.loads(req.content)['commit']['sha']

    def update_file(self, sha):
        """
        Creates file on repo_file_path in repo_name.

        @return sha of file commit
        """
        # POST /repos/:owner/:repo/contents/:path
        url = "/".join([self.api_url,
                        'repos',
                        self.git_name,
                        self.repo_name,
                        'contents',
                        self.repo_file_path])
        post_data = json.dumps({'path': self.repo_file_path,
                                'message': 'updated with honor',
                                'content': self.content,
                                'sha':sha})
        req = requests.put(url, post_data, headers=self.headers)
        req.raise_for_status()
        return json.loads(req.content)['commit']['sha']


def main():
    """
    Parse input arguments, prepares them for Class.
    Checks if repo exists, creates one if not.
    Checks if file exists. Create new one if not, updatea otherwise.

    Returns commit hash
    """

    parser = argparse.ArgumentParser(prog='save_to_git.py',
                                     description="Saves file into GIT. If "\
                                                 "repository doesn't exist, "\
                                                 "creates it",
                                     usage="./save_to_git.py <owner> "\
                                           "<api_token> <local file path> "\
                                           "<reponame>/<file path>")
    parser.add_argument('owner',
                        help='owner of repo')
    parser.add_argument('api_token',
                        help='authorized API token')
    parser.add_argument('local_file_path',
                        help='file to commit')
    parser.add_argument('repo_file_path',
                        help='reponame and path where to commit')

    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    #open file, read it, encode it
    try:
        with open(args.local_file_path, 'r') as f:
            content = base64.b64encode(f.read())
    except IOError, e:
        print(e)
        exit(1)
    #split arg's repo_file_path to repo_name and repo_file_path
    try:
        repo_name, repo_file_path = args.repo_file_path.split('/', 1)
    except ValueError, e:
        print(e)
        exit(1)

    saver = GitSaver(args.owner, args.api_token, repo_name, repo_file_path, content)

    if args.verbose:
        print("check if repo exists")
    #check
    try:
        exists = saver.repo_exists()
    except:
        print("Communication error. e.g check git name and token.")
        exit(1)

    if not exists:
        if args.verbose:
            print("no. creating repo")
        saver.create_repo()
    if args.verbose:
        print("yes")

    if args.verbose:
        print("get file info")

    file_sha = saver.get_file()


    if file_sha:
        if args.verbose:
            print("file already exists. updating. %s" % file_sha)
        return saver.update_file(file_sha)
    else:
        if args.verbose:
            print("file is new. creating")
        return saver.create_file()


if __name__ == "__main__":
    commit_sha = main()
    print(commit_sha)
