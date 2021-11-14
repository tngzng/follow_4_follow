import logging
import os

from config import load_env
from unfollow_accounts import unfollow_accounts

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    load_env()
    CREDENTIALS = os.getenv("INSTAGRAM_CREDENTIALS")
    # CREDENTIALS are formatted like so:
    # username_1,password_1;username_2,password_2
    credential_pairs = CREDENTIALS.split(";")
    for credential_pair in credential_pairs:
        username, password = credential_pair.split(",")
        unfollow_accounts(username, password)
