#!/usr/bin/env python3
"""
Medium Article Scraper - Final Working Version
Extracts articles from Medium using multiple methods
"""

import requests
import json
import time
from datetime import datetime
import re
import html as html_module
from urllib.parse import quote

class MediumScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })

    def extract_json_from_file(self, filename):
        """Extract JSON response from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        response_marker = content.find('response')
        if response_marker == -1:
            return None

        start = content.find('[', response_marker)
        if start == -1:
            return None

        json_content = content[start:]

        try:
            return json.loads(json_content)
        except:
            return None

    def extract_article_content(self, url):
        """Extract full article content using multiple methods"""
        try:
            print(f"🔍 Fetching: {url}")
            response = self.session.get(url, timeout=30)

            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code}")
                return ""

            html_content = response.text

            # Method 1: Apollo State extraction
            content = self.extract_from_apollo_state(html_content)
            if content and len(content) > 500:
                print(f"✅ Apollo: {len(content)} chars")
                return content

            # Method 2: JSON-LD structured data
            content = self.extract_from_jsonld(html_content)
            if content and len(content) > 500:
                print(f"✅ JSON-LD: {len(content)} chars")
                return content

            # Method 3: Article tags
            content = self.extract_from_article_tags(html_content)
            if content and len(content) > 200:
                print(f"✅ HTML: {len(content)} chars")
                return content

            print(f"⚠️ Limited content: {len(content)} chars")
            return content

        except Exception as e:
            print(f"❌ Error: {e}")
            return ""

    def extract_from_apollo_state(self, html_content):
        """Extract from Apollo GraphQL state"""
        try:
            apollo_pattern = r'window\.__APOLLO_STATE__\s*=\s*({.*?});'
            apollo_match = re.search(apollo_pattern, html_content, re.DOTALL)

            if not apollo_match:
                return ""

            apollo_data = json.loads(apollo_match.group(1))

            # Find main post
            for key, value in apollo_data.items():
                if isinstance(value, dict) and value.get('__typename') == 'Post':
                    content_ref = value.get('content', {})
                    if isinstance(content_ref, dict) and '__ref' in content_ref:
                        content_obj = apollo_data.get(content_ref['__ref'], {})
                        body_ref = content_obj.get('bodyModel', {})
                        if isinstance(body_ref, dict) and '__ref' in body_ref:
                            body_obj = apollo_data.get(body_ref['__ref'], {})
                            paragraphs = body_obj.get('paragraphs', [])

                            content_parts = []
                            for para_ref in paragraphs:
                                if isinstance(para_ref, dict) and '__ref' in para_ref:
                                    para_obj = apollo_data.get(para_ref['__ref'], {})
                                    text = para_obj.get('text', '').strip()
                                    para_type = para_obj.get('type', 'P')

                                    if text:
                                        if para_type == 'H3':
                                            content_parts.append(f"\n### {text}\n")
                                        elif para_type == 'H4':
                                            content_parts.append(f"\n#### {text}\n")
                                        elif para_type == 'BQ':
                                            content_parts.append(f"\n> {text}\n")
                                        elif para_type == 'PRE':
                                            content_parts.append(f"\n```\n{text}\n```\n")
                                        else:
                                            content_parts.append(text)

                            return '\n\n'.join(content_parts)

        except Exception as e:
            pass

        return ""

    def extract_from_jsonld(self, html_content):
        """Extract from JSON-LD structured data"""
        try:
            jsonld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
            jsonld_matches = re.findall(jsonld_pattern, html_content, re.DOTALL)

            for match in jsonld_matches:
                try:
                    data = json.loads(match)

                    if isinstance(data, dict):
                        if 'articleBody' in data:
                            return data['articleBody']
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'articleBody' in item:
                                return item['articleBody']

                except json.JSONDecodeError:
                    continue

        except Exception:
            pass

        return ""

    def extract_from_article_tags(self, html_content):
        """Extract from HTML article tags"""
        try:
            patterns = [
                r'<article[^>]*>(.*?)</article>',
                r'<div[^>]*class="[^"]*postArticle[^"]*"[^>]*>(.*?)</div>',
                r'<section[^>]*data-field="body"[^>]*>(.*?)</section>',
            ]

            for pattern in patterns:
                matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    cleaned = self.clean_html_content(match)
                    if len(cleaned) > 200:
                        return cleaned

        except Exception:
            pass

        return ""

    def clean_html_content(self, html):
        """Clean HTML and extract readable text"""
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Convert headers
        html = re.sub(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', lambda m: '\n' + '#' * int(m.group(1)) + ' ' + m.group(2) + '\n', html)

        # Convert paragraphs and breaks
        html = re.sub(r'<p[^>]*>', '\n', html)
        html = re.sub(r'</p>', '\n', html)
        html = re.sub(r'<br[^>]*/?>', '\n', html)

        # Remove all other HTML tags
        html = re.sub(r'<[^>]+>', '', html)

        # Decode HTML entities
        html = html_module.unescape(html)

        # Clean up whitespace
        html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
        html = re.sub(r' +', ' ', html)

        return html.strip()

    def scrape_from_existing_data(self, max_articles=None):
        """Scrape articles from existing data files"""
        print("🚀 Loading articles from data files...")

        # Load from stories page
        stories_data = self.extract_json_from_file("example/stories page.txt")
        if not stories_data:
            print("❌ Could not load stories data")
            return []

        articles = []
        connection = stories_data[0]['data']['viewer']['latestPostsConnection']
        for preview in connection['postPreviews']:
            articles.append(preview['post'])

        if max_articles:
            articles = articles[:max_articles]

        print(f"📊 Processing {len(articles)} articles...")

        results = []

        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] {article['title'][:60]}...")

            # Extract content
            content = self.extract_article_content(article['mediumUrl'])

            article_data = {
                'metadata': {
                    'id': article['id'],
                    'title': article['title'],
                    'url': article['mediumUrl'],
                    'unique_slug': article['uniqueSlug'],
                    'published_at': datetime.fromtimestamp(article['firstPublishedAt'] / 1000).isoformat() if article.get('firstPublishedAt') else None,
                    'updated_at': datetime.fromtimestamp(article['updatedAt'] / 1000).isoformat() if article.get('updatedAt') else None,
                    'reading_time': article.get('readingTime', 0),
                    'word_count': article.get('wordCount', 0),
                    'clap_count': article.get('clapCount', 0),
                    'visibility': article.get('visibility'),
                    'is_locked': article.get('isLocked', False),
                    'response_count': article.get('postResponses', {}).get('count', 0),
                    'creator': article.get('creator', {})
                },
                'content': content,
                'content_length': len(content),
                'extraction_successful': len(content) > 200
            }

            results.append(article_data)
            print(f"📄 Content: {len(content)} characters")

            # Be respectful
            time.sleep(2)

        return results

    def save_results(self, articles, filename="scraped_articles.json"):
        """Save scraping results"""
        output = {
            'scraping_info': {
                'total_articles': len(articles),
                'scraped_at': datetime.now().isoformat(),
                'successful_extractions': sum(1 for a in articles if a['extraction_successful']),
                'scraper_version': 'final',
                'username': 'ismatsamadov'
            },
            'articles': articles
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        successful = output['scraping_info']['successful_extractions']
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"📁 Saved to: {filename}")
        print(f"📊 Total: {len(articles)} articles")
        print(f"✅ Successful: {successful}/{len(articles)}")

        return filename

def main():
    """Main function with options"""
    print("Medium Article Scraper")
    print("=" * 50)

    scraper = MediumScraper()

    # Default: scrape first 5 articles for testing
    print("Starting with first 5 articles (change max_articles=None for all)...")
    articles = scraper.scrape_from_existing_data(max_articles=5)

    if articles:
        filename = scraper.save_results(articles, "medium_articles_scraped.json")
        print(f"\n📋 To scrape all articles, edit the script and set max_articles=None")
    else:
        print("❌ No articles scraped")

if __name__ == "__main__":
    main()