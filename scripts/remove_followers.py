import time
import logging
from typing import Iterator, Dict, Any

from instagram_private_api import Client as AppClient
from instagram import WebClient, paginate_all


def remove_followers(username: str, password: str) -> None:
    logging.info(f"Removing accounts from {username}")
    authed_web_api = WebClient(
        auto_patch=True,
        authenticate=True,
        username=username,
        password=password,
    )

    followers = [
        u
        for u in paginate_all(
            authed_web_api.user_followers, authed_web_api, "edge_followed_by"
        )
    ]
    following = [
        u
        for u in paginate_all(
            authed_web_api.user_following, authed_web_api, "edge_follow"
        )
    ]
    follower_handles = {f["username"] for f in followers}
    following_handles = {f["username"] for f in following}
    remove_handles = follower_handles - following_handles
    remove_ids = [f["id"] for f in followers if f["username"] in remove_handles]
    logging.info(f"found {len(remove_ids)} followers to remove")

    authed_private_api = AppClient(
        auto_patch=True,
        authenticate=True,
        username=username,
        password=password,
    )
    for remove_id, remove_handle in zip(remove_ids, remove_handles):
        logging.info(f"Unfollowing {remove_handle}...")
        authed_private_api.remove_follower(remove_id)
        time.sleep(60)
