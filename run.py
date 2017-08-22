#!/usr/bin/python

import MySQLdb

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# YouTube
DEVELOPER_KEY            = "DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION      = "v3"
YOUTUBE_CHANNEL_ID       = "YOUTUBE_CHANNEL_ID"

# MySQL
HOST   = "127.0.0.1"
USER   = "username"
PASS   = "password"
DBNAME = "video"
PORT   = "3306"

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

  insert_db(videos)

def insert_db(videos):

  db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset="utf8mb4")
  cursor = db.cursor()

  try:
    sql = "INSERT INTO video (youtube_id, title, image_url) VALUES (%s, %s, %s)"
    cursor.executemany(sql, videos)
    db.commit()
  except Exception as e:
      print e
      db.rollback()

  db.close()

if __name__ == "__main__":
  try:
    youtube_search()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
