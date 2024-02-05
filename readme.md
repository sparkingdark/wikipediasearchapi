# FastAPI Word Frequency Analysis API

This is a FastAPI application that performs word frequency analysis on articles fetched from Wikipedia based on a specific topic.

## API Details

### Analyze Word Frequency

Endpoint: `/wordfrequencyanalysis`

- **Method**: POST
- **Request Body**: JSON with `topic` (str) and `n` (int) representing the subject of the article and the number of top words to analyze.
- **Example Request**:

  ```json
  {
    "topic": "Natural Language Processing",
    "n": 10
  }
  ```
- **Example Response**:
  
  ```json
  {
  "topic": "Natural Language Processing",
  "id": "3e2b493a-814e-4a41-81c8-6876ea29e13b",
  "top_words": [
    {"word": "language", "count": 35},
    {"word": "processing", "count": 25},
    {"word": "natural", "count": 20},
    ...
  ]
  }

### Search History

EndPoint: `/searchhistory`
- **Method**: GET
- **Request Body**: Just the get request to the api.

- **Example Response**:
  
  ```json
    [
    {"topic": "Natural Language Processing", "n": 10},
    {"topic": "Machine Learning", "n": 5, "id": "3e2b493a-814e-4a41-81c8-6876ea29e13b", "top_words": [...]},
    ...
    ]



## Setup and Run

### Using Docker Compose

1. Clone the repository and go to the directory.

```bash
git clone https://github.com/your-username/your-fastapi-app.git
cd your-fastapi-app

```

2. Then run `docker-compose up -d`

4. Access the FastAPI application at http://localhost:8000/docs/.

5. To stop and remove the containers: `docker-compose down`


### Using Python

1. Clone the repository and go to the directory.

```bash
git clone https://github.com/your-username/your-fastapi-app.git
cd your-fastapi-app

```

2. Then run `pip3 install -r requirements.txt`

3. Then just `uvicorn app:app --reload`

4. Access the FastAPI application at `http://localhost:8000/docs/` .


