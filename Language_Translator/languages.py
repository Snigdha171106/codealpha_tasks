# ============================================================
# languages.py
# Stores all supported language names and their ISO 639-1 codes.
# Easy to extend — just add more entries to LANGUAGES dict.
# ============================================================

# Maps human-readable language names → Google Translate language codes
LANGUAGES: dict[str, str] = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Arabic": "ar",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Marathi": "mr",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
}

# Inverted map: code → name  (useful for reverse-lookups)
CODE_TO_LANGUAGE: dict[str, str] = {v: k for k, v in LANGUAGES.items()}

# Both source and target use the same full language list
SOURCE_LANGUAGE_OPTIONS: list[str] = list(LANGUAGES.keys())
TARGET_LANGUAGE_OPTIONS: list[str] = list(LANGUAGES.keys())


def get_language_code(language_name: str) -> str:
    """Return the ISO code for a given language name.

    Args:
        language_name: Human-readable language name (e.g. "French").

    Returns:
        Corresponding ISO 639-1 code string (e.g. "fr").

    Raises:
        ValueError: If the language name is not in the supported list.
    """
    if language_name not in LANGUAGES:
        raise ValueError(f"Unsupported language: '{language_name}'")
    return LANGUAGES[language_name]


def get_language_name(language_code: str) -> str:
    """Return the human-readable name for a given ISO code.

    Args:
        language_code: ISO 639-1 code (e.g. "fr").

    Returns:
        Human-readable language name (e.g. "French"), or the raw code
        if no matching name is found.
    """
    return CODE_TO_LANGUAGE.get(language_code, language_code.upper())
