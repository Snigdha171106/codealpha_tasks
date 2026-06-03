# CodeAlpha AI Internship 

**Snigdha Dashrath Kandikatla**
CodeAlpha AI Internship — June 2026
GitHub: https://github.com/Snigdha171106

---

## Task 1 — LinguaFlow: Language Translation Tool

LinguaFlow is a clean, fully functional language translation web app built from scratch using Python and Streamlit. It translates text across 57 languages, lets you listen to the translation out loud, and handles all the small things that make a tool actually pleasant to use — like swapping languages with one click, seeing word counts, and getting clear error messages when something goes wrong.

No API keys. No complicated setup. Just clone it, install three packages, and run it.

### What it can do

- Translate across 57 languages — from Afrikaans to Welsh, all the major ones are covered
- Text-to-Speech — hit the Listen button and hear the translated text read aloud
- Copy to Clipboard — one click and your translation is ready to paste anywhere
- Language Swap — flip source and target languages instantly without retyping anything
- Live stats — word count and character count update in real time for both input and output
- RTL support — Arabic, Hebrew, Urdu, Persian and others automatically flip to right-to-left layout
- Friendly error messages — empty input, failed API calls, bad language pairs — all handled gracefully
- One-click clear — reset everything and start fresh in a second

### Tech Stack

- **Frontend:** Streamlit, HTML, CSS, JavaScript
- **Backend:** Python
- **Libraries:** deep-translator, gTTS

### Getting it running

**Step 1 — Make sure Python is installed**

```bash
python --version
# Should say 3.10 or higher
```

**Step 2 — Clone the repo**

```bash
git clone https://github.com/Snigdha171106/Language-Translator.git
cd Language-Translator
```

**Step 3 — Set up a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**Step 4 — Install dependencies**

```bash
pip install -r requirements.txt
```

This installs Streamlit, deep-translator, and gTTS. Should take under a minute.

**Step 5 — Run it**

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

> **Note:** You need an active internet connection — translation and TTS both call Google's servers in real time.

### How to use it

1. Type or paste your text into the left panel
2. Pick your source language from the dropdown on the left
3. Pick your target language from the dropdown on the right
4. Hit **Translate**
5. The result appears instantly on the right
6. Want to hear it? Click **Listen (TTS)** — an audio player will appear below
7. Need to copy it? Click **Copy Text**
8. Want to flip the languages? Click the swap button `< >` — it also moves your translated text back into the input
9. Done? Hit **Clear All** to start fresh

### How it's built under the hood

**Session state** — Streamlit reruns the entire script on every interaction. All the app's data (current text, translation, audio bytes) lives in `st.session_state` so nothing gets wiped between button clicks.

**Modular design** — The UI (`app.py`), translation logic (`translator.py`), and language data (`languages.py`) are deliberately separated. If you want to swap Google Translate for DeepL tomorrow, you only touch one function in `translator.py`.

**RTL detection** — `is_rtl_language()` checks the target language code against a set of known RTL languages and adds a CSS class to the output box, which flips the text direction automatically.

**Clipboard copy** — Streamlit doesn't have a native clipboard API, so a tiny vanilla JavaScript snippet injected via `st.components.v1.html` handles the copy using the browser's `navigator.clipboard` API.

### What I'd add next

- File translation — drag in a `.txt` or `.pdf` and translate the whole thing
- Translation history — keep a log of past translations within the session
- Pinned language pairs — remember your favourite source/target combo
- Confidence scores — show how certain the translation engine is
- DeepL integration — optional higher-quality translation for supported languages

---

## Task 2 — FAQ Chatbot using NLP

An AI-powered FAQ Chatbot built using Python and Natural Language Processing. Designed to automatically answer frequently asked e-commerce customer support questions related to orders, shipping, payments, refunds, and account management.

Instead of relying on exact keyword matching, the chatbot uses TF-IDF Vectorization and Cosine Similarity to understand user queries and identify the closest matching FAQ. The app also has a simple graphical interface built with Tkinter for real-time interaction.

### Features

- Interactive chatbot interface
- NLP-based question matching
- FAQ dataset stored in JSON format
- Text preprocessing using NLTK
- TF-IDF Vectorization for text representation
- Cosine Similarity for intelligent FAQ matching
- Real-time chatbot responses
- Timestamped conversations
- Clear chat and save chat functionality
- Enter key support for quick interaction
- Scrollable chat window with a dark-themed interface

### Tech Stack

- **Language:** Python
- **NLP:** NLTK, TF-IDF Vectorization, Cosine Similarity
- **ML:** Scikit-Learn
- **GUI:** Tkinter
- **Data:** JSON

### How it works

1. FAQ data is loaded from a JSON file
2. Questions are preprocessed using NLTK
3. TF-IDF Vectorization converts text into numerical representations
4. Cosine Similarity calculates similarity between the user's query and stored FAQs
5. The most relevant FAQ is selected
6. The corresponding answer is displayed to the user
7. If no suitable match is found, the chatbot shows a fallback response

### Getting it running

```bash
git clone <repository-link>
cd FAQ-Chatbot

python -m venv venv
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python app.py
```

### Sample questions you can ask

- How can I track my order?
- What is your return policy?
- How do I reset my password?
- Can I cancel my order?
- Do you offer refunds?
- How can I contact customer support?
- Is cash on delivery available?
- How long does shipping take?

### What I'd add next

- Support for larger FAQ datasets
- Voice-based interaction
- Multi-language support
- Integration with web applications
- Machine Learning-based intent classification

---

## Task 3 — Real-Time Object Detection and Tracking using YOLOv8

This project performs real-time object detection and tracking using a webcam feed. It uses the YOLOv8 model to identify objects in each video frame and assigns unique tracking IDs to detected objects, allowing them to be tracked continuously as they move across the frame.

### Features

- Real-time video capture using OpenCV
- Object detection using a pre-trained YOLOv8 model
- Real-time object tracking with unique IDs
- Bounding box visualization around detected objects
- Object labels displayed on screen
- Live tracking of multiple objects simultaneously
- Lightweight and easy-to-use implementation

### Tech Stack

- **Language:** Python
- **Libraries:** OpenCV, YOLOv8 (Ultralytics), NumPy

### How it works

1. The webcam captures live video frames
2. Each frame is processed using the YOLOv8 model
3. Objects are detected and classified
4. Tracking IDs are assigned to detected objects
5. Bounding boxes, labels, and IDs are displayed on the video feed
6. The process continues in real time until the user exits

### Getting it running

```bash
git clone <repository-link>
cd Object_Detection_Tracking

python -m venv venv
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python main.py
```

Press **Q** to close the application window.

### Sample output

The system can detect and track common objects such as person, cell phone, bottle, laptop, backpack, chair, keyboard, and book. Detected objects are highlighted with bounding boxes and assigned unique tracking IDs for continuous tracking.

### Learning outcomes

Through this project, I gained practical experience in computer vision, real-time video processing, object detection and tracking, OpenCV integration, and working with pre-trained deep learning models.

---

## About

All three projects were developed as part of the **CodeAlpha AI Internship — June 2026**.

The goal across all tasks was to build things that are genuinely useful — tools I'd actually want to open, not just homework submissions.

⭐ Developed as part of the CodeAlpha AI Internship Program
