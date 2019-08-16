from git import Repo
import os
import sys
import re

def git_push(PATH_OF_GIT_REPO, REMOTE):
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        REMOTE = str(REMOTE).strip()
        repo.git.add(update=True)
        #repo.git.add()
        origin = repo.remote(name=REMOTE)
        #origin.fetch()
        origin.push(force=True)
        print('Successfully pushed to: ', REMOTE)
    except Exception as e:
        print(f'Some error occured while pushing the code to {REMOTE}: ',e)


def readcfg(CFG):
    # get upstreams from config
    res = []
    if os.path.exists(PATH_OF_GIT_REPO):
        with open(CFG) as f:
            data = f.readline()
            c = 1
            while data:
                data = f.readline()
                search = r'(^\[remote\ *)(\"(.+?)\")'
                match = re.findall(search, data)
                if match:
                    res.append(match[0][2])
                c += 1
    else:
        print("Config not found! Change you path to git working directory and try again. Exiting...")
        sys.exit(1)
    return res

PATH_OF_GIT_REPO = r'.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = input("Specify a comment please: ")
COMMIT_MESSAGE = str(COMMIT_MESSAGE).strip()

CFG = f"{PATH_OF_GIT_REPO}/config"

w = readcfg(CFG)
repo = Repo(PATH_OF_GIT_REPO)
repo.index.commit(COMMIT_MESSAGE)

for REMOTE in w:
    if REMOTE != 'prepod':
        git_push(PATH_OF_GIT_REPO, REMOTE)
