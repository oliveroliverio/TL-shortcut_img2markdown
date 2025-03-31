#!/usr/bin/env python3
import os
import sys
import json
import datetime

def main():
    debug_info = {
        "timestamp": str(datetime.datetime.now()),
        "working_directory": os.getcwd(),
        "python_path": sys.executable,
        "python_version": sys.version,
        "environment_variables": dict(os.environ),
        "script_path": os.path.abspath(__file__),
        "args": sys.argv,
        "env_file_exists": os.path.exists(".env"),
        "dist_executable_exists": os.path.exists("./dist/img2markdown"),
        "user_home": os.path.expanduser("~"),
        "files_in_current_dir": os.listdir(".")
    }
    
    # Write debug info to a file in the user's home directory
    debug_file = os.path.join(os.path.expanduser("~"), "shortcut_debug.json")
    with open(debug_file, "w", encoding="utf-8") as f:
        json.dump(debug_info, f, indent=2, default=str)
    
    print(f"Debug information written to {debug_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
