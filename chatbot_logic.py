import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# -------------------------------
# NLTK Setup
# -------------------------------
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("processed_data.csv")

with open("intents.json") as file:
    intents = json.load(file)

# -------------------------------
# FAQ Dictionary
# -------------------------------
faq = {
    "how many calories in rice": "One cup of cooked rice has about 200 calories.",
    "how many calories in banana": "One medium banana has about 105 calories.",
    "how many calories in apple": "One medium apple has about 95 calories.",
    "balanced diet": "A balanced diet includes carbs, protein, fats, vitamins, and minerals.",
    "protein per day": "Typically 0.8–1.2g per kg body weight.",
    "healthy fats": "Avocados, nuts, seeds, olive oil, and fish.",
    "carbs bad": "No, whole carbs are healthy.",
    "weight loss foods": "Fruits, vegetables, oats, lean protein.",
    "breakfast": "Oats, eggs, fruits, yogurt.",
    "gain weight": "Increase calories using nuts, dairy, whole grains.",
    "build muscle": "High protein foods like chicken, eggs, paneer."
}

# -------------------------------
# NLP Keyword Extraction
# -------------------------------
def extract_keywords(text):
    words = word_tokenize(text.lower())
    keywords = [w for w in words if w.isalnum() and w not in stop_words]
    return keywords

# -------------------------------
# FAQ Matching (NLP)
# -------------------------------
def match_faq(user_input):
    keywords = extract_keywords(user_input)

    best_match = None
    max_score = 0

    for question in faq:
        q_words = question.split()

        # Count matching words
        score = sum(1 for word in keywords if word in q_words)

        if score > max_score:
            max_score = score
            best_match = question

    # Only return if meaningful match
    if max_score >= 2:
        return faq[best_match]

    return None


# -------------------------------
# Intent Matching (NLP)
# -------------------------------
def find_intent(user_input):

    keywords = extract_keywords(user_input)

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = pattern.lower().split()

            if any(word in keywords for word in pattern_words):
                return intent["tag"], intent.get("response", "Here are some suggestions:")

    return None, None

# -------------------------------
# Recommendations
# -------------------------------
def get_recommendations(tag):

    if tag == "high_protein":
        result = df[df["protein"] > 15]

    elif tag == "low_calorie":
        result = df[df["calories"] < 100]

    elif tag == "weight_loss":
        result = df[(df["calories"] < 150) & (df["fats"] < 10)]

    elif tag == "muscle_gain":
        result = df[(df["protein"] > 15) & (df["calories"] > 200)]

    elif tag == "low_carb":
        result = df[df["carbs"] < 20]

    elif tag == "low_fat":
        result = df[df["fats"] < 5]

    else:
        return None

    return result[["food", "calories", "protein"]].head(5)

# -------------------------------
# Smart Food Search (NLP)
# -------------------------------
def search_food(query):
    keywords = extract_keywords(query)

    result = df[df["food"].str.lower().apply(
        lambda x: any(word in x for word in keywords)
    )]

    return result[["food", "calories", "protein"]].head(5)

# -------------------------------
# FINAL Chatbot Response
# -------------------------------
def chatbot_response(user_input):

    # ✅ FAQ first
    faq_answer = match_faq(user_input)
    if faq_answer:
        return {
            "text": faq_answer,
            "table": None
        }

    # ✅ Intent next
    tag, response = find_intent(user_input)

    if tag:
        recs = get_recommendations(tag)

        if recs is not None and not recs.empty:
            return {
                "text": response,
                "table": recs
            }
        else:
            return {
                "text": response,
                "table": None
            }

    # ✅ Search fallback
    search_result = search_food(user_input)

    if not search_result.empty:
        return {
            "text": "Here are some matching foods:",
            "table": search_result
        }

    # ✅ Default fallback
    return {
        "text": "Sorry, I couldn't understand. Try asking about food, calories, or diet.",
        "table": None
    }