import openai
from tinydb import TinyDB, Query

from ar_com_pelucadorada_www.News import News

class GPTClient:
    def __init__(self, openai_api_key):
        self.db = TinyDB('ar_com_pelucadorada_data/website_content.json')
        self.query = Query()
        self.associations_db = TinyDB('ar_com_pelucadorada_data/news_semantic_association.json')
        openai.api_key = openai_api_key

    def process_semantic_associations(self):
        all_equivalences = self.associations_db.all()
        for equivalence in all_equivalences:
            news_array = self._fetch_news_array(equivalence)
            if news_array:
                merged_news = self.send(news_array)
                # Process the merged news as required

    def _fetch_news_array(self, equivalence):
        news_array = []
        added_news_ids = set()  # To keep track of added news IDs
        pivotal_news_id = equivalence['news_id']
        equivalent_news_ids = equivalence['semantically_equivalent_to']

        # Debugging: Print out the IDs being searched
        print(f"Pivotal News ID: {pivotal_news_id}")
        print(f"Equivalent News IDs: {equivalent_news_ids}")

        # Iterate through each newspaper record
        for record in self.db.all():
            for category in record['categories']:
                for news in category['news']:
                    if news['id'] in [pivotal_news_id] + equivalent_news_ids and news['id'] not in added_news_ids:
                        print(f"Found news with ID {news['id']}")
                        news_instance = News(news)
                        news_array.append(news_instance)
                        added_news_ids.add(news['id'])  # Mark this ID as added

        return news_array



    def send(self, news_array):
        prompt = self._create_gpt_prompt(news_array)
        return self._send_to_gpt(prompt)

    def _create_gpt_prompt(self, news_array):
        prompt = "Combinar las siguientes noticias semanticamente similares en una sola noticia y ademas ponerle un titulo representativo de la misma: \n\n"
        for i, news in enumerate(news_array, 1):
            prompt += f"Article {i}:\nTitle: {news.title}\nBody: {news.body}\n\n"
        prompt += "Rewritten News Article:"
        return prompt


    def _send_to_gpt(self, prompt):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # Replace with the actual model you are using
                prompt=prompt,
                max_tokens=150
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
# gpt_client = GPTClient(your_openai_api_key)
# gpt_client.process_semantic_associations()