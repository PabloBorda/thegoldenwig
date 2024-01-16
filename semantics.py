import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (if not already done)
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Tokenize and lowercases the input text, removing stopwords.
    """
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in tokens if word.isalpha() and word not in stop_words])

def compute_semantic_similarity(text1, text2):
    """
    Compute the semantic similarity between two texts using cosine similarity of their TF-IDF vectors.
    """
    preprocessed_texts = [preprocess_text(text1), preprocess_text(text2)]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_texts)
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# Example usage
text1 = "Yesterday I sat over the table."
text2 = "Today I went running outside."

similarity_score = compute_semantic_similarity(text1, text2)
print(f"Semantic Similarity Score: {similarity_score}")
