import requests
import tweepy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class SentimentAnalyzer:
    def __init__(self, news_api_key: str, twitter_bearer_token: str):
        self.news_api_key = news_api_key
        self.twitter_bearer_token = twitter_bearer_token
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def clean_text(self, text: str) -> str:
        """Clean text for sentiment analysis"""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        return text
    
    def analyze_sentiment_vader(self, text: str) -> float:
        """Analyze sentiment using VADER"""
        cleaned_text = self.clean_text(text)
        scores = self.vader_analyzer.polarity_scores(cleaned_text)
        return scores['compound']
    
    def analyze_sentiment_textblob(self, text: str) -> float:
        """Analyze sentiment using TextBlob"""
        cleaned_text = self.clean_text(text)
        analysis = TextBlob(cleaned_text)
        return analysis.sentiment.polarity
    
    def get_crypto_news(self, query: str = "crypto Bitcoin Ethereum") -> List[Dict]:
        """Fetch crypto news from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': self.news_api_key,
                'from': (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return articles[:20]  # Return top 20 articles
            return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_twitter_sentiment(self, query: str = "Bitcoin OR BTC OR crypto") -> List[Dict]:
        """Fetch and analyze tweets (simplified - would need proper Twitter API access)"""
        # Note: This is a simplified version. For production, you'd need proper Twitter API v2 access
        try:
            # This is a placeholder - implement proper Twitter API integration
            client = tweepy.Client(bearer_token=self.twitter_bearer_token)
            
            # Example tweet search (adjust based on your API access level)
            tweets = client.search_recent_tweets(
                query=query,
                max_results=50,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            tweet_data = []
            if tweets.data:
                for tweet in tweets.data:
                    tweet_data.append({
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'retweet_count': tweet.public_metrics['retweet_count']
                    })
            return tweet_data
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []
    
    def calculate_overall_sentiment(self) -> Tuple[float, str]:
        """Calculate overall market sentiment"""
        try:
            # Get news sentiment
            articles = self.get_crypto_news()
            news_sentiments = []
            
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')
                content = f"{title} {description}"
                
                vader_score = self.analyze_sentiment_vader(content)
                textblob_score = self.analyze_sentiment_textblob(content)
                combined_score = (vader_score + textblob_score) / 2
                news_sentiments.append(combined_score)
            
            # Calculate average news sentiment
            avg_news_sentiment = sum(news_sentiments) / len(news_sentiments) if news_sentiments else 0
            
            # Get Twitter sentiment (placeholder - implement based on your access)
            tweets = self.get_twitter_sentiment()
            tweet_sentiments = []
            
            for tweet in tweets:
                vader_score = self.analyze_sentiment_vader(tweet['text'])
                tweet_sentiments.append(vader_score)
            
            avg_twitter_sentiment = sum(tweet_sentiments) / len(tweet_sentiments) if tweet_sentiments else 0
            
            # Combined sentiment (weighted average)
            overall_sentiment = (avg_news_sentiment * 0.6 + avg_twitter_sentiment * 0.4)
            
            # Classify sentiment
            if overall_sentiment > 0.1:
                sentiment_label = "BULLISH"
            elif overall_sentiment < -0.1:
                sentiment_label = "BEARISH"
            else:
                sentiment_label = "NEUTRAL"
                
            return overall_sentiment, sentiment_label
            
        except Exception as e:
            print(f"Error calculating sentiment: {e}")
            return 0.0, "NEUTRAL"