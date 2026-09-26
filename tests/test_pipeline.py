from app.pipeline.text_pipeline import process_complaint


print("===== LANGUAGE PROCESSING PIPELINE TEST =====")


# Hindi complaint
hindi_complaint = "मुझे मेरे पड़ोसी द्वारा धमकी दी जा रही है।"

hindi_result = process_complaint(
    hindi_complaint,
    "Hindi"
)

print("\n--- Hindi Complaint ---")
print("Original:")
print(hindi_result["original_text"])

print("\nHindi Preprocessed:")
print(hindi_result["hindi_processed"])

print("\nTranslated English:")
print(hindi_result["translated_text"])

print("\nEnglish Preprocessed:")
print(hindi_result["english_processed"])


# English complaint
english_complaint = "My neighbor is threatening me and sending abusive messages!"

english_result = process_complaint(
    english_complaint,
    "English"
)

print("\n\n--- English Complaint ---")
print("Original:")
print(english_result["original_text"])

print("\nEnglish Preprocessed:")
print(english_result["english_processed"])