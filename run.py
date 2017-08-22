#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY            = "DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION      = "v3"
YOUTUBE_CHANNEL_ID       = "YOUTUBE_CHANNEL_ID"

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey = DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    part       = "snippet",
    channelId  = YOUTUBE_CHANNEL_ID,
    eventType  = "live", # completed, live, upcoming
    maxResults = 50,
    order      = "date",
    type       = "video",
  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    videos.append([search_result["id"]["videoId"], search_result["snippet"]["title"], search_result["snippet"]["thumbnails"]["high"]["url"]])

  print "Videos:\n", "\n".join(str(v).decode("unicode-escape") for v in videos), "\n"

if __name__ == "__main__":
  try:
    youtube_search()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
