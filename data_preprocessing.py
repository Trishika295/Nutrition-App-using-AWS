import pandas as pd
import re

# Load raw data
df = pd.read_csv("raw_data.csv")

# Drop missing values
df.dropna(inplace=True)

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Clean food names
def clean_food_name(name):
    name = str(name).lower()
    name = re.sub(r'[^a-z\s]', '', name)  # remove punctuation/numbers
    return name.strip()

df["food_clean"] = df["food"].apply(clean_food_name)

# Save cleaned dataset
df.to_csv("nutrition_clean.csv", index=False)
print("Cleaned dataset saved to nutrition_clean.csv")


# ================== ADD BELOW (DO NOT CHANGE ABOVE CODE) ==================

# Select only required columns
required_cols = ["food", "calories", "protein", "carbs", "fats"]
df = df[required_cols]

# Remove duplicates (based on food name)
df = df.drop_duplicates(subset="food")

# Convert numeric columns properly
for col in ["calories", "protein", "carbs", "fats"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with invalid numeric values
df = df.dropna()

# 🔥 Improved Variation Logic (REALISTIC VALUES)

variation_factors = {
    "Raw": 1.0,
    "Boiled": 0.95,
    "Cooked": 0.90,
    "Grilled": 0.92
}

expanded_rows = []

for _, row in df.iterrows():
    for var, factor in variation_factors.items():
        new_row = row.copy()
        new_row["food"] = f"{row['food']} ({var})"

        # Apply variation to nutrients
        new_row["calories"] = round(row["calories"] * factor, 2)
        new_row["protein"] = round(row["protein"] * factor, 2)
        new_row["carbs"] = round(row["carbs"] * factor, 2)
        new_row["fats"] = round(row["fats"] * factor, 2)

        expanded_rows.append(new_row)

# Convert to DataFrame
expanded_df = pd.DataFrame(expanded_rows)

# Combine original + expanded
df_final = pd.concat([df, expanded_df])

# Remove duplicates again
df_final = df_final.drop_duplicates(subset="food")

# Reset index (clean output)
df_final = df_final.reset_index(drop=True)

# Save final processed dataset
df_final.to_csv("processed_data.csv", index=False)

print("✅ Processed dataset saved to processed_data.csv")