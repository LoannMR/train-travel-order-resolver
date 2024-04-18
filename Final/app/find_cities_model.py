import pickle
from keras.models import load_model
import tensorflow as tf

vocabulary = {
    "O": 0,
    "B-TO": 1,
    "B-FROM": 2,
    "I-TO": 3,
    "I-FROM": 4,
    "PAD": 5
}

def custom_standardization(input_text):
    # Remove punctuations, but preserve apostrophes
    return tf.strings.regex_replace(input_text, "[^a-zA-Z0-9À-ÖØ-öø-ÿ' ]", "")

# load model
model_bi_gru = load_model('./models/model_bidirectional_gru.keras', custom_objects={'custom_standardization': custom_standardization})

# Define the reverse vocabulary mapping from integers to labels
reverse_vocabulary = {index: label for label, index in vocabulary.items()}

def make_prediction(sentence):
    pred = model_bi_gru.predict([sentence], verbose=0)[0]

    # calculate the real length of the sentence to remove the padding
    actual_length = len(sentence.split())

    predicted_tags = tf.argmax(pred, axis=-1).numpy()[:actual_length]

    labels = [reverse_vocabulary[index] for index in predicted_tags]

    return labels

def extract_predicted_cities(sentence: str, labels: list):
    """
    Extracts predicted cities from a sentence based on the provided labels.

    Args:
    - sentence (str): The input sentence.
    - labels (list): List of labels corresponding to each word in the sentence.

    Returns:
    - dict: A dictionary containing predicted cities categorized by label.
    """
    predicted_cities = {
        "B-TO": [],
        "B-FROM": [],
        "I-TO": [],
        "I-FROM": [],
    }

    # Split the sentence into words
    words = sentence.split()

    # Iterate through each label and its corresponding word
    for label, word in zip(labels, words):
        if label in predicted_cities:
            predicted_cities[label].append(word)

    return predicted_cities
