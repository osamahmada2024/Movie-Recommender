# Movie Recommender System

A lightweight, content-based movie recommender that processes movie metadata [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata], generates semantic embeddings, and serves personalized recommendations through a local Flask web interface.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the server:

```bash
python app.py
```

Then open the app in your browser at:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Structure

* **data/** – movie datasets
* **artifacts/** – models and similarity files
* **app.py** – main web application
* **notebook/movie-recommender.ipynb** – Jupyter Notebook with preprocessing and recommendation examples

## Notes

* Supports semantic tag embeddings
* Works fully offline after setup
* Can be extended with additional models or datasets
* Data extracted from `https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata`
