from tinydb import TinyDB, Query

class NewsCategoryManager:
    def __init__(self, db_path='..ar_com_pelucadorada_data/news_categories.json'):
        # Initialize or load the database
        self.db = TinyDB(db_path)
        self.query = Query()

    def initialize_database(self, initial_data):
        # Clear existing data and initialize with initial data
        self.db.truncate()
        for language, categories in initial_data.items():
            self.db.insert({'language': language, 'categories': categories})

    def get_categories(self, language):
        # Retrieve categories for a specific language
        result = self.db.search(self.query.language == language)
        return result[0]['categories'] if result else []

    def add_category(self, category, translations):
        # Add a category in English and its equivalent in other languages
        for language, translated_category in translations.items():
            self.db.update({'categories': self.query.categories.append(translated_category)}, self.query.language == language)

    def remove_category(self, category):
        # Remove a category from all languages
        for record in self.db.all():
            if category in record['categories']:
                updated_categories = [c for c in record['categories'] if c != category]
                self.db.update({'categories': updated_categories}, self.query.language == record['language'])


# Initialize the manager
#manager = NewsCategoryManager()
#manager.initialize_database({"en": main_categories_en})


# Insert statements for other languages
#for lang_code in iso_language_codes:
    # Assuming you have a function or a way to get translated categories for each language
   # translated_categories = get_translated_categories(lang_code, main_categories_en)
   # manager.add_language(lang_code, translated_categories)


