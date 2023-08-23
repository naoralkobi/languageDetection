from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load the dataset
data = pd.read_csv("dataset.csv")

# Split the data into features (X) and labels (y)
x = np.array(data["Text"])
y = np.array(data["language"])

# Create a Count Vectorized to convert text data to numerical features
cv = CountVectorizer()
X = cv.fit_transform(x)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.33,
                                                    random_state=42)

# Initialize and train the Multinomial Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train)


# Save the trained model to a file using pickle
with open('trained_model.pkl', 'wb') as file:
    pickle.dump(model, file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        input_text_length = len(input_text)

        # Load the trained model from the file
        with open('trained_model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)

        if input_text_length < 10:
            error_message = "The input text is too short."
            return render_template('result.html', error_message=error_message)

        else:
            # Perform language detection using the loaded model
            user_data = cv.transform([input_text]).toarray()

            predicted_language = loaded_model.predict(user_data)[0]
            return render_template('result.html', predicted_language=predicted_language)


@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        input_text = request.form.get('input_text')
        # Do something with the feedback and input text
        return render_template('feedback.html', feedback=feedback)


if __name__ == '__main__':
    app.run(debug=True)
