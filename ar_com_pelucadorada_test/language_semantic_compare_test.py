import os
import pytest
from tinydb import TinyDB
from ar_com_pelucadorada_language.Language import Language
from news_iterator import create_associations


# Test for language detection
def test_language_detection():
    english_text = "This is a sample sentence in English."
    spanish_text = "Esto es una frase de ejemplo en Español."

    assert Language.detect_language(english_text) == 'en'
    assert Language.detect_language(spanish_text) == 'es'

# Test for semantic comparison - same language
def test_semantic_comparison_same_language():
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "A fast brown fox leaps over a sleepy dog."

    # Assuming your semantic comparison returns a boolean or a similarity score
    # Adjust the assertion based on the actual return type of semantic_compare
    similarity_score = Language.semantic_compare(text1, text2)
    assert similarity_score > 0.2  # Adjust the threshold as needed

# Test for semantic comparison - different languages
def test_semantic_comparison_different_language():
    english_text = "This is a sample sentence in English."
    spanish_text = "Esto es una frase de ejemplo en Español."

    with pytest.raises(Exception):  # Replace Exception with your specific exception type
        Language.semantic_compare(english_text, spanish_text)

# Add more tests as needed to cover different scenarios and edge cases

# Test for semantic comparison - same language (Spanish)
def test_semantic_comparison_same_language_spanish():
    text1 = "El rápido zorro marrón salta sobre el perro perezoso."
    text2 = "Un ágil zorro marrón brinca sobre un perro dormido."

    # Assuming your semantic comparison returns a similarity score
    # Adjust the assertion based on the actual return type of semantic_compare
    similarity_score = Language.semantic_compare(text1, text2)
    assert similarity_score > 0.3  # Adjust the threshold as needed


def test_create_associations():
    # Setup: Clear the existing database if it exists
    db_path = '../ar_com_pelucadorada_data/news_semantic_association.json'
    if os.path.exists(db_path):
        os.remove(db_path)
    # Run the function to create associations
    create_associations()
    # Test: Check if the database is not empty
    db = TinyDB(db_path)
    assert len(db) > 0, "The database should not be empty after running create_associations"
    # Cleanup: Optionally, you can delete the test database after the test
    os.remove(db_path)