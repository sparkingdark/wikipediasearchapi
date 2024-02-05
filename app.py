import nltk
import json
import wikipedia
from uuid import uuid4
from loguru import logger
from nltk.corpus import stopwords
from fastapi import FastAPI
from analyzer import analysze_text, wikipedia_content
from models import WordFrequencyAnalysisTopicModel
from history import JSONSearchHistory





app = FastAPI(
   description="A api to provide word frequency analysis of a subject and search history endpoint from the wikipedia." 
)

try:
    nltk.data.find('tokenizers/punkt')
    stopwords.words('english')
except (LookupError, FileNotFoundError):
    nltk.download('punkt')
    nltk.download('stopwords')

json_search_history = JSONSearchHistory()




    

    


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