from transformers import pipeline
import pandas as pd
# Add to ai_analyzer.py
from googlesearch import search
import requests
from bs4 import BeautifulSoup
# In ai_analyzer.py
import plotly.express as px
import pandas as pd

def generate_profit_plot(self, sales_df):
    fig = px.line(sales_df, x='date', y='profit', 
                 title='Profit Trend Analysis',
                 template='plotly_dark')
    return fig.to_html(full_html=False)

def get_competitors(location, product):
    query = f"{product} near {location}"
    competitors = []
    
    for url in search(query, num=3, stop=3, pause=2):  # Free scraping
        try:
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.text, 'html.parser')
            title = soup.title.string if soup.title else url
            competitors.append({
                'name': title,
                'url': url,
                'price_range': self.extract_prices(soup)  # Implement your logic
            })
        except:
            continue
            
    return competitors

# Add this to BusinessAnalyzer class
def extract_prices(self, soup):
    # Basic price extraction logic
    prices = []
    for tag in soup.find_all(['span', 'div'], class_=['price', 'amount']):
        text = tag.get_text().strip()
        if '$' in text or '€' in text or '¥' in text:
            prices.append(text)
    return prices[:3] if prices else "Not detected"

class BusinessAnalyzer:
    def __init__(self):
        self.sentiment = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")
        
    def generate_recommendations(self, business_data, sales_df):
        # Basic Profit Analysis
        sales_df['profit'] = sales_df['revenue'] - sales_df['expenses']
        avg_profit = sales_df['profit'].mean()
        
        # Sentiment Analysis on Product Description
        sentiment = self.sentiment(business_data['product'])[0]
        
        # Rule-Based Recommendations
        recs = []
        if avg_profit < 1000:
            recs.append("Boost short-term sales with limited-time offers")
        if 'young adults' in business_data['target_audience']:
            recs.append("Focus on TikTok and Instagram Reels ads")
            
        return {
            "profit_trend": sales_df['profit'].tolist(),
            "sentiment": sentiment['label'],
            "recommendations": recs,
            "social_platforms": ["Instagram", "Facebook Marketplace"] if "local" in business_data['location'] else ["TikTok Ads", "Google Ads"]
        }

# Add to ai_analyzer.py
def generate_social_post(self, business_data, analysis):
    platforms = {
        'Instagram': f"🔥 New {business_data['product']} alert! ",
        'TikTok': f"Did you know about {business_data['product']}? ",
        'LinkedIn': f"Elevating {business_data['product']} solutions for "
    }
    
    posts = {}
    for platform in analysis['social_platforms']:
        base = platforms.get(platform, "")
        posts[platform] = {
            'text': base + self._generate_hashtags(business_data['product']),
            'best_time': self._optimal_time(platform)
        }
    return posts

def _generate_hashtags(self, product):
    return " ".join([f"#{word}" for word in product.split()[:3]])

def _optimal_time(self, platform):
    # Basic time suggestions
    return {
        'Instagram': "9AM or 7PM",
        'TikTok': "11AM-3PM",
        'LinkedIn': "8-10AM Tue/Wed"
    }.get(platform, "Afternoon")
