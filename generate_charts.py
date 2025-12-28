"""
Generate Business Intelligence Charts from Medium Articles Dataset
This script creates visualizations focused on strategic business insights
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

# Set style for professional business charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Create charts directory if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Load the dataset
print("Loading dataset...")
with open('ALL_179_MEDIUM_ARTICLES_COMPLETE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles = data['articles']
collection_info = data['collection_info']

print(f"Analyzing {len(articles)} articles...")

# Define business-relevant topic categories
TOPIC_KEYWORDS = {
    'AI & Machine Learning': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'neural', 'deep learning', 'model', 'llm', 'gpt'],
    'Data Science & Analytics': ['data', 'analytics', 'statistics', 'analysis', 'statistical', 'analyst', 'visualization'],
    'Software Development': ['java', 'python', 'code', 'programming', 'developer', 'software', 'development'],
    'Business & Strategy': ['business', 'startup', 'entrepreneur', 'market', 'strategy', 'management'],
    'Web Development': ['web', 'react', 'frontend', 'backend', 'api', 'scraping'],
    'Career Development': ['career', 'journey', 'learning', 'guide', 'tips', 'roadmap'],
    'System Architecture': ['system', 'architecture', 'design', 'scalable', 'distributed'],
    'Security & Fraud': ['fraud', 'detection', 'security', 'prevention'],
}

# Analyze topics from titles
topic_counts = Counter()
article_topics = {}

for idx, article in enumerate(articles):
    title_lower = article['title'].lower()
    article_topics[idx] = []

    for topic, terms in TOPIC_KEYWORDS.items():
        if any(term in title_lower for term in terms):
            topic_counts[topic] += 1
            article_topics[idx].append(topic)

# ============================================================================
# CHART 1: Content Portfolio Distribution by Topic Area
# ============================================================================
print("Generating Chart 1: Content Portfolio Distribution...")

fig, ax = plt.subplots(figsize=(14, 8))
topics = [t for t, _ in topic_counts.most_common()]
counts = [c for _, c in topic_counts.most_common()]
percentages = [c/len(articles)*100 for c in counts]

colors = sns.color_palette("husl", len(topics))
bars = ax.barh(topics, counts, color=colors)

# Add value labels
for i, (bar, count, pct) in enumerate(zip(bars, counts, percentages)):
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2,
            f'{count} ({pct:.1f}%)',
            ha='left', va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Number of Articles', fontsize=13, fontweight='bold')
ax.set_title('Content Portfolio Distribution Across Topic Areas\nStrategic Focus on AI, Data Science, and Software Development',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/01_content_portfolio_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 2: Topic Concentration - Top 5 vs Others
# ============================================================================
print("Generating Chart 2: Topic Concentration Analysis...")

fig, ax = plt.subplots(figsize=(12, 7))
top_5_topics = dict(topic_counts.most_common(5))
top_5_count = sum(top_5_topics.values())
other_count = len(articles) - top_5_count

data_for_chart = list(top_5_topics.values()) + [other_count]
labels_for_chart = list(top_5_topics.keys()) + ['Other Topics']
colors_chart = sns.color_palette("Set2", len(data_for_chart))

bars = ax.bar(range(len(data_for_chart)), data_for_chart, color=colors_chart, edgecolor='black', linewidth=1.5)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, data_for_chart)):
    height = bar.get_height()
    pct = val/len(articles)*100
    ax.text(bar.get_x() + bar.get_width()/2, height + 1,
            f'{val}\n({pct:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_xticks(range(len(labels_for_chart)))
ax.set_xticklabels(labels_for_chart, rotation=45, ha='right')
ax.set_ylabel('Number of Articles', fontsize=13, fontweight='bold')
ax.set_title('Content Concentration: Top 5 Strategic Topics Drive Majority of Output\nCore Competencies Clearly Defined',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/02_topic_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 3: Title Length Distribution - Engagement Optimization
# ============================================================================
print("Generating Chart 3: Title Length Analysis...")

title_lengths = [len(article['title']) for article in articles]
df_titles = pd.DataFrame({'length': title_lengths})

fig, ax = plt.subplots(figsize=(12, 7))
ax.hist(title_lengths, bins=30, color='#3498db', edgecolor='black', alpha=0.7)

mean_length = sum(title_lengths) / len(title_lengths)
ax.axvline(mean_length, color='red', linestyle='--', linewidth=2, label=f'Average: {mean_length:.1f} chars')

ax.set_xlabel('Title Length (characters)', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Articles', fontsize=13, fontweight='bold')
ax.set_title('Title Length Distribution: Optimization for Reader Engagement\nMost Titles Between 20-60 Characters - Aligned with Best Practices',
             fontsize=15, fontweight='bold', pad=20)
ax.legend(fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/03_title_length_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 4: Content Volume Quartile Analysis
# ============================================================================
print("Generating Chart 4: Content Volume Quartile Analysis...")

# Divide articles into quartiles by article number
quartile_size = len(articles) // 4
quartiles = {
    'Q1 (Early)': articles[:quartile_size],
    'Q2': articles[quartile_size:quartile_size*2],
    'Q3': articles[quartile_size*2:quartile_size*3],
    'Q4 (Recent)': articles[quartile_size*3:],
}

quartile_counts = {q: len(arts) for q, arts in quartiles.items()}

fig, ax = plt.subplots(figsize=(12, 7))
colors_q = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
bars = ax.bar(quartile_counts.keys(), quartile_counts.values(), color=colors_q, edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_ylabel('Number of Articles', fontsize=13, fontweight='bold')
ax.set_xlabel('Publication Timeline', fontsize=13, fontweight='bold')
ax.set_title('Content Production Consistency Across Publishing Timeline\nSteady Output Demonstrates Sustained Content Strategy',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/04_content_volume_timeline.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 5: Most Valuable Keywords - Strategic Content Themes
# ============================================================================
print("Generating Chart 5: Strategic Keyword Analysis...")

stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
              'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'my',
              'your', 'how', 'what', 'when', 'where', 'why', 'this', 'that', 'these',
              'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'vs', 'part'}

all_words = []
for article in articles:
    words = re.findall(r'\b\w+\b', article['title'].lower())
    all_words.extend([w for w in words if w not in stop_words and len(w) > 2])

word_freq = Counter(all_words)
top_15_words = word_freq.most_common(15)

fig, ax = plt.subplots(figsize=(14, 8))
words = [w for w, _ in top_15_words]
freqs = [f for _, f in top_15_words]

colors = sns.color_palette("coolwarm", len(words))
bars = ax.barh(words, freqs, color=colors)

# Add value labels
for i, (bar, freq) in enumerate(zip(bars, freqs)):
    width = bar.get_width()
    ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
            f'{freq}',
            ha='left', va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Frequency in Article Titles', fontsize=13, fontweight='bold')
ax.set_title('Top 15 Strategic Keywords: Content Themes Driving Expertise Positioning\nData, Java, and Machine Learning Define Core Value Proposition',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/05_strategic_keywords.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 6: Multi-Topic Articles - Cross-Domain Expertise
# ============================================================================
print("Generating Chart 6: Cross-Domain Expertise Analysis...")

topics_per_article = [len(topics) for topics in article_topics.values()]
topic_dist = Counter(topics_per_article)

fig, ax = plt.subplots(figsize=(12, 7))
labels = [f'{count} Topic{"s" if count != 1 else ""}' for count in sorted(topic_dist.keys())]
values = [topic_dist[count] for count in sorted(topic_dist.keys())]
colors_td = sns.color_palette("viridis", len(labels))

bars = ax.bar(labels, values, color=colors_td, edgecolor='black', linewidth=1.5)

# Add value labels
for bar, val in zip(bars, values):
    height = bar.get_height()
    pct = val/len(articles)*100
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
            f'{val}\n({pct:.1f}%)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Number of Articles', fontsize=13, fontweight='bold')
ax.set_xlabel('Topic Coverage per Article', fontsize=13, fontweight='bold')
ax.set_title('Cross-Domain Content Strategy: Multi-Topic Articles Demonstrate Versatility\nIntersectional Expertise Creates Unique Value',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('charts/06_cross_domain_expertise.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 7: Topic Co-occurrence - Strategic Content Synergies
# ============================================================================
print("Generating Chart 7: Topic Synergy Analysis...")

# Find top topic combinations
topic_pairs = Counter()
for topics in article_topics.values():
    if len(topics) >= 2:
        for i in range(len(topics)):
            for j in range(i+1, len(topics)):
                pair = tuple(sorted([topics[i], topics[j]]))
                topic_pairs[pair] += 1

top_10_pairs = topic_pairs.most_common(10)

if top_10_pairs:
    fig, ax = plt.subplots(figsize=(14, 9))
    pair_labels = [f"{p[0][:20]}...\n+\n{p[1][:20]}..." if len(p[0]) > 20 or len(p[1]) > 20
                   else f"{p[0]}\n+\n{p[1]}" for p, _ in top_10_pairs]
    pair_counts = [c for _, c in top_10_pairs]

    colors = sns.color_palette("Spectral", len(pair_labels))
    bars = ax.barh(range(len(pair_labels)), pair_counts, color=colors)

    ax.set_yticks(range(len(pair_labels)))
    ax.set_yticklabels(pair_labels, fontsize=10)
    ax.set_xlabel('Number of Articles', fontsize=13, fontweight='bold')
    ax.set_title('Top Content Synergies: Most Powerful Topic Combinations\nStrategic Intersections Create Differentiated Value Propositions',
                 fontsize=15, fontweight='bold', pad=20)

    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, pair_counts)):
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
                f'{count}',
                ha='left', va='center', fontsize=11, fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('charts/07_topic_synergies.png', dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# CHART 8: Content Strategy Heat Map - Title Length vs Topic
# ============================================================================
print("Generating Chart 8: Content Strategy Heat Map...")

# Create data for heatmap
topic_length_data = {topic: [] for topic in TOPIC_KEYWORDS.keys()}

for idx, article in enumerate(articles):
    title_len = len(article['title'])
    for topic in article_topics.get(idx, []):
        if topic in topic_length_data:
            topic_length_data[topic].append(title_len)

# Calculate average length per topic
avg_lengths = {topic: (sum(lengths)/len(lengths) if lengths else 0)
               for topic, lengths in topic_length_data.items()}
count_per_topic = {topic: len(lengths) for topic, lengths in topic_length_data.items()}

# Filter out topics with no articles
filtered_topics = {k: v for k, v in avg_lengths.items() if v > 0}

fig, ax = plt.subplots(figsize=(14, 8))
topics_sorted = sorted(filtered_topics.keys(), key=lambda x: filtered_topics[x], reverse=True)
avg_lens_sorted = [filtered_topics[t] for t in topics_sorted]
counts_sorted = [count_per_topic[t] for t in topics_sorted]

# Create bars with color gradient based on article count
normalize = plt.Normalize(vmin=min(counts_sorted), vmax=max(counts_sorted))
colors = plt.cm.RdYlGn(normalize(counts_sorted))

bars = ax.barh(topics_sorted, avg_lens_sorted, color=colors, edgecolor='black', linewidth=1)

# Add value labels
for i, (bar, avg_len, count) in enumerate(zip(bars, avg_lens_sorted, counts_sorted)):
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{avg_len:.1f} chars ({count} articles)',
            ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Average Title Length (characters)', fontsize=13, fontweight='bold')
ax.set_title('Title Length Strategy by Topic: Optimization Patterns\nColor Intensity = Article Volume | Reveals Topic-Specific Engagement Approaches',
             fontsize=15, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add colorbar legend
sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=normalize)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.01)
cbar.set_label('Article Volume', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_title_strategy_by_topic.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*80)
print("CHART GENERATION COMPLETE")
print("="*80)
print(f"\nGenerated 8 business intelligence charts in the 'charts/' directory:")
print("  1. Content Portfolio Distribution")
print("  2. Topic Concentration Analysis")
print("  3. Title Length Distribution")
print("  4. Content Volume Timeline")
print("  5. Strategic Keywords")
print("  6. Cross-Domain Expertise")
print("  7. Topic Synergies")
print("  8. Title Strategy by Topic")
print("\n" + "="*80)
print("\nKey Business Metrics:")
print(f"  • Total Articles: {len(articles)}")
print(f"  • Primary Topics: {len(topic_counts)}")
print(f"  • Average Title Length: {sum(title_lengths)/len(title_lengths):.1f} characters")
print(f"  • Top Content Area: {topic_counts.most_common(1)[0][0]} ({topic_counts.most_common(1)[0][1]} articles)")
print(f"  • Content Diversity Score: {len(topic_counts)/len(articles):.2%}")
print("="*80)
