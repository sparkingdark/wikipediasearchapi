import wikipedia
import json
from uuid import uuid4
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from loguru import logger
from datetime import datetime
from typing import Union,List,Dict
from history import  JSONSearchHistory

json_search_history = JSONSearchHistory()

def wikipedia_content(topic: str) -> Union[str, Dict[str, Union[str, List[str]]]]:
    """
    Fetch content from Wikipedia based on the given topic.

    Args:
        topic (str): The subject of the Wikipedia article.

    Returns:
        Union[str, Dict[str, Union[str, List[str]]]]: Content of the Wikipedia article or error information.

    Raises:
        None
    """
    try:
        content = wikipedia.page(topic).content
        return content
    except wikipedia.exceptions.DisambiguationError as e:
        logger.error(f"DisambiguationError: {e}")
        error_data = {"error": "Exact topic is not available, pass any topics available from the options.", "options": e.options,"id":str(uuid4()),"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        json_search_history.add_to_history(json.dumps(error_data))
        return error_data
    except Exception as e:
        logger.error(f"Error fetching Wikipedia page: {e}")
        error_data = {"error": "Error fetching Wikipedia page","id":str(uuid4()),"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        json_search_history.add_to_history(json.dumps(error_data))
        return error_data
    

def analysze_text(text:str,topic:str,n:int):
    """
    Analyze the text content and extract the top n words by frequency.

    Args:
        text (str): The text content to analyze.
        topic (str): The topic of the analysis.
        n (int): The number of top words to extract.

    Returns:
        dict: Dictionary containing the topic, a unique identifier (id), and the top n words with their counts.

    Raises:
        None
    """
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
