from flask import Flask, jsonify, render_template
import feedparser
from datetime import datetime
import time

app = Flask(__name__)
FEEDS = [
    'https://assabah.ma/feed',
    'https://www.alaraby.com/rss/news',
    'https://www.theguardian.com/world/rss',
    'https://feeds.arstechnica.com/arstechnica/index/',
    'https://www.aljazeera.com/xml/rss/all.xml'
]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/posts')
def get_posts():
    all_posts = []

    for url in FEEDS:
        feed = feedparser.parse(url)
        source_title = feed.feed.get('title', 'Unknown Source')

        for entry in feed.entries:
            image_url = ""
            if 'media_content' in entry:
                image_url = entry.media_content[0].get('url', '')
            elif 'media_thumbnail' in entry:
                image_url = entry.media_thumbnail[0].get('url', '')
            elif 'links' in entry:
                for link in entry.links:
                    if link.get('type', '').startswith('image/'):
                        image_url = link.get('href', '')
                        break

            # Parse publication date as datetime
            published = entry.get('published_parsed')
            published_dt = datetime.fromtimestamp(time.mktime(published)) if published else datetime.now()

            all_posts.append({
                'title': entry.title,
                'link': entry.link,
                'pubDate': published_dt.isoformat(),
                'source': source_title,
                'summary': entry.get('summary', '')[:250],
                'image': image_url,
                'timestamp': published_dt.timestamp()
            })

    # Sort by time, newest first
    sorted_posts = sorted(all_posts, key=lambda x: x['timestamp'], reverse=True)

    return jsonify(sorted_posts)

if __name__ == '__main__':
    app.run(debug=True)