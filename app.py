import nltk
import json
import wikipedia
from uuid import uuid4
from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from typing import Dict,Any,Union,List


class WordFrequencyAnalysisTopicModel(BaseModel):
    """
    A model for analyzing word frequency in a given article based on a specific topic.

    Args:
        topic (str): The subject of the article to be fetched from Wikipedia.
        n (int): The number of top words by frequency to be extracted from the article.

    Example:
        To analyze the top 10 words in an article about "Natural Language Processing":
        >>> model = WordFrequencyAnalysisTopicModel(topic="Natural Language Processing", n=10)
        >>> result = analyze_article(model)
        >>> print(result)
        {'word': 'frequency'}
    """
    topic: str
    n: int


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

json_search_history = JSONSearchHistory()
app = FastAPI(
   description="A api to provide word frequency analysis of a subject and search history endpoint from the wikipedia." 
)

try:
    nltk.data.find('tokenizers/punkt')
    stopwords.words('english')
except (LookupError, FileNotFoundError):
    nltk.download('punkt')
    nltk.download('stopwords')




def wikipedia_content(topic: str) -> Union[str, Dict[str, Union[str, List[str]]]]:
    try:
        content = wikipedia.page(topic).content
        return content
    except wikipedia.exceptions.DisambiguationError as e:
        logger.error(f"DisambiguationError: {e}")
        error_data = {"error": "Exact topic is not available, pass any topics available from the options.", "options": e.options,"id":str(uuid4())}
        json_search_history.add_to_history(json.dumps(error_data))
        return error_data
    except Exception as e:
        logger.error(f"Error fetching Wikipedia page: {e}")
        error_data = {"error": "Error fetching Wikipedia page","id":str(uuid4())}
        json_search_history.add_to_history(json.dumps(error_data))
        return error_data
    

def analysze_text(text:str,topic:str,n:int):
    # Tokenize the text and remove stopwords
    tokens = [word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stopwords.words('english')]
    # Use Counter to count word occurrences
    word_counts = Counter(tokens)
    # Get the top n words
    top_n_words = word_counts.most_common(n)
    # Log the top words
    logger.info(f"Top {n} words for topic '{topic}': {top_n_words}")

    top_n_words_response = {"topic":topic,"id":str(uuid4()),"top_words": [{"word": word, "count": count} for word, count in top_n_words],}
    return top_n_words_response

    

    


@app.post("/wordfrequencyanalysis")
def word_frequency_analysis(data: WordFrequencyAnalysisTopicModel):
    json_search_history.add_to_history(json.dumps(data.dict()))
    topic = data.topic
    n_words = data.n

    if n_words == 0:
        return {
            "error":"number of the common words should be greater than zero"
        }
    
    text = wikipedia_content(topic)
    if type(text) == dict:
        return text
    top_words = analysze_text(text,topic,n_words)
    json_search_history.add_to_history(json.dumps(top_words))
    return top_words

@app.get("/searchhistory")
def search_history():
    history = [json.loads(item) for item in json_search_history.get_history()]
    return history