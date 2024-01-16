from langdetect import detect, DetectorFactory, lang_detect_exception
import nltk
import logging
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DifferentLanguagesException(Exception):
    pass


# Set the logging level for NLTK to WARNING
logging.getLogger('nltk').setLevel(logging.WARNING)
nltk.download('punkt')

class Language:
    @staticmethod
    def detect_language(text):
        try:
            DetectorFactory.seed = 0
            return detect(text)
        except lang_detect_exception.LangDetectException:
            return None

    @staticmethod
    def preprocess_text(text, lang='en'):

        tokens = nltk.word_tokenize(text.lower(), language=lang)
        stop_words = set(stopwords.words(lang))
        return ' '.join([word for word in tokens if word.isalpha() and word not in stop_words])

    @staticmethod
    def compute_semantic_similarity(text1, text2, lang='english'):
               # Preprocess the texts
        preprocessed_texts = [Language.preprocess_text(text1, lang), Language.preprocess_text(text2, lang)]

        # Use TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform(preprocessed_texts)
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except ValueError:
            # Handle empty vocabulary case by returning a default low similarity score
            similarity_score = 0.0

        return similarity_score
    
    def semantically_similar(text1,text2):       
        similarity_score = Language.compute_semantic_similarity(text1, text2,lang='spanish')
        return similarity_score > 0.3  # Adjust the threshold as needed




    @staticmethod
    def semantic_compare(text1, text2):
        lang1 = Language.detect_language(text1)
        lang2 = Language.detect_language(text2)
        Language.semantically_similar(text1, text2)
        
        # if lang1 != lang2:
        #     words1 = len(text1.split())
        #     words2 = len(text2.split())
        #     if (words2 < 4):
        #         lang2 = lang1
        #         if (words1 < 4):
        #             lang1 = lang2
        #         else:
        #             lang2 = lang1
        #         raise DifferentLanguagesException(f"Different languages detected: {lang1}, {lang2}")
        # if lang1 == 'en':
        #     return Language.compute_semantic_similarity(text1, text2, 'english') > 0.1
                 
        # elif lang1 == 'es':
        #     return Language.compute_semantic_similarity(text1, text2, 'spanish') > 0.1
        # else:
        #     raise NotImplementedError(f"Semantic comparison not implemented for language: {lang1}")
        
    @staticmethod
    def get_similarity_score(text1, text2, lang='en'):
        """
        Compute and return the semantic similarity score between two texts.
        """
        return Language.compute_semantic_similarity(text1, text2, lang)

# Example usage
#try:
#    similarity_score = Language.semantic_compare("This is a sample text.", "This is another example text.")
#    print(f"Semantic Similarity Score: {similarity_score}")
#except DifferentLanguagesException as e:
#    print(e)
#except NotImplementedError as e:
#    print(e)
