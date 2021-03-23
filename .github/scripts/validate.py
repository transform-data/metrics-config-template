import json
import os
import requests
import sys

EXPECTED_TF_CONFIG_FILE_NAMES = ["tdfconfig.yml", "tdfconfig.yaml", "validate_configs.yaml", "commit_configs.yaml"]
TRANSFORM_API_URL = "web-api.prod.transformdata.io"

REPO = os.getenv("REPO")
# remove github org from repo
REPO = '/'.join(REPO.split('/')[1:])

if os.getenv("GITHUB_HEAD_REF") == "":
    BRANCH = os.getenv("GITHUB_REF").lstrip("/refs/heads/")
else:
    BRANCH = os.getenv("GITHUB_HEAD_REF")

COMMIT = os.getenv("GITHUB_SHA")
TRANSFORM_API_KEY = os.getenv("TRANSFORM_API_KEY")
TRANSFORM_CONFIG_DIR = os.getenv("TRANSFORM_CONFIG_DIR")

def read_config_files(config_dir):
    """Read yaml files from config_dir. Returns (file name, file contents) per file in dir"""
    config_dir = "./" + config_dir
    assert os.path.exists(config_dir), f"User-specified config dir ({config_dir}) does not exist"

    results = {}
    for path, _folders, filenames in os.walk(config_dir):
        for fname in filenames:
            if not (fname.endswith(".yml") or fname.endswith(".yaml")):
                continue

            # ignore transform config
            if fname in EXPECTED_TF_CONFIG_FILE_NAMES:
                continue

            with open(os.path.join(path, fname), "r") as f:
                results[fname] = f.read()

    return results

yaml_files = read_config_files(TRANSFORM_CONFIG_DIR or ".")
results = {'yaml_files': yaml_files}
print(f"Files to upload: {yaml_files.keys()}")
headers = {'Content-Type': 'application/json', 'Authorization': f'X-Api-Key {TRANSFORM_API_KEY}'}

add_files_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{REPO}/{BRANCH}/{COMMIT}/add_model_files"
print(f"add_files_url: {add_files_url}")
print("Uploading config files")
r = requests.post(add_files_url, data=json.dumps(results).encode('utf-8'), headers=headers)
print(r.text)
assert r.status_code == 200, "Failed uploading config yaml files"

if sys.argv[1] == "validate":
    validate_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{REPO}/{BRANCH}/{COMMIT}/validate_model"
    print(f"validate_url: {validate_url}")
    print("Checking that uploaded configs are valid and form a valid model")
    r = requests.post(validate_url, headers=headers)
    print(r.text)
    assert r.status_code == 200, "Failed validating uploaded configs"

elif sys.argv[1] == "commit":
    commit_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{REPO}/{BRANCH}/{COMMIT}/commit_model"
    print(f"commit_url: {commit_url}")
    print("Committing model")
    r = requests.post(commit_url, headers=headers)
    print(r.text)
    assert r.status_code == 200, "Failed committing uploaded configs"

else:
    raise Exception("Invalid mode. Expected 'validate' or 'commit'")

