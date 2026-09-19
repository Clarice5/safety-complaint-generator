function copyText(elementId) {

    const text = document.getElementById(elementId).innerText;

    navigator.clipboard.writeText(text);

    alert("Complaint copied successfully!");
}

// Hindi keyboard character set (consonants, vowels, numerals, common punctuation)
const hindiCharacters = [
    // Vowels (स्वर)
    "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ",
    // Consonants (व्यंजन) — common ones
    "क", "ख", "ग", "घ", "च", "छ", "ज", "झ", "ट", "ठ", "ड", "ढ", "त", "थ", "द", "ध",
    "न", "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह",
    // Matras (vowel marks)
    "ा", "ि", "ी", "ु", "ू", "े", "ै", "ो", "ौ", "ं", "ः", "ँ",
    // Numerals
    "०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
    // Common punctuation
    "।", "॥", ",", "।", "?", "!", " "
];

function initializeHindiKeyboard() {

    const grid = document.getElementById("keyboardGrid");

    if (!grid || grid.dataset.initialized) return;

    grid.dataset.initialized = "true";

    hindiCharacters.forEach(char => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "keyboard-key";
        btn.textContent = char;
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            insertCharacterAtCursor(char);
        });
        grid.appendChild(btn);
    });
}

function insertCharacterAtCursor(char) {

    const textarea = document.getElementById("complaint");
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;

    textarea.value = text.substring(0, start) + char + text.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + char.length;
    textarea.focus();
}

function toggleHindiKeyboard() {

    const toggle = document.getElementById("toggleHindiKeyboard");
    const keyboard = document.getElementById("hindiKeyboard");

    if (!toggle || !keyboard) return;

    const isVisible = keyboard.style.display !== "none";

    if (isVisible) {
        keyboard.style.display = "none";
        toggle.textContent = "Enable Hindi Keyboard";
        toggle.classList.remove("active");
    } else {
        keyboard.style.display = "block";
        toggle.textContent = "Hide Hindi Keyboard";
        toggle.classList.add("active");
        initializeHindiKeyboard();
    }
}

// Text shown for each field, per language. The page title is intentionally
// left out of this object — it must always stay in English.
const translations = {
    English: {
        languageLabel: "Language",
        dateLabel: "Date",
        timeLabel: "Time",
        locationLabel: "Location",
        complaintLabel: "Complaint",
        complaintPlaceholder: "Enter your complaint here...",
        locationPlaceholder: "Enter location"
    },
    Hindi: {
        languageLabel: "भाषा",
        dateLabel: "तारीख",
        timeLabel: "समय",
        locationLabel: "स्थान",
        complaintLabel: "शिकायत",
        complaintPlaceholder: "अपनी शिकायत यहाँ दर्ज करें",
        locationPlaceholder: "स्थान दर्ज करें"
    }
};

function applyLanguage(lang) {

    const t = translations[lang] || translations.English;

    const languageLabel = document.getElementById("languageLabel");
    const dateLabel = document.getElementById("dateLabel");
    const timeLabel = document.getElementById("timeLabel");
    const locationLabel = document.getElementById("locationLabel");
    const complaintLabel = document.getElementById("complaintLabel");
    const complaintField = document.getElementById("complaint");
    const locationField = document.getElementById("location");

    if (languageLabel) languageLabel.textContent = t.languageLabel;
    if (dateLabel) dateLabel.textContent = t.dateLabel;
    if (timeLabel) timeLabel.textContent = t.timeLabel;
    if (locationLabel) locationLabel.textContent = t.locationLabel;
    if (complaintLabel) complaintLabel.textContent = t.complaintLabel;
    if (complaintField) complaintField.placeholder = t.complaintPlaceholder;
    if (locationField) locationField.placeholder = t.locationPlaceholder;
}

document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const submitButton = document.getElementById("submitButton");

    const loadingMessage = document.getElementById("loadingMessage");

    const languageSelect = document.getElementById("language");


    // The language <select>, and therefore the whole form, only exists on
    // the "no result yet" page — guard everything so the results-only page
    // (where the form is hidden) doesn't throw errors.

    if (languageSelect) {

        applyLanguage(languageSelect.value);

        languageSelect.addEventListener("change", function () {
            applyLanguage(this.value);
        });

    }

    if (form) {

        form.addEventListener("submit", function () {

            submitButton.disabled = true;

            submitButton.innerText = "Processing...";

            loadingMessage.style.display = "block";

        });

    }

    const keyboardToggle = document.getElementById("toggleHindiKeyboard");
    if (keyboardToggle) {
        keyboardToggle.addEventListener("click", function (e) {
            e.preventDefault();
            toggleHindiKeyboard();
        });
    }

});