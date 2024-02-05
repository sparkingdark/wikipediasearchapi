import json
from typing import List
class JSONSearchHistory:
    def __init__(self, filename='search_history.json'):
        self.filename = filename
        self.search_history = self.load_history()

    def load_history(self) -> List[str]:
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_history(self):
        with open(self.filename, 'w') as file:
            json.dump(self.search_history, file)

    def add_to_history(self, topic: str):
        self.search_history.append(topic)
        self.save_history()

    def get_history(self) -> List[str]:
        return self.search_history