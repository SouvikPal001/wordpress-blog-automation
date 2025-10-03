# Run this in terminal
# pip install cohere requests python-dotenv
# Create a text file named as topics.txt and include all your topics line by line
# Go to .env

import os
import requests
import cohere
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
WP_ACCESS_TOKEN = os.getenv("WP_ACCESS_TOKEN")
WP_SITE = os.getenv("WP_SITE")

# === Load topics from external .txt file ===
def load_topics_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

topics = load_topics_from_txt("./topics.txt")

# === Step 1: Generate blog using Cohere Chat API ===
def generate_blog(title):
    prompt = f"""
Write a full blog post on: "{title}".
Include an introduction, 3–4 sections with subheadings, and a conclusion.
Make it blog-style, SEO-friendly, and easy to read.
"""
    co = cohere.Client(COHERE_API_KEY)
    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
        temperature=0.7
    )

    return response.text.strip()


# === Step 2: Format to basic HTML ===
def format_to_html(text):
    html = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith("###"):
            html.append(f"<h5>{line.strip('# ').strip()}</h5>")
        elif line.startswith("##"):
            html.append(f"<h4>{line.strip('# ').strip()}</h4>")
        elif line.startswith("#"):
            html.append(f"<h3>{line.strip('# ').strip()}</h3>")
        else:
            html.append(f"<p>{line}</p>")
    return "\n".join(html)

# === Step 3: Post to WordPress ===
def post_to_wordpress(title, html_content):
    api_url = f"https://public-api.wordpress.com/rest/v1.1/sites/{WP_SITE}/posts/new"
    headers = {
        "Authorization": f"Bearer {WP_ACCESS_TOKEN}"
    }
    payload = {
        "title": title,
        "content": html_content,
        "status": "publish"
    }
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code in (200, 201):
        print(f"✅ Posted: {title}")
        print("🔗 Link:", response.json().get("URL"))
    else:
        print(f"❌ Failed to post: {title} — {response.status_code}")
        print(response.text)

# === Run for all topics ===
if __name__ == "__main__":
    for topic in topics:
        print(f"⏳ Generating blog for: {topic}")
        try:
            blog = generate_blog(topic)
            html_blog = format_to_html(blog)
            post_to_wordpress(topic, html_blog)
        except Exception as e:
            print(f"❌ Error for '{topic}':", str(e))