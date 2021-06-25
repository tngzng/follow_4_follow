# follow_4_follow
A chron job using GitHub Workflows to maintain one-to-one follower relationships on Instagram.

## why?
Instagram can be draining. I've found myself spending hours scrolling through brand and influencer content that doesn't nourish me in any meaningful way. This script attempts to remedy part of that problem, by only maintaining follow 4 follow relationships (two-way relationships that resemble Facebook friends rather than Twitter followers). This changes an Instagram feed from an endless scroll of peripheral content, to a short and sweet summary of people you actually know and care about.

## local usage
1. install dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip && pip3 install -r requirements.txt
```
2. run script
```
python3 unfollow.py
```

## checking workflow status
Go to the [Actions tab](https://github.com/tngzng/follow_4_follow/actions) and click the latest run to view Workflow status. For more info, see [this guide](https://docs.github.com/en/actions/quickstart#viewing-your-workflow-results).
