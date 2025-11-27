import json
import fcntl
import os
from pathlib import Path

# the ugly parts of this file are actually caused by fastapi
# as it is a preforking server and would run into race conditions
# between server processes corrupting the file.
# hence all the locking annoyance.

# since we have to lock the files to avoid corruption we also can't use aiofiles here

def write_to_file(input_message: str, response: str):
    json_message = json.dumps({"input": input_message, "result": response})
    filename = "output.txt"
    assure_file_exists(filename)
    append_to_file(filename, json_message)

## initial file creation must be exclusive, otherwise locking has no real benefit
def assure_file_exists(filename):
    if not Path(filename).exists():
        try:
            open(filename, 'x')
        except FileExistsError:
            pass # it's ok, some other worker in parallel created the file first
    pass


def append_to_file(filename, json_message):
    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0, os.SEEK_END)
        f.write(json_message + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)

