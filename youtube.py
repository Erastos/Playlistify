#!/usr/bin/env python3

import google_auth_oauthlib.flow
import dotenv
import os
import googleapiclient.discovery

dotenv.load_dotenv()

class YoutubeClient():
    def __init__(self, secret_file):
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(secret_file, ["https://www.googleapis.com/auth/youtube"])
        self.yclient = None

    def auth_url(self):
        url, state = self.flow.authorization_url()
        return url

    def authorizeClient(self, response_url):
        creds = self.flow.fetch_token(authorization_response=response_url)
        self.yclient = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    def listChannel(self, channel_id):
        if self.yclient is not None:
            r = self.yclient.channels().list(id=channel_id)
            res = r.execute()
            return res
        else:
            raise Exception(f"Youtube Client has not been authorized, and is therefore unable to list channel {channel_id}")


if __name__ == "__main__":
    yt = YoutubeClient(os.getenv("YOUTUBE_SECRET_FILE"))
    print(f"Authorization URL: {yt.auth_url()}")
    url = input("Reponse URL: ")
    yt.authorizeClient(url)
    print(yt.listChannel("UCaSYagggAN8NtlqYbLuKWSw"))
