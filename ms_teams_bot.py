import time
from dotenv import dotenv_values
from news_rss_feeds.news_feed_poller import poll_news_feeds
import requests
from pprint import pprint
from dotenv import load_dotenv
import os
from misc.helpers import extract_txt, update_txt
from datetime import datetime as dt
import argparse

LAST_SCAN_FILEPATH = "./txt_files/last_poll.txt"

# Posts team message/postcard
def post_team_message(message, webhook_url, isTest): 
    payload = {
        "message" : message,
    }

    headers = {
        "Content-Type": "application/json"
    }

    if isTest:
        print("=============TESTING==============")
        print(message)
    else:
        requests.post(webhook_url, headers=headers, json=payload, verify=False)



# Main polling tasks: Grabs infromation for polled articles -> Posts them on team via webhooks
def polling_task(message_hook, postcard_hook, debug_mode):
    print("Running Polling")

    last_scan_date = dt.strptime(extract_txt(LAST_SCAN_FILEPATH), "%Y-%m-%d %H:%M:%S")
    print("Last Updated Time: ", last_scan_date)

    post_team_message(f"🔄 Checking for new updates...\n🕒 Last checked: {last_scan_date}", message_hook, debug_mode)

    # Find all new articles since the last polling time
    new_article_notifications = poll_news_feeds()
    print(f"Finished Polling. Found {len(new_article_notifications)} relevent news artiles. Uploading to teams chat...")
    for notif in new_article_notifications:
            post_team_message(notif, postcard_hook, debug_mode)
            time.sleep(3)

    print("All Notifications have been sent. Task has been compelted.")

    time.sleep(20)
    post_team_message(f"Performed hourly polling. Added: {len(new_article_notifications)} new articles!", message_hook, debug_mode)

    # Update Last Poll Time
    update_txt(LAST_SCAN_FILEPATH, dt.now().strftime("%Y-%m-%d %H:%M:%S"))  

# Runs main feed 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script fetches new articles from multiple sources and filters based on predefined key words"
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Determine if fetching will be done on debug mode"
    )

    parser.add_argument(
        "-j",
        "--junk",
        action="store_true",
        help="Determine if messages should be sent to junk teams chat"
    )

    args = parser.parse_args()
    debug_mode = args.debug
    junk_mode = args.junk

    # print(junk_mode, debug_mode)

    # Webhooks for both feeds    
    load_dotenv()

    if not junk_mode: 
        MESSAGE_FEED_WEBHOOK = os.getenv("MS_TEAMS_MESSAGE_WEBHOOK")
        POSTCARD_FEED_WEBHOOK = os.getenv("MS_TEAMS_POSTCARD_WEBHOOK")
    else:
        MESSAGE_FEED_WEBHOOK = os.getenv("TESTING_MS_TEAMS_MESSAGE_WEBHOOK")
        POSTCARD_FEED_WEBHOOK = os.getenv("TESTING_MS_TEAMS_POSTCARD_WEBHOOK")

    polling_task(MESSAGE_FEED_WEBHOOK, POSTCARD_FEED_WEBHOOK, debug_mode)