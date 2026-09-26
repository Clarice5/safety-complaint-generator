def get_safety_advice(category: str, language: str = "Hindi") -> str:
    """
    Return safety advice based on complaint category and language.
    """

    advice_hindi = {
        "Blackmail": "ब्लैकमेल करने वाले व्यक्ति को पैसे या कोई अन्य लाभ न दें। संदेश, कॉल रिकॉर्ड और अन्य सबूत सुरक्षित रखें तथा पुलिस या साइबर अपराध प्राधिकरण से संपर्क करें।",
        "Eve Teasing": "यदि आपको सार्वजनिक स्थान पर परेशान किया जा रहा है, तो किसी सुरक्षित स्थान पर जाएं और आसपास के लोगों या पुलिस से सहायता लें।",
        "Harassment": "उत्पीड़न की घटनाओं का रिकॉर्ड और संबंधित संदेश सुरक्षित रखें। यदि उत्पीड़न जारी रहता है, तो पुलिस या संबंधित प्राधिकरण से सहायता लें।",
        "Domestic Violence": "यदि आपको घर में हिंसा का खतरा है, तो पहले किसी सुरक्षित स्थान पर जाएं। किसी विश्वसनीय व्यक्ति, स्थानीय पुलिस या महिला हेल्पलाइन (181) से संपर्क करें।",
        "Public Safety": "सार्वजनिक स्थान पर खतरा महसूस होने पर सुरक्षित स्थान पर जाएं। आवश्यकता होने पर आपातकालीन सेवा (112) से संपर्क करें।",
        "Threat": "यदि आपको धमकी दी जा रही है, तो उससे संबंधित संदेश या कॉल रिकॉर्ड सुरक्षित रखें। तत्काल खतरा होने पर पुलिस से संपर्क करें।",
        "Stalking": "यदि कोई व्यक्ति आपका लगातार पीछा कर रहा है, तो घटनाओं का रिकॉर्ड रखें और अकेले सामना करने से बचें। तुरंत पुलिस सहायता लें।",
        "Cyber Harassment": "ऑनलाइन उत्पीड़न करने वाले व्यक्ति को जवाब देने से बचें। संदेश और स्क्रीनशॉट सुरक्षित रखें तथा cybercrime.gov.in पर शिकायत दर्ज करें।",
        "Theft": "चोरी की घटना होने पर घटनास्थल और उपलब्ध सबूतों को सुरक्षित रखें। जितनी जल्दी हो सके स्थानीय पुलिस में शिकायत (FIR) दर्ज करें।",
        "Other": "घटना से संबंधित सभी महत्वपूर्ण जानकारी और सबूत सुरक्षित रखें। यदि खतरा महसूस हो, तो पुलिस या संबंधित प्राधिकरण से संपर्क करें।"
    }

    advice_english = {
        "Blackmail": "Do not pay or yield to demands. Preserve all messages, call logs, and evidence, and report to the police or cybercrime portal immediately.",
        "Eve Teasing": "Move to a crowded or safe area immediately. Seek help from bystanders or contact the emergency police helpline (112).",
        "Harassment": "Keep written records and screenshots of all harassing communications. Report the matter to local authorities or HR/ICC if workplace-related.",
        "Domestic Violence": "Ensure your immediate safety first. Reach out to trusted relatives, local police, or the national women helpline (181).",
        "Public Safety": "Move to a secure location if you feel unsafe in public. Contact local emergency authorities immediately.",
        "Threat": "Preserve all threat communications (texts, audio, emails). Do not confront the individual alone and inform local police.",
        "Stalking": "Avoid isolated areas, inform friends/family of your movement, and register an official complaint with local law enforcement.",
        "Cyber Harassment": "Do not engage or respond to the harasser. Block the user, save screenshots as evidence, and report at cybercrime.gov.in.",
        "Theft": "Preserve the crime scene where applicable, gather proof of ownership, and lodge an FIR at the nearest police station immediately.",
        "Other": "Keep all evidence safe. If you feel you are in danger, move to a safe location and contact emergency authorities immediately."
    }

    if language.lower() == "english":
        return advice_english.get(category, advice_english["Other"])
    
    return advice_hindi.get(category, advice_hindi["Other"])