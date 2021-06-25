import json
import random
import string
import hashlib
import datetime
import uuid
import logging
import os

from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError


class MyClient(Client):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = "".join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()

    @classmethod
    def generate_uuid(cls, return_hex=False, seed=None):
        """
        Generate uuid
        :param return_hex: Return in hex format
        :param seed: Seed value to generate a consistent uuid
        :return:
        """
        if seed:
            m = hashlib.md5()
            m.update(seed.encode("utf-8"))
            new_uuid = uuid.UUID(m.hexdigest())
        else:
            new_uuid = uuid.uuid1()
        if return_hex:
            return new_uuid.hex
        return str(new_uuid)

    def login(self):
        """Login to the web site."""
        if not self.username or not self.password:
            raise ClientError("username/password is blank")

        time = str(int(datetime.datetime.now().timestamp()))
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}"

        params = {
            "username": self.username,
            "enc_password": enc_password,
            "queryParams": "{}",
            "optIntoOneTap": False,
        }
        self._init_rollout_hash()
        login_res = self._make_request(
            "https://www.instagram.com/accounts/login/ajax/", params=params
        )
        if not login_res.get("status", "") == "ok" or not login_res.get(
            "authenticated"
        ):
            raise ClientLoginError("Unable to login")

        if self.on_login:
            on_login_callback = self.on_login
            on_login_callback(self)
        return login_res


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


def unfollow() -> None:
    authed_web_api = MyClient(
        auto_patch=True,
        authenticate=True,
        username=os.getenv("INSTAGRAM_USER"),
        password=os.getenv("INSTAGRAM_PASSWORD"),
    )

    my_id = authed_web_api.authenticated_user_id
    # TODO: support pagination
    followers = authed_web_api.user_followers(my_id, count=50)
    following = authed_web_api.user_following(my_id, count=50)
    follower_handles = {f["username"] for f in followers}
    following_handles = {f["username"] for f in following}
    unfollow_handles = following_handles - follower_handles
    unfollow_ids = [f["id"] for f in following if f["username"] in unfollow_handles]
    logging.info(f"found {len(unfollow_ids)} users to unfollow")
    for unfollow_id in unfollow_ids:
        logging.info(f"unfollowing user id: {unfollow_id}")
        authed_web_api.friendships_destroy(unfollow_id)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    load_env()
    unfollow()
