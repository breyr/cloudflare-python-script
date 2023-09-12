# Author: Brey Rivera
# Date created: 09/11/2023
'''
Prereqs:
    - Python 3.9+
    - Signed into Cloudflare account
'''

import subprocess

REPO_NAME = "example-repo"
GITHUB_ACCT = "example-username"

commands = [f"wget https://github.com/{GITHUB_ACCT}/{REPO_NAME}/archive/main.zip",
            "unzip main.zip",
            "rm main.zip",
            # install dependencies if you want to modify code
            # "npm install",
            # checks if wrangler is installed, if not installs it
            "npm list -g | grep wrangler || npm install -g wrangler",
            # check to see if user is logged in, if not have them log in
            "wrangler whoami || wrangler login",
            f"wrangler d1 create {REPO_NAME}-db",
            # deploy to Cloudflare
            f"cd {REPO_NAME}-main && wrangler deploy"]

for command in commands:
    print(f"Running command: {command}")
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        # if wrangler d1 create dev is run, append the output to wrangler.toml
        # only need last 5 lines of output
        if command == f"wrangler d1 create {REPO_NAME}-db":
            with open(f"{REPO_NAME}-main/wrangler.toml", "a") as f:
                # write new line to separate configs in toml file for spacing
                f.write("\n" * 2)
                for line in output.split("\n")[-5:]:
                    f.write(line + "\n")
        elif command == f"cd {REPO_NAME}-main && wrangler deploy":
            print(output)
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur
        print(f"Error running command: {command}")
        print(f"Error message: {e.output}")

print("Deployed to Cloudflare! ✅")
