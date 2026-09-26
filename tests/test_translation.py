from app.translation.translator import (
    translate_hindi_to_english,
    translate_english_to_hindi
)


print("===== TRANSLATION TEST =====")


# Hindi → English
hindi_text = "मुझे मेरे पड़ोसी द्वारा धमकी दी जा रही है।"

english_result = translate_hindi_to_english(hindi_text)

print("\n--- Hindi → English ---")
print("Hindi:")
print(hindi_text)

print("English:")
print(english_result)


# English → Hindi
english_text = "My neighbor is threatening me."

hindi_result = translate_english_to_hindi(english_text)

print("\n--- English → Hindi ---")
print("English:")
print(english_text)

print("Hindi:")
print(hindi_result)