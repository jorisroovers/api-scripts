# Youtube

Scripts that interact with the Youtube API.

## Top Videos
Fetch top videos for all your personal subscriptions, print as csv.

```sh
poetry shell
poetry install
# Download the client_secret.json file first from the google cloud console
# Needs to have "YouTube Data API v3" APIs enabled for project
# See https://developers.google.com/youtube/v3/quickstart/python
export CLIENT_SECRET_FILE="client_secret.json"
python top-videos.py
```
