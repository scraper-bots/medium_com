import json
import pandas as pd
from datetime import datetime
from collections import Counter
import re

# Load the dataset
with open('ALL_179_MEDIUM_ARTICLES_COMPLETE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles = data['articles']
collection_info = data['collection_info']

print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"Total articles: {len(articles)}")
print(f"Author: {collection_info['author']}")
print(f"Scraped at: {collection_info['scraped_at']}")
print(f"\nArticle topics: {', '.join(collection_info['article_topics'])}")

# Extract all available fields from sample articles
print("\n" + "="*80)
print("FIELD ANALYSIS")
print("="*80)

sample_article = articles[0]
print("\nAvailable fields in articles:")
for key in sample_article.keys():
    print(f"  - {key}")

# Analyze titles for patterns
print("\n" + "="*80)
print("TITLE ANALYSIS")
print("="*80)

titles = [article['title'] for article in articles]
title_lengths = [len(title) for title in titles]
print(f"\nAverage title length: {sum(title_lengths) / len(title_lengths):.1f} characters")
print(f"Shortest title: {min(title_lengths)} characters")
print(f"Longest title: {max(title_lengths)} characters")

# Topic extraction from titles
print("\n" + "="*80)
print("TOPIC ANALYSIS FROM TITLES")
print("="*80)

# Common tech/business keywords
keywords = {
    'AI/ML': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'neural', 'deep learning', 'model'],
    'Data Science': ['data', 'analytics', 'statistics', 'analysis', 'statistical'],
    'Programming': ['java', 'python', 'code', 'programming', 'developer', 'software'],
    'Business': ['business', 'startup', 'entrepreneur', 'market', 'strategy'],
    'Web Development': ['web', 'react', 'frontend', 'backend', 'api'],
    'Career/Personal': ['career', 'journey', 'learning', 'guide', 'tips', 'how to'],
    'System Design': ['system', 'architecture', 'design', 'scalable', 'distributed'],
    'Testing/QA': ['test', 'testing', 'qa', 'quality'],
}

topic_counts = Counter()
for article in articles:
    title_lower = article['title'].lower()
    for topic, terms in keywords.items():
        if any(term in title_lower for term in terms):
            topic_counts[topic] += 1

print("\nTopic distribution (from title analysis):")
for topic, count in topic_counts.most_common():
    print(f"  {topic}: {count} articles ({count/len(articles)*100:.1f}%)")

# Analyze URL patterns
print("\n" + "="*80)
print("URL PATTERN ANALYSIS")
print("="*80)

urls = [article['url'] for article in articles]
avg_url_length = sum(len(url) for url in urls) / len(urls)
print(f"\nAverage URL length: {avg_url_length:.1f} characters")

# Analyze article numbering
print("\n" + "="*80)
print("ARTICLE SEQUENCE ANALYSIS")
print("="*80)

article_numbers = [article.get('article_number', 0) for article in articles]
print(f"\nArticle numbers range: {min(article_numbers)} to {max(article_numbers)}")
print(f"Total unique article numbers: {len(set(article_numbers))}")

# Create a DataFrame for easier analysis
df_data = []
for article in articles:
    row = {
        'article_number': article.get('article_number', 0),
        'title': article['title'],
        'title_length': len(article['title']),
        'url_length': len(article['url']),
        'has_content': article['metadata'].get('content_available', False),
    }

    # Add topic flags
    title_lower = article['title'].lower()
    for topic, terms in keywords.items():
        row[f'topic_{topic.replace("/", "_").replace(" ", "_")}'] = any(term in title_lower for term in terms)

    df_data.append(row)

df = pd.DataFrame(df_data)

# Save for further analysis
df.to_csv('articles_analysis.csv', index=False)
print("\n" + "="*80)
print(f"\nData exported to 'articles_analysis.csv' for further analysis")
print(f"Total rows: {len(df)}")
print("\nDataFrame columns:")
for col in df.columns:
    print(f"  - {col}")

# Title word frequency
print("\n" + "="*80)
print("MOST COMMON WORDS IN TITLES (excluding common words)")
print("="*80)

stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
              'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'my',
              'your', 'how', 'what', 'when', 'where', 'why', 'this', 'that', 'these',
              'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}

all_words = []
for title in titles:
    words = re.findall(r'\b\w+\b', title.lower())
    all_words.extend([w for w in words if w not in stop_words and len(w) > 2])

word_freq = Counter(all_words)
print("\nTop 30 most frequent words:")
for word, count in word_freq.most_common(30):
    print(f"  {word}: {count}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
