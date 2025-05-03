class Database:
    def __init__(self):
        self.categories = {
            "1": {"name": "Девушки", "tag": "rating:safe"},
            "2": {"name": "Котики", "tag": "neko"},
            "3": {"name": "Мейд", "tag": "maid"}
        }

    def get_categories(self):
        return {k: v["name"] for k, v in self.categories.items()}

    def get_category(self, cat_id):
        return self.categories.get(cat_id)
