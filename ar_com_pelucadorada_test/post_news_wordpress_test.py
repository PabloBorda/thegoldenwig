import pytest
from Wordpress import WordPress
from News import News

class TestWordPress:
    @pytest.fixture
    def wordpress_instance(self):
        # Replace with your test WordPress instance details
        return WordPress("https://yourtestwordpresssite.com", "test_username", "test_app_password")

    @pytest.fixture
    def sample_news(self):
        # Create a sample news item for testing
        return News("Test News Title", "This is a test news body.", "path/to/test/image.jpg")

    def test_post_news(self, wordpress_instance, sample_news):
        # Mock the WordPress API response
        # You should mock the requests.post method here to avoid actual network requests
        response = wordpress_instance.post_news(sample_news)

        # Assert that the response is successful (you might need to adjust this based on your mock setup)
        assert response.status_code == 201


    def test_activate_theme(wordpress_instance):
        site_url = 'http://example.com'
        username = 'admin'
        password = 'password'
        theme_name = 'twentytwentyone'

        with requests_mock.Mocker() as m:
            # Mock the request for retrieving themes
            m.get(f'{site_url}/wp-json/wp/v2/themes', json=[{'slug': theme_name, 'id': 123}])

            # Mock the request for activating the theme
            m.post(f'{site_url}/wp-json/wp/v2/themes/123', json={'status': 'active'})

            # Call the activate_theme method
            result = wordpress_instance.activate_theme(site_url, username, password, theme_name)

            assert result == True
