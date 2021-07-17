# -*- coding: utf-8 -*-

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def store_channels(response, channel_dict):
    for item in response['items']:
        channel_dict[item['snippet']['resourceId']['channelId']] = item['snippet']

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = os.environ["CLIENT_SECRET_FILE"]
    skip_channels = [c.strip() for c in os.environ["SKIP_CHANNELS"].split(",")]


    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


    subscriptions = {}

    # Fetch a list of all the user's channels, paginate through all responses, store them in 'channels' dict. 
    subscription_kwargs = { "part": "id,snippet", "mine": True, "maxResults": 50}
    request = youtube.subscriptions().list(**subscription_kwargs)
    response = request.execute()
    store_channels(response, subscriptions)
    while response.get('nextPageToken', False):
        request = youtube.subscriptions().list(pageToken=response['nextPageToken'], **subscription_kwargs)
        response = request.execute()
        store_channels(response, subscriptions)

    # pretty print channels dict
    print("SUBSCRIPTIONS")
    print("Subscription Count:", len(subscriptions))
    for channel_id, channel in subscriptions.items():
        if (channel['title'] in skip_channels):
            print("SKIPPING {0}".format(channel['title']))
        else:
            print("FETCHING {0}".format(channel['title']))
            continue
        # print(channel['title'], channel_id)
        # search is an expensive operation, it takes 100 credits! (and only 10k credits per day)
        request = youtube.search().list(channelId=channel_id, type="video", part="snippet", order="viewCount")
        response = request.execute()
        for video in response['items']:
            # print("\t", video['snippet']['title'], "https://www.youtube.com/watch?v={0}".format(video['id']['videoId']))
            print(channel['title'] + "\\" + video['snippet']['title'] + "\\" + 
                  "https://www.youtube.com/watch?v={0}".format(video['id']['videoId']))


if __name__ == "__main__":
    main()