class News:
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], dict):
            # If the first argument is a dictionary, use it to set attributes
            news_data = args[0]
            self.id = news_data.get("id")
            self.title = news_data.get("title")
            self.body = news_data.get("body")
            self.url = news_data.get("url")
            self.category = news_data.get("category")
        else:
            # Otherwise, expect individual parameters
            self.id, self.title, self.body, self.url, self.category = args

    def __str__(self):
        return f"News(id={self.id}, title={self.title}, category={self.category}, url={self.url})"

    def __repr__(self):
        return self.__str__()