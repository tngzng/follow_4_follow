import os
import json


def load_env() -> None:
    # in the prod workflow, GitHub secrets will pre-load the env vars for us
    # https://docs.github.com/en/actions/reference/encrypted-secrets
    # but locally, we have to source the env vars ourselves
    ENV_FILE = "env.json"
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            env_vars = json.load(f)

        for var_name, val in env_vars.items():
            os.environ[var_name] = val
