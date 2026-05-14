import random

# Sample meal library
meals = {
    "breakfast": ["Oats with milk", "Eggs & toast", "Smoothie"],
    "lunch": ["Rice & chicken", "Quinoa salad", "Fish curry"],
    "dinner": ["Roti & paneer", "Vegetable stir-fry", "Grilled salmon"],
    "snacks": ["Nuts", "Yogurt", "Fruit bowl"]
}

def generate_plan(weight, goal, duration_weeks=2):
    plan = []
    calorie_target = 2000  

    if goal == "Lose Weight":
        calorie_target -= 500
    elif goal == "Gain Weight":
        calorie_target += 300

    for day in range(duration_weeks * 7):
        plan.append({
            "day": day + 1,
            "breakfast": random.choice(meals["breakfast"]),
            "lunch": random.choice(meals["lunch"]),
            "dinner": random.choice(meals["dinner"]),
            "snacks": random.choice(meals["snacks"]),
            "calories_target": calorie_target
        })
    return plan

if __name__ == "__main__":
    sample_plan = generate_plan(70, "Lose Weight")
    for day in sample_plan:
        print(day)
