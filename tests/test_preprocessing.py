from app.preprocessing.english_preprocessing import preprocess_english


complaint = "My neighbor is threatening me and sending abusive messages!"

result = preprocess_english(complaint)

print("Original:")
print(complaint)

print("\nPreprocessed:")
print(result)