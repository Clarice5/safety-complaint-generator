import pandas as pd

from app.preprocessing.english_preprocessing import preprocess_english


# Load the dataset
df = pd.read_csv("dataset/english_dataset.csv")


# Store word counts
original_counts = []
processed_counts = []


# Preprocess all complaints
for complaint in df["complaint"]:
    processed = preprocess_english(complaint)

    original_word_count = len(complaint.split())
    processed_word_count = len(processed.split())

    original_counts.append(original_word_count)
    processed_counts.append(processed_word_count)


# Calculate averages
average_original = sum(original_counts) / len(original_counts)
average_processed = sum(processed_counts) / len(processed_counts)

average_removed = average_original - average_processed
percentage_removed = (average_removed / average_original) * 100


print("===== PREPROCESSING STATISTICS =====")

print(f"Total complaints: {len(df)}")

print(f"Average original words: {average_original:.2f}")

print(f"Average processed words: {average_processed:.2f}")

print(f"Average words removed: {average_removed:.2f}")

print(f"Percentage of words removed: {percentage_removed:.2f}%")