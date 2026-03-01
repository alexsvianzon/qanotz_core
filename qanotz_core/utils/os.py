"""
Copyright 2026 Alex

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

import platform
import os
from datetime import datetime
from pathlib import Path

def get_os():
    return platform.system()

def get_appdata_dir() -> str:
    if get_os() == "Windows":
        return str(os.getenv('APPDATA'))
    elif get_os() == "Darwin":
        return os.path.expanduser('~/Library/Application Support')
    else:
        return os.path.expanduser('~/.config')
    
def ensure_dir(path: str) -> bool:
    path_obj = Path(path)
    if path_obj.exists() and path_obj.is_dir():
        return True
    else:
        os.makedirs(path, exist_ok=True)
        return True
    
def get_datetime():
    return datetime.now().strftime("%c")
    
if __name__ == "__main__":
    print(f"Operating System: {get_os()}")
    print(f"AppData Directory: {get_appdata_dir()}")
    print(f"Does AppData Directory Exist? {ensure_dir(f'{get_appdata_dir()}/notes_app')}")
    print(f"It is {get_datetime()}")
    