# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from emotion_model import EmotionModel

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite database
db = SQLAlchemy(app)
emotion_model = EmotionModel()

# Define a simple database model for storing chat messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    sender = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_emotion', methods=['POST'])
def predict_emotion():
    data = request.json
    text = data['text']

    # Save the user's message to the database
    user_message = Message(content=text, sender='user')
    db.session.add(user_message)
    db.session.commit()

    # Predict emotion and save bot's response to the database
    prediction = emotion_model.predict(text)
    bot_response = f"I detected you're feeling {prediction}."
    bot_message = Message(content=bot_response, sender='bot')
    db.session.add(bot_message)
    db.session.commit()

    return jsonify({'emotion': prediction, 'response': bot_response})

if __name__ == '__main__':
    # Initialize the database
    db.create_all()

    # Replace with your actual training data
    X_train = ["I love this product", "I am feeling sad today", ...]
    y_train = ["happy", "sad", ...]

    # Train the model
    emotion_model.train(X_train, y_train)

    # Save the trained model
    emotion_model.save_model()

    # Run the Flask app
    app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite database
