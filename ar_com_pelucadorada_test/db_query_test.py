# test_db_query.py

import pytest
from tinydb import TinyDB, Query

@pytest.fixture
def db():
    # Setup: create a database connection
    test_db = TinyDB('ar_com_pelucadorada_data/website_content.json')

    # This setup can also include populating the database with test data

    yield test_db  # This will be passed to your test functions

    # Teardown: close database connection or clean up
    test_db.close()

def test_fetch_news_by_id(db):
    query = Query()
    test_id = "e89fbb1c12d85f66799abb2fb44100ae"
    
    all_records = db.all()
    print("All Records:", all_records)  # This will print all records in the database for inspection

    result = db.search(query.news_id == test_id)
    print("Search Result:", result)  # This will print the result of the search query

    assert len(result) > 0, f"No records found for given ID: {test_id}"


def test_fetch_any_news(db):
    # Fetching any record from the database
    result = db.all()  # Using .all() to get all records in the database

    assert len(result) > 0, "No records found in the database"
