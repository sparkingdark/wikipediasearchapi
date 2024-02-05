import json
from typing import List
class JSONSearchHistory:
    """
    A class for managing and storing search history in a JSON file.

    Attributes:
        filename (str): The name of the JSON file to store the search history.
        search_history (List[str]): A list to store the search history.

    Methods:
        __init__: Initializes the JSONSearchHistory object.
        load_history: Loads the search history from the JSON file.
        save_history: Saves the search history to the JSON file.
        add_to_history: Adds a search topic to the search history.
        get_history: Retrieves the entire search history.

    Example:
        >>> search_history = JSONSearchHistory()
        >>> search_history.add_to_history("Python")
        >>> search_history.get_history()
        ['Python']
    """
    def __init__(self, filename='search_history.json'):
        self.filename = filename
        self.search_history = self.load_history()

    def load_history(self) -> List[str]:
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except Exception:
            return []

    def save_history(self):
        with open(self.filename, 'w') as file:
            json.dump(self.search_history, file)

    def add_to_history(self, topic: str):
        self.search_history.append(topic)
        self.save_history()

    def get_history(self) -> List[str]:
        return self.search_history