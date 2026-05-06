from pydantic import BaseModel

class Basic_Article_Info(BaseModel):
    title: str
    date: str
    link: str
    tags: list
    summary: str
    source: str
    cves: str | set
    chatgpt_link: str
    article_text : str
    image : str

def create_teams_article_notifcation(article_info: Basic_Article_Info):
    return f"""
    <strong>New Article Notification</strong>
    <br>
    <br>
    <strong>Title: </strong> {article_info['title']}
    <br>
    <strong>Source: </strong> {article_info['source']}
    <br>
    <strong>Published Date & Time: </strong> {article_info['date']}
    <br>
    <strong>Tags : </strong> {' | '.join(article_info['tags'])}
    <br>
    <strong>Summary: </strong> {article_info['summary']}
    <br>
    <strong>CVEs: </strong> {article_info['cves'] if isinstance(article_info['cves'], str) else ', '.join(article_info['cves'])}
    <br>
    <strong>Link: </strong><a href={article_info['link']}>Article Link</a>
    <br>
"""

def create_article_postcards(article_info: Basic_Article_Info):
    postcard ={
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "2.0",
        "speak": "test",
        "body": [
            {
                "type": "TextBlock",
                "text": "📰 News Notification",
                "weight": "Bolder",
                "size": "Large"
            },
            {
                "type": "Container",
                "$data": "${articles}",
                "spacing": "Medium",
                "separator": "true",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": article_info["title"],
                        "weight": "Bolder",
                        "wrap": "true",
                        "size": "Large",
                        "spacing": "None"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**Source:** {article_info['source']}",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Medium"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**Published Date:** {article_info['date']}",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**Flagged Words:** {' | '.join(article_info['tags'])}",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**Article Summary:** {article_info['summary']}",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**CVEs:** {article_info['cves'] if isinstance(article_info['cves'], str) else ', '.join(article_info['cves'])}",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "Image",
                        "url": f"{article_info['image']}",
                        "altText": "Article Image",
                        "height": "250px",
                        "width": "400px",
                        "spacing": "Medium",
                        "horizontalAlignment": "Center"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"**Link**: [Article Link]({article_info['link']})",
                        "wrap": "true",
                        "size": "Small",
                        "spacing": "Medium"
                    },
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "Analyze in ChatGPT",
                "url": article_info['chatgpt_link']
            },
        ]
    }

    return postcard