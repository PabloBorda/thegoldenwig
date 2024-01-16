import os
from tinydb import TinyDB, Query
from datetime import datetime
from tqdm import tqdm


from ar_com_pelucadorada_language.Language import Language


def news_iterator():
    today_date = datetime.now().strftime('%d/%m/%Y')
    todays_newspapers = db.search(query.date == today_date)

    for newspaper_record in todays_newspapers:
        current_newspaper = newspaper_record['newspaper']
        for category in newspaper_record['categories']:
            category_name = category['category_name']
            news_list = category['news']
            for news_article in news_list:
                yield current_newspaper, category_name, news_article

def category_news_iterator(newspaper,target_news, target_category, compare_function):
    today_date = datetime.now().strftime('%d/%m/%Y')
    todays_newspapers = db.search(query.date == today_date)

    for newspaper_record in todays_newspapers:
        if newspaper_record['newspaper'] != newspaper:  # Skip same newspaper
            for category in newspaper_record['categories']:
                if category['category_name'] == target_category:
                    for news_article in category['news']:
                        if compare_function(target_news['title'], news_article['title']):
                            yield news_article


def create_associations():
    db = TinyDB('ar_com_pelucadorada_data/website_content.json')
    query = Query()
    associations_db = TinyDB('ar_com_pelucadorada_data/news_semantic_association.json')

    # Fetch existing associations and create a set of processed IDs
    existing_associations = associations_db.all()
    processed_ids = {assoc['news_id'] for assoc in existing_associations}

    today_date = datetime.now().strftime('%d/%m/%Y')
    todays_newspapers = db.search(query.date == today_date)
    total_number_of_articles = sum(len(newspaper_record['categories']) for newspaper_record in todays_newspapers)

    with tqdm(total=total_number_of_articles, desc="Processing Articles") as pbar:
        for newspaper, category, article in news_iterator():
            # Skip already processed articles
            if article['id'] in processed_ids:
                pbar.update(1)
                continue

            association = {'news_id': article['id'], 'semantically_equivalent_to': []}
            tqdm.write(f"Newspaper: {newspaper}, Category: {category}, Article: {article['title']}")

            for similar_article in category_news_iterator(newspaper, article, category, Language.semantically_similar):
                if similar_article['id'] not in processed_ids:
                    association['semantically_equivalent_to'].append(similar_article['id'])

            if association['semantically_equivalent_to']:
                associations_db.insert(association)
                processed_ids.add(article['id'])

            pbar.update(1)

    return associations_db.all()




db = TinyDB('ar_com_pelucadorada_data/website_content.json')
query = Query()

associations_db = TinyDB('ar_com_pelucadorada_data/news_semantic_association.json')
# Call the function and store the equivalences
equivalence_classes = create_associations()