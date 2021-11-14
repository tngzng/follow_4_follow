import time
import logging
from typing import Iterator, Dict, Any

from instagram import WebClient, paginate_all


def unfollow(username: str, password: str) -> None:
    logging.info(f"Unfollowing accounts from {username}")
    # authed_web_api = WebClient(
    #     auto_patch=True,
    #     authenticate=True,
    #     username=username,
    #     password=password,
    # )

    # followers = [
    #     u
    #     for u in paginate_all(
    #         authed_web_api.user_followers, authed_web_api, "edge_followed_by"
    #     )
    # ]
    # following = [
    #     u
    #     for u in paginate_all(
    #         authed_web_api.user_following, authed_web_api, "edge_follow"
    #     )
    # ]
    # follower_handles = {f["username"] for f in followers}
    # following_handles = {f["username"] for f in following}
    # unfollow_handles = following_handles - follower_handles
    # unfollow_ids = [f["id"] for f in following if f["username"] in unfollow_handles]
    # logging.info(f"found {len(unfollow_ids)} users to unfollow")
    # for unfollow_id, unfollow_handle in zip(unfollow_ids, unfollow_handles):
    #     logging.info(f"Unfollowing {unfollow_handle}...")
    #     authed_web_api.friendships_destroy(unfollow_id)
    #     time.sleep(60)
