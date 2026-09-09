from app.preprocessing.hindi_preprocessing import preprocess_hindi


complaints = [
    "मुझे मेरे पड़ोसी द्वारा धमकी दी जा रही है।",
    "एक व्यक्ति मुझे लगातार परेशान कर रहा है!",
    "मेरे घर के पास चोरी की घटना हुई है।"
]


print("===== HINDI PREPROCESSING TEST =====")

for i, complaint in enumerate(complaints, start=1):

    result = preprocess_hindi(complaint)

    print(f"\nComplaint {i}:")
    print("Original:    ", complaint)
    print("Preprocessed:", result)