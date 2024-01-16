from tinydb import TinyDB, Query
from datetime import datetime

from ar_com_pelucadorada_language.Language import Language

# Initialize the database
db = TinyDB('ar_com_pelucadorada_data/website_content.json')
query = Query()

def find_similar_news(input_news):
    # Extract necessary details from the input news
    input_text = input_news['text']
    input_category = input_news['category']
    input_language = Language.detect_language(input_text)

    # Today's date (or the date you want to search)
    today_date = datetime.now().strftime('%d/%m/%Y')

    # Search for today's news in the same category
    todays_news = db.search((query.date == today_date) & (query.category == input_category))

    # List to store similar news with their similarity scores
    similar_news = []

    for news in todays_news:
        # Skip comparing the news with itself
        if news['id'] == input_news['id']:
            continue

        # Calculate similarity score
        news_text = news['text']
        score = Language.get_similarity_score(input_text, news_text, input_language)
        similar_news.append((news, score))

    # Sort the news by similarity score in descending order
    similar_news.sort(key=lambda x: x[1], reverse=True)

    return similar_news

# Example usage
input_news = {
    'id': 'news_id_123',
    'text': 'Your input news text here',
    'category': 'politics',
    # Add other relevant fields if needed
}

similar_news_list = find_similar_news(input_news)
for news, score in similar_news_list:
    print(f"ID: {news['id']}, Score: {score}")
