import openai
import re
import json

from tinydb import TinyDB, Query
from ar_com_pelucadorada_www.News import News

class GPTClient:
    def __init__(self, openai_api_key):
        self.db = TinyDB('ar_com_pelucadorada_data/website_content.json')
        self.query = Query()
        self.associations_db = TinyDB('ar_com_pelucadorada_data/news_semantic_association.json')
        openai.api_key = openai_api_key
        self.news_arrays=[]



    def process_semantic_associations(self):
        all_equivalences = self.associations_db.all()
        for equivalence in all_equivalences:
            news_array = self._fetch_news_array(equivalence)
            if news_array:
                prompt = self._create_gpt_prompt(news_array)
                return self._send_to_gpt(prompt)
                



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




    def _create_gpt_prompt(self, news_array):
        # Create a list of dictionaries for each news article
        articles = [{"title": news.title, "body": news.body} for news in news_array]
        
        # Convert the list of articles to JSON string
        articles_json = json.dumps(articles, indent=2)
        
        # Create the prompt including the JSON string of articles
        prompt = (
            "Below are news articles in JSON format. "
            "Combine the following news articles into a single, cohesive news article. "
            "Ensure that the final article is well-written, in the style of a newspaper, "
            "and includes all relevant information from each article.\n\n"
            f"Articles JSON:\n{articles_json}\n\n"
            "Rewritten News Article:"
        )
        
        return prompt


    def split_text_into_chunks(self,text, max_chunk_size=1000):
        """
        Splits the text into chunks, each of size approximately max_chunk_size.
        It tries to split at sentence boundaries for coherence.
        
        :param text: The input text to split.
        :param max_chunk_size: The maximum size of each chunk in characters.
        :return: A list of text chunks.
        """
        # Regular expression to split the text at the end of sentences
        sentence_endings = re.compile(r"(?<=[.!?]) +")
        sentences = sentence_endings.split(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    # Add the current chunk to the chunks list
                    chunks.append(current_chunk.strip())
                # Start a new chunk with the current sentence
                current_chunk = sentence + " "

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks



    def _send_to_gpt(self, prompt, max_chunk_size=2049):
        try:
            # Split the prompt into chunks
            chunks = self.split_text_into_chunks(prompt, max_chunk_size)

            # Initialize an empty string to collect responses
            full_response = ""

            # Process each chunk with the GPT model
            for chunk in chunks:
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=chunk,
                    max_tokens=150  # Adjust as needed
                )

                # Check if the response is valid and append it to the full response
                if 'choices' in response and len(response['choices']) > 0:
                    full_response += response['choices'][0].text.strip() + "\n"

            return full_response.strip()

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
