# emotion_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib as jb
from flask_sqlalchemy import SQLAlchemy
import os

class EmotionModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = SVC(kernel='linear')
        # Initialize the database for the emotion model
        # with db.app.app_context():
        #     db.create_all()

    def train(self, X, y):
        X_tfidf = self.vectorizer.fit_transform(X)
        self.model.fit(X_tfidf, y)

    def predict(self, text):
        text_tfidf = self.vectorizer.transform([text])
        prediction = self.model.predict(text_tfidf)
        return prediction[0]

    def save_model(self, filename='emotion_model.pkl'):
        jb.dump((self.vectorizer, self.model), filename)

    def load_model(self, filename='emotion_model.pkl'):
        self.vectorizer, self.model = jb.load(filename)