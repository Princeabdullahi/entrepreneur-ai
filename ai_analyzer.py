from transformers import pipeline
import pandas as pd

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