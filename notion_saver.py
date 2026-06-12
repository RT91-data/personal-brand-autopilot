import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def save_post_to_notion(title, content, topic, image_suggestion, scheduled_date=None):
    """Save a generated LinkedIn post to Notion content calendar."""
    
    word_count = len(content.split())
    
    properties = {
        "Post Title": {
            "title": [{"text": {"content": title}}]
        },
        "Post Content": {
            "rich_text": [{"text": {"content": content[:2000]}}]
        },
        "Topic": {
            "rich_text": [{"text": {"content": topic}}]
        },
        "Status": {
            "select": {"name": "Draft"}
        },
        "Image Suggestion": {
            "rich_text": [{"text": {"content": image_suggestion}}]
        },
        "Word Count": {
            "number": word_count
        }
    }
    
    if scheduled_date:
        properties["Scheduled Date"] = {
            "date": {"start": scheduled_date.strftime("%Y-%m-%d")}
        }
    
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=properties
    )
    
    return response["url"]