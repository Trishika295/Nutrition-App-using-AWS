import joblib
import numpy as np

# Load trained model
model = joblib.load('calorie_predictor.pkl')

# Example input
input_data = np.array([[30, 50, 20]])  # protein, carbs, fats
prediction = model.predict(input_data)

print(f'Predicted calories: {prediction[0]:.2f}')
