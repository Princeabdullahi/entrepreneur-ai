from transformers import pipeline
import pandas as pd
# Add to ai_analyzer.py
from googlesearch import search
import requests
from bs4 import BeautifulSoup

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
