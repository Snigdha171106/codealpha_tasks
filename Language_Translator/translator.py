# ============================================================
# translator.py
# Handles all translation and text-to-speech (TTS) functionality.
# ============================================================

import io
import logging

from deep_translator import GoogleTranslator
from gtts import gTTS

from languages import get_language_name, CODE_TO_LANGUAGE

# Configure module-level logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------

def translate_text(text: str, source_lang: str, target_lang: str) -> dict:
    """Translate *text* from *source_lang* to *target_lang*.

    Uses the deep-translator library which wraps Google Translate under the
    hood — no paid API key is required for moderate usage.

    Args:
        text:        The string to translate.
        source_lang: ISO 639-1 source code (e.g. "en").
        target_lang: ISO 639-1 target code (e.g. "fr").

    Returns:
        A dict with keys:
            "success"          (bool)
            "translated_text"  (str)  — populated on success
            "error"            (str)  — populated on failure
    """
    result = {
        "success": False,
        "translated_text": "",
        "error": "",
    }

    # ── Guard: empty input ──────────────────────────────────────────────────
    stripped = text.strip()
    if not stripped:
        result["error"] = "Please enter some text to translate."
        return result

    # ── Guard: source == target (skip unnecessary API call) ─────────────────
    if source_lang == target_lang:
        result["success"] = True
        result["translated_text"] = stripped
        return result

    # ── Perform translation ─────────────────────────────────────────────────
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(stripped)

        if translated is None or translated == "":
            result["error"] = (
                "Translation returned an empty result. "
                "Please try again or use a different language pair."
            )
            return result

        result["success"] = True
        result["translated_text"] = translated

    except Exception as exc:  # noqa: BLE001
        logger.error("Translation error: %s", exc, exc_info=True)
        result["error"] = (
            f"Translation failed: {exc}\n\n"
            "Possible reasons: no internet connection, "
            "unsupported language pair, or API limit reached."
        )

    return result


# ---------------------------------------------------------------------------
# Text Statistics
# ---------------------------------------------------------------------------

def compute_statistics(source_text: str, translated_text: str) -> dict:
    """Return word / character counts for both source and translated text.

    Args:
        source_text:     Original input string.
        translated_text: Translated output string.

    Returns:
        Dict with keys:
            "source_chars", "source_words",
            "translated_chars", "translated_words"
    """
    src = source_text.strip()
    tgt = translated_text.strip()
    return {
        "source_chars": len(src),
        "source_words": len(src.split()) if src else 0,
        "translated_chars": len(tgt),
        "translated_words": len(tgt.split()) if tgt else 0,
    }


# ---------------------------------------------------------------------------
# Text-to-Speech
# ---------------------------------------------------------------------------

def text_to_speech(text: str, language_code: str) -> bytes | None:
    """Convert *text* to MP3 audio bytes using gTTS.

    Args:
        text:          The string to convert to speech.
        language_code: ISO 639-1 code for the language (e.g. "fr").
                       "auto" is not valid here; pass a concrete code.

    Returns:
        Raw MP3 bytes on success, or ``None`` on failure.
    """
    if not text.strip():
        logger.warning("TTS called with empty text.")
        return None

    # Some codes used by deep-translator include region (e.g. "zh-cn").
    # gTTS accepts "zh-CN" style — keep as-is; gTTS handles most variants.
    lang = language_code
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read()
    except Exception as exc:  # noqa: BLE001
        logger.error("TTS error for lang '%s': %s", lang, exc, exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def is_rtl_language(language_code: str) -> bool:
    """Return True if the language is right-to-left (RTL).

    Used by the UI to apply correct text direction.

    Args:
        language_code: ISO 639-1 code.

    Returns:
        True if RTL, False otherwise.
    """
    RTL_CODES = {"ar", "he", "fa", "ur", "yi", "dv", "ps"}
    return language_code in RTL_CODES
