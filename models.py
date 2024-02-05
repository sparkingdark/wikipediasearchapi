from pydantic import BaseModel

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
