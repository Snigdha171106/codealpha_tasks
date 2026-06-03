import json
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt")
nltk.download("stopwords")

with open("faq_data.json", "r") as file:
    faqs = json.load(file)

questions = [faq["question"] for faq in faqs]

stop_words = set(stopwords.words("english"))

def preprocess(text):
    words = word_tokenize(text.lower())

    words = [
        word
        for word in words
        if word.isalnum() and word not in stop_words
    ]

    return " ".join(words)

processed_questions = [
    preprocess(q)
    for q in questions
]

vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(
    processed_questions
)

def get_response(user_question):

    processed_input = preprocess(user_question)

    input_vector = vectorizer.transform(
        [processed_input]
    )

    similarities = cosine_similarity(
        input_vector,
        question_vectors
    )

    best_match_index = similarities.argmax()

    score = similarities[0][best_match_index]

    if score < 0.3:
        return (
            "I couldn't find a matching FAQ.\n\n"
            "Try asking about:\n"
            "• Orders\n"
            "• Shipping\n"
            "• Payments\n"
            "• Refunds\n"
            "• Support"
        )

    return faqs[best_match_index]["answer"]