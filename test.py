GNU nano 7.2                                                                                git.py
from os import popen
from os import listdir, getcwd
from os.path import join, isdir
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

lock = Lock()

def update(_dir):
    _dir = join(getcwd(), _dir)
    if isdir(_dir) and ".git" in list(listdir(_dir)):
        with lock:
            print(f"Opening Directory {_dir}")
            git_status = popen(f"cd '{_dir}' && git config --local --add safe.directory '{_dir}' && git fetch --all && git reset --no-refresh && git pull").read()

        if git_status.strip() != "Already up to date.":
            popen("cd '" + _dir + "' & find . -type f -exec chmod 644 {} +")
            popen("cd '" + _dir + "' & find . -type d -exec chmod 755 {} +")
            popen("cd '" + _dir + "' & find . -type f -name '*.html' -exec chmod 777 {} +")
            popen("cd '" + _dir + "' & chown -R www-data:www-data ./*")


while True:
    with ThreadPoolExecutor() as executor:
        for dir in listdir("."):
            # update(dir)
            executor.submit(update, dir)





