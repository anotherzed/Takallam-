import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import re
from difflib import SequenceMatcher

# --- CONFIG ---
st.set_page_config(page_title="Takallam!", page_icon="🎙️", layout="centered")

# --- KAHOOT STYLE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Nunito+Sans:wght@400;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&display=swap');

.ar {
    font-family: 'Amiri', 'Traditional Arabic', 'Times New Roman', serif !important;
    font-size: 1.05em;
    line-height: 1.75;
    direction: rtl;
    display: inline;
}

body, .stApp {
    background: #46178f !important;
    font-family: 'Nunito Sans', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

.kk-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 16px;
}
.kk-logo {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 28px;
    color: white;
    letter-spacing: -0.5px;
}
.kk-logo span { color: #f7c33f; }
.kk-badge {
    background: #f7c33f;
    color: #46178f;
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 14px;
    padding: 5px 14px;
    border-radius: 20px;
}
.kk-score-badge {
    background: rgba(255,255,255,0.18);
    color: white;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 14px;
    padding: 5px 14px;
    border-radius: 20px;
}
.kk-progress-wrap {
    background: rgba(255,255,255,0.2);
    border-radius: 6px;
    height: 10px;
    margin-bottom: 16px;
    overflow: hidden;
}
.kk-progress-fill {
    height: 100%;
    background: #f7c33f;
    border-radius: 6px;
    transition: width 0.4s;
}

/* Question card */
.kk-question-card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.28);
    margin-bottom: 12px;
}
.kk-question-text {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 19px;
    color: #222;
    line-height: 1.7;
    margin: 0;
    white-space: pre-line;
}
.kk-question-text .ar {
    font-size: 22px;
    font-weight: 700;
    display: block;
    margin-top: 6px;
}
.kk-dialog-box {
    background: #f4f0ff;
    border-left: 4px solid #46178f;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 12px 0 4px;
    text-align: right;
    direction: rtl;
    font-family: 'Amiri', 'Traditional Arabic', serif;
    font-size: 18px;
    line-height: 2.0;
    color: #333;
}
.kk-question-label {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 15px;
    color: #46178f;
    margin-top: 10px;
    text-align: center;
}

/* Clue box */
.kk-clue-box {
    background: rgba(255,255,255,0.13);
    border: 1.5px solid rgba(255,255,255,0.3);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.kk-clue-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 13px;
    color: #f7c33f;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}
.kk-clue-option {
    background: rgba(255,255,255,0.15);
    border-radius: 9px;
    padding: 9px 14px;
    font-family: 'Amiri', 'Traditional Arabic', serif;
    font-weight: 400;
    font-size: 19px;
    color: white;
    direction: rtl;
    text-align: right;
    line-height: 1.8;
}
.kk-clue-option span.label {
    float: left;
    direction: ltr;
    font-weight: 800;
    color: #f7c33f;
    font-size: 13px;
    margin-top: 2px;
}

/* Mic section */
.kk-mic-section {
    background: rgba(255,255,255,0.12);
    border-radius: 14px 14px 0 0;
    padding: 14px 16px 10px;
    text-align: center;
    margin-bottom: 0px;
}
.kk-mic-label {
    color: rgba(255,255,255,0.9);
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 4px;
}
.kk-mic-warn {
    color: #f7c33f;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 12px;
}

section[data-testid="stMain"] > div > div > div > div:has(> div[data-testid="stAudioRecorder"]) {
    margin-top: -2px;
    background: rgba(255,255,255,0.12);
    border-radius: 0 0 14px 14px;
    padding: 4px 16px 14px;
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
}

.kk-feedback-correct {
    background: #26890c;
    color: white;
    border-radius: 10px;
    padding: 13px 16px;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 15px;
    text-align: center;
    margin-bottom: 10px;
    direction: rtl;
    line-height: 1.7;
}
.kk-feedback-correct .ar, .kk-feedback-wrong .ar {
    font-family: 'Amiri', 'Traditional Arabic', serif !important;
    font-size: 19px;
    font-weight: 700;
}
.kk-feedback-wrong {
    background: #e21b3c;
    color: white;
    border-radius: 10px;
    padding: 13px 16px;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 15px;
    text-align: center;
    margin-bottom: 10px;
    direction: rtl;
    line-height: 1.7;
}

/* Next button */
div.stButton > button {
    background: #f7c33f !important;
    color: #46178f !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
    font-size: 16px !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 10px 28px !important;
    box-shadow: 0 4px 0 rgba(0,0,0,0.2) !important;
}
div.stButton > button:hover { filter: brightness(1.05) !important; }

/* Result screen */
.kk-result-screen {
    background: rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 32px 20px 24px;
    text-align: center;
    margin-bottom: 16px;
}
.kk-result-emoji { font-size: 64px; margin-bottom: 10px; }
.kk-result-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 30px;
    color: #f7c33f;
    margin-bottom: 8px;
}
.kk-result-score {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 72px;
    color: white;
    line-height: 1;
    margin-bottom: 6px;
}
.kk-result-sub {
    color: rgba(255,255,255,0.7);
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 0;
}

/* Result detail cards */
.kk-detail-header {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 15px;
    color: #f7c33f;
    letter-spacing: 0.5px;
    margin: 18px 0 10px;
    text-align: center;
}
.kk-detail-card {
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-family: 'Nunito Sans', sans-serif;
    font-size: 13px;
    line-height: 1.6;
}
.kk-detail-card.correct {
    background: rgba(38,137,12,0.25);
    border: 1.5px solid rgba(38,137,12,0.6);
}
.kk-detail-card.wrong {
    background: rgba(226,27,60,0.22);
    border: 1.5px solid rgba(226,27,60,0.5);
}
.kk-detail-card .dc-top {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 5px;
}
.kk-detail-card .dc-icon {
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 1px;
}
.kk-detail-card .dc-soal {
    color: white;
    font-weight: 600;
    font-size: 13px;
    flex: 1;
}
.kk-detail-card .dc-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 4px;
    flex-wrap: wrap;
}
.kk-detail-card .dc-label {
    font-size: 11px;
    font-weight: 700;
    color: rgba(255,255,255,0.55);
    white-space: nowrap;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
.kk-detail-card .dc-val {
    font-size: 13px;
    color: rgba(255,255,255,0.9);
    direction: rtl;
    text-align: right;
}
.kk-detail-card .dc-val.ar-text {
    font-family: 'Amiri', 'Traditional Arabic', serif;
    font-size: 17px;
    line-height: 1.8;
}
.kk-detail-card .dc-val.kunci {
    color: #f7c33f;
    font-weight: 700;
}
.kk-detail-card .dc-val.jawaban {
    color: rgba(255,255,255,0.8);
}
</style>
""", unsafe_allow_html=True)

# --- QUESTIONS ---
questions = [
    {
        "soal": 'Ungkapan yang berarti "Sampai jumpa" adalah...',
        "kunci": ["مع السلامة", "مع السلامه"],
        "wrong_keys": ["السلام عليكم", "صباح الخير"],
        "clues": ["a. السَّلَامُ عَلَيْكُمْ", "b. مَعَ السَّلَامَةِ", "c. صَبَاحُ الْخَيْرِ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": "Baca dialog berikut, lalu jawab pertanyaan!",
        "kunci": ["من جاكرتا", "انا من جاكرتا", "من جاكارتا"],
        "wrong_keys": ["من بندونغ", "من باندونغ", "من سورابايا"],
        "clues": ["a. مِنْ جَاكَرْتَا", "b. مِنْ بَانْدُونْغ", "c. مِنْ سُورَابَايَا"],
        "dialog": "أ: السَّلَامُ عَلَيْكُمْ. أَنَا أَحْمَدُ. مَا اسْمُكَ؟\nب: وَعَلَيْكُمُ السَّلَامُ. أَنَا عَلِيٌّ.\nأ: مِنْ أَيْنَ أَنْتَ يَا عَلِيُّ؟\nب: أَنَا مِنْ جَاكَرْتَا.",
        "question_label": "?مِنْ أَيْنَ عَلِيٌّ",
    },
    {
        "soal": 'Bahasa Arab dari "Nenek" adalah?',
        "kunci": ["الجده", "جده", "الجدة"],
        "wrong_keys": ["الجد", "حديقه"],
        "clues": ["a. الْجَدُّ", "b. حَدِيقَةٌ", "c. الْجَدَّةُ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": 'Apa bahasa arabnya "Saya membersihkan kelas"?',
        "kunci": ["انا انظف الفصل", "انا نظف الفصل", "أنا أنظف الفصل"],
        "wrong_keys": ["نحن ننظف الساحه", "انا ادرس في الفصل"],
        "clues": ["a. نَحْنُ نُنَظِّفُ السَّاحَةَ", "b. أَنَا أُنَظِّفُ الْفَصْلَ", "c. أَنَا أَدْرُسُ فِي الْفَصْلِ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": "الْبَابَ ....!\n(Bukalah pintu itu!) Bentuk perintah yang tepat untuk melengkapi kalimat tersebut adalah?",
        "kunci": ["افتح", "اِفْتَحْ", "iftah"],
        "wrong_keys": ["اقرا", "اقرأ", "انظر"],
        "clues": ["a. اِقْرَأْ", "b. اُنْظُرْ", "c. اِفْتَحْ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": 'Apa bahasa arabnya "Berapa harga buku ini?"',
        "kunci": ["كم ثمن هذا الكتاب"],
        "wrong_keys": ["هذا كتاب جديد", "ثمنه عشرون الف روبيه"],
        "clues": ["a. هَذَا كِتَابٌ جَدِيدٌ", "b. ثَمَنُهُ عِشْرُونَ أَلْفَ رُوبِيَّةٍ", "c. كَمْ ثَمَنُ هَذَا الْكِتَابِ؟"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": "Tolong lafadzkan dengan tepat kata ini:\nلَعِبُ كُرَةِ الْقَدَمِ",
        "kunci": ["لعب كره القدم", "لعب كرة القدم"],
        "wrong_keys": [],
        "clues": None,
        "dialog": None, "question_label": None,
    },
    {
        "soal": 'Apa Bahasa Arab dari "Sekolah"?',
        "kunci": ["مدرسه", "مدرسة", "المدرسه", "المدرسة"],
        "wrong_keys": ["مقبره", "غابه", "مقبرة", "غابة"],
        "clues": ["a. مَقْبَرَةٌ", "b. غَابَةٌ", "c. مَدْرَسَةٌ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": 'Apa bahasa arabnya "Hobi saya adalah berenang."?',
        "kunci": ["هوايتي السباحه", "هوايتي السباحة"],
        "wrong_keys": ["انا احب القراءه", "انا العب كره القدم"],
        "clues": ["a. أَنَا أُحِبُّ الْقِرَاءَةَ", "b. هِوَايَتِي السِّبَاحَةُ", "c. أَنَا أَلْعَبُ كُرَةَ الْقَدَمِ"],
        "dialog": None, "question_label": None,
    },
    {
        "soal": 'Kata yang berarti "kamar mandi" dalam bahasa Arab adalah?',
        "kunci": ["حمام"],
        "wrong_keys": ["مطبخ", "غرفه النوم"],
        "clues": ["a. مَطْبَخٌ", "b. حَمَّامٌ", "c. غُرْفَةُ النَّوْمِ"],
        "dialog": None, "question_label": None,
    },
]

# --- SESSION ---
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
    st.session_state.scores = {}
    st.session_state.answered = False
    st.session_state.streak = 0
    st.session_state.max_streak = 0
    st.session_state.last_recog = ""
    st.session_state.answer_log = {}   # {q_idx: {"jawaban": str, "benar": bool}}

# --- TRANSLITERATION MAP (Latin → Arabic) ---
# Covers common Indonesian-style Arabic transliteration
TRANSLIT_MAP = [
    # Multi-char first (order matters)
    ("dzh", "ذ"), ("dz", "ذ"),
    ("sy", "ش"), ("sh", "ص"),
    ("kh", "خ"), ("gh", "غ"),
    ("th", "ط"), ("ts", "ث"),
    ("zh", "ظ"),
    ("ai", "ي"), ("ay", "ي"),
    ("au", "و"), ("aw", "و"),
    # Single chars
    ("a", "ا"), ("b", "ب"), ("t", "ت"),
    ("j", "ج"), ("h", "ح"),  # default h = ح
    ("d", "د"), ("r", "ر"), ("z", "ز"),
    ("s", "س"), ("f", "ف"), ("q", "ق"),
    ("k", "ك"), ("l", "ل"), ("m", "م"),
    ("n", "ن"), ("w", "و"), ("y", "ي"),
    ("e", "ع"), ("i", "ي"), ("u", "و"),
    ("'", "ء"), ("g", "ج"),
]

def is_arabic(text):
    """Check if text contains Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def translit_to_arabic(text):
    """
    Convert Latin transliteration to approximate Arabic script.
    Only used when text contains no Arabic characters.
    Words are converted individually then joined.
    """
    text = text.lower().strip()
    # Common full-word mappings first (Indonesian Arabic loanwords / phrases)
    word_map = {
        "ana": "انا",
        "anta": "انت",
        "anti": "انت",
        "huwa": "هو",
        "hiya": "هي",
        "hia": "هي",
        "nahnu": "نحن",
        "antum": "انتم",
        "hum": "هم",
        "ma": "ما",
        "min": "من",
        "fi": "في",
        "ila": "الى",
        "ala": "على",
        "wa": "و",
        "la": "لا",
        "hal": "هل",
        "kam": "كم",
        "man": "من",
        "aina": "اين",
        "mata": "متى",
        "kaifa": "كيف",
        "lima": "لماذا",
        "madza": "ماذا",
        "madha": "ماذا",
        # verbs
        "unazhzif": "انظف",
        "unadzif": "انظف",
        "andziful": "انظف",
        "andzif": "انظف",
        "nadzif": "نظف",
        "unadzzifu": "انظف",
        "unazzif": "انظف",
        "iqra": "اقرا",
        "ikra": "اقرا",
        "iftah": "افتح",
        "ifta": "افتح",
        "albab": "الباب",
        # nouns
        "alfashl": "الفصل",
        "alfashal": "الفصل",
        "alfahsl": "الفصل",
        "fashl": "فصل",
        "fashal": "فصل",
        "alkitab": "الكتاب",
        "kitab": "كتاب",
        "alhamam": "الحمام",
        "hamam": "حمام",
        "hammam": "حمام",
        "alhammam": "الحمام",
        "mathbakh": "مطبخ",
        "almathbakh": "المطبخ",
        "madrasah": "مدرسة",
        "madrasa": "مدرسة",
        "almadrasa": "المدرسة",
        "almadrasah": "المدرسة",
        "maqbarah": "مقبرة",
        "maqbara": "مقبرة",
        "ghabah": "غابة",
        "ghaba": "غابة",
        "hiwayah": "هواية",
        "hiwayati": "هوايتي",
        "hiwayatii": "هوايتي",
        "huwayati": "هوايتي",
        "alsibahah": "السباحة",
        "sibahah": "سباحة",
        "assibahah": "السباحة",
        "ali": "علي",
        "ahmad": "احمد",
        "bandung": "بندونغ",
        "jakarta": "جاكرتا",
        "surabaya": "سورابايا",
        "jaddah": "جدة",
        "jaddati": "جدتي",
        "laib": "لعب",
        "laab": "لعب",
        "lacib": "لعب",
        "laibu": "لعب",
        "kuratul": "كرة",
        "kuratuil": "كرة",
        "kuratil": "كرة",
        "qadami": "القدم",
        "qadami": "القدم",
        "qadami": "القدم",
        "alqadami": "القدم",
        "alqadam": "القدم",
        "qadam": "قدم",
        "kura": "كرة",
        "kuroti": "كرة",
        "maa": "ما",
        "hiya": "هي",
        "hiwa": "هي",
        "tsaman": "ثمن",
        "thaman": "ثمن",
        "hadzal": "هذا",
        "hadza": "هذا",
        "maal": "مع",
        "maa": "مع",
        "assalamu": "السلام",
        "salamu": "السلام",
        "alaikum": "عليكم",
        "wassalam": "السلام",
        "massalama": "مع السلامة",
        "massalame": "مع السلامة",
        "maassalamah": "مع السلامة",
    }

    words = text.split()
    result_words = []
    i = 0
    while i < len(words):
        w = words[i]
        # Try two-word combinations first
        if i + 1 < len(words):
            two = words[i] + " " + words[i+1]
            if two in word_map:
                result_words.append(word_map[two])
                i += 2
                continue
        if w in word_map:
            result_words.append(word_map[w])
        else:
            # Fallback: character-by-character transliteration
            ar = []
            j = 0
            while j < len(w):
                matched = False
                for latin, arabic in TRANSLIT_MAP:
                    if w[j:j+len(latin)] == latin:
                        ar.append(arabic)
                        j += len(latin)
                        matched = True
                        break
                if not matched:
                    j += 1
            result_words.append("".join(ar) if ar else w)
        i += 1

    return " ".join(result_words)

# --- HELPERS ---
def normalize_ar(text):
    """Normalize Arabic: strip harakat, unify alef/ta marbuta/ya/waw variants."""
    if not text:
        return ""
    text = re.sub(r'[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', text)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    text = text.replace('ة', 'ه')
    text = text.replace('ؤ', 'و')
    text = text.replace('ئ', 'ي').replace('ى', 'ي')
    text = text.replace('ـ', '')
    text = re.sub(r'[^\u0621-\u064Aa-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def word_overlap(hasil_words, kunci_words):
    if not kunci_words:
        return 0.0
    return sum(1 for w in kunci_words if w in hasil_words) / len(kunci_words)

def normalize_latin(text):
    """Normalize Latin transliteration: lowercase, strip punctuation/apostrophes."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"['\u2018\u2019\u02bc\u0027]", "", text)  # remove apostrophes
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def check_answer(hasil_raw, kunci_list, wrong_keys=None):
    """
    Check answer. Tries:
    1. Direct Arabic comparison (normalized)
    2. Transliteration → Arabic comparison
    3. Direct Latin-to-Latin comparison (for Latin kunci variants)
    Returns score 0.0–1.0.
    """
    candidates_ar = [hasil_raw]

    # If no Arabic chars, also try converting transliteration → Arabic
    if not is_arabic(hasil_raw):
        converted = translit_to_arabic(hasil_raw)
        if converted != hasil_raw:
            candidates_ar.append(converted)

    best_final = 0.0

    # --- Arabic comparison path ---
    for candidate in candidates_ar:
        hasil = normalize_ar(candidate)
        hasil_words = set(hasil.split())

        best_correct = 0.0
        for k in kunci_list:
            k_norm = normalize_ar(k)
            k_words = set(k_norm.split())
            seq_sim = similarity(hasil, k_norm)
            overlap = word_overlap(hasil_words, k_words)
            combined = (seq_sim * 0.6) + (overlap * 0.4)
            best_correct = max(best_correct, combined)

        if wrong_keys:
            best_wrong = 0.0
            for wk in wrong_keys:
                wk_norm = normalize_ar(wk)
                wk_words = set(wk_norm.split())
                seq_sim = similarity(hasil, wk_norm)
                overlap = word_overlap(hasil_words, wk_words)
                combined = (seq_sim * 0.6) + (overlap * 0.4)
                best_wrong = max(best_wrong, combined)

            if best_wrong >= best_correct * 0.8:
                best_correct *= 0.4

        best_final = max(best_final, best_correct)

    # --- Latin-to-Latin comparison path (for kunci that are Latin strings) ---
    if not is_arabic(hasil_raw):
        hasil_lat = normalize_latin(hasil_raw)
        hasil_lat_words = set(hasil_lat.split())
        for k in kunci_list:
            if not is_arabic(k):
                k_lat = normalize_latin(k)
                k_lat_words = set(k_lat.split())
                seq_sim = similarity(hasil_lat, k_lat)
                overlap = word_overlap(hasil_lat_words, k_lat_words)
                combined = (seq_sim * 0.6) + (overlap * 0.4)
                best_final = max(best_final, combined)

    return best_final

def wrap_arabic(text):
    """
    Wrap Arabic script segments in <span class='ar'> for Traditional Arabic font.
    Leaves Latin/Indonesian text as-is.
    """
    def replacer(m):
        return f'<span class="ar">{m.group(0)}</span>'
    # Match runs of Arabic characters + harakat + spaces between Arabic words
    result = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][^\u0000-\u007F\n<>]*', replacer, text)
    return result

# Thresholds per soal
THRESHOLDS = [0.65, 0.55, 0.70, 0.55, 0.70, 0.55, 0.60, 0.55, 0.60, 0.70]

total_score = sum(st.session_state.scores.values())
q_idx = st.session_state.q_idx

# --- TOP BAR ---
st.markdown(f"""
<div class="kk-topbar">
    <div class="kk-logo">Takallam<span>!</span></div>
    <div class="kk-badge">🔥 {st.session_state.streak} Berturut</div>
    <div class="kk-score-badge">⭐ {total_score} pts</div>
</div>
""", unsafe_allow_html=True)

# --- RESULT SCREEN ---
if q_idx >= len(questions):
    st.balloons()
    emoji = "🏆" if total_score >= 80 else "🎉" if total_score >= 50 else "📚"
    jumlah_benar = sum(1 for v in st.session_state.scores.values() if v == 10)
    jumlah_salah = len(questions) - jumlah_benar

    st.markdown(f"""
    <div class="kk-result-screen">
        <div class="kk-result-emoji">{emoji}</div>
        <div class="kk-result-title">Tes Selesai!</div>
        <div class="kk-result-score">{total_score}</div>
        <div class="kk-result-sub">
            dari 100 poin &nbsp;|&nbsp; Streak terbaik: {st.session_state.max_streak}<br>
            ✅ {jumlah_benar} Benar &nbsp;&nbsp; ❌ {jumlah_salah} Salah
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- DETAIL RINCIAN PER SOAL ---
    st.markdown('<div class="kk-detail-header">📊 RINCIAN JAWABAN</div>', unsafe_allow_html=True)

    for i, q in enumerate(questions):
        benar = st.session_state.scores.get(i, 0) == 10
        log = st.session_state.answer_log.get(i, {})
        jawaban_siswa = log.get("jawaban", "—")
        kunci_display = q["kunci"][0]

        # Truncate soal text for display
        soal_short = q["soal"].replace("\n", " ")
        if len(soal_short) > 60:
            soal_short = soal_short[:57] + "..."

        status_class = "correct" if benar else "wrong"
        icon = "✅" if benar else "❌"

        jawaban_html = wrap_arabic(jawaban_siswa)
        kunci_html = wrap_arabic(kunci_display)
        soal_short_html = wrap_arabic(soal_short)

        st.markdown(f"""
        <div class="kk-detail-card {status_class}">
            <div class="dc-top">
                <div class="dc-icon">{icon}</div>
                <div class="dc-soal"><b>Soal {i+1}:</b> {soal_short_html}</div>
            </div>
            <div class="dc-row">
                <span class="dc-label">Kunci jawaban:</span>
                <span class="dc-val kunci ar-text">{kunci_html}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 Main Lagi!"):
        for key in ["q_idx","scores","answered","streak","max_streak","last_recog","answer_log"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.stop()

# --- PROGRESS ---
progress_pct = int((q_idx + 1) / len(questions) * 100)
st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
    <div class="kk-progress-wrap" style="flex:1;margin:0;">
        <div class="kk-progress-fill" style="width:{progress_pct}%"></div>
    </div>
    <div style="color:rgba(255,255,255,0.7);font-family:'Nunito',sans-serif;font-weight:800;font-size:13px;white-space:nowrap;">
        {q_idx+1} / {len(questions)}
    </div>
</div>
""", unsafe_allow_html=True)

q = questions[q_idx]

# --- QUESTION CARD ---
dialog_html = ""
if q.get("dialog"):
    lines = wrap_arabic(q["dialog"]).replace("\n", "<br>")
    dialog_html = f'<div class="kk-dialog-box">{lines}</div>'

qlabel_html = ""
if q.get("question_label"):
    qlabel_html = f'<div class="kk-question-label">❓ <span class="ar" style="font-size:19px;">{q["question_label"]}</span></div>'

soal_text = wrap_arabic(q["soal"]).replace("\n", "<br>")

st.markdown(f"""
<div class="kk-question-card">
    <p class="kk-question-text">{soal_text}</p>
    {dialog_html}
    {qlabel_html}
</div>
""", unsafe_allow_html=True)

# --- CLUE BOX ---
if q.get("clues"):
    clue_items = ""
    for c in q["clues"]:
        label = c[0]
        rest = wrap_arabic(c[2:].strip())
        clue_items += f'<div class="kk-clue-option"><span class="label" style="font-family:\'Nunito\',sans-serif;font-size:13px;">{label}.</span>{rest}</div>'
    st.markdown(f"""
    <div class="kk-clue-box">
        <div class="kk-clue-title">📋 PILIHAN JAWABAN</div>
        {clue_items}
    </div>
    """, unsafe_allow_html=True)

# --- MIC SECTION ---
st.markdown("""
<div class="kk-mic-section">
    <div class="kk-mic-label">🎤 Tekan tombol lalu ucapkan jawaban kamu dalam Bahasa Arab dengan <b style="color:#f7c33f;font-size:14px;letter-spacing:1px;">JELAS</b></div>
    <div class="kk-mic-warn">⚠️ Ucapkan jawaban langsung, bukan A, B, C nya!</div>
</div>
""", unsafe_allow_html=True)

audio = audio_recorder(
    text="  Rekam Jawaban",
    recording_color="#e21b3c",
    neutral_color="#f7c33f",
    icon_name="microphone",
    icon_size="2x",
    key=f"audio_{q_idx}"
)

# --- PROCESS AUDIO ---
if audio is not None and len(audio) > 800 and not st.session_state.answered:
    with open("temp_tak.wav", "wb") as f:
        f.write(audio)

    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0
    r.non_speaking_duration = 0.6

    recog_text = None
    with sr.AudioFile("temp_tak.wav") as source:
        r.adjust_for_ambient_noise(source, duration=0.4)
        data = r.record(source)

    # Try Arabic first, then Indonesian (for transliteration input)
    for lang in ["ar-SA", "ar-EG", "ar", "id-ID"]:
        try:
            recog_text = r.recognize_google(data, language=lang)
            if recog_text:
                break
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            break

    if recog_text:
        st.session_state.last_recog = recog_text
        threshold = THRESHOLDS[q_idx] if q_idx < len(THRESHOLDS) else 0.65
        score = check_answer(recog_text, q["kunci"], q.get("wrong_keys", []))

        is_correct = score >= threshold

        if is_correct:
            st.session_state.scores[q_idx] = 10
            st.session_state.streak += 1
            st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
        else:
            st.session_state.scores[q_idx] = 0
            st.session_state.streak = 0

        # Log jawaban untuk halaman hasil
        st.session_state.answer_log[q_idx] = {
            "jawaban": recog_text,
            "benar": is_correct,
        }

        st.session_state.answered = True
        st.rerun()

# --- SHOW FEEDBACK AFTER ANSWERING ---
if st.session_state.answered:
    got_right = st.session_state.scores.get(q_idx, 0) == 10
    kunci_display = wrap_arabic(q["kunci"][0])
    recog_display = wrap_arabic(st.session_state.last_recog) if st.session_state.last_recog else "—"

    if got_right:
        st.markdown(f"""
        <div class="kk-feedback-correct">
            🎉 Mantap! Jawaban benar!<br>
            <span style="font-size:13px;opacity:0.85;font-family:'Nunito',sans-serif;">Kunci: {kunci_display}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="kk-feedback-wrong">
            ❌ Belum tepat!<br>
            <span style="font-size:13px;opacity:0.85;font-family:'Nunito',sans-serif;">Kunci: {kunci_display}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("Soal Berikutnya ➡️"):
        old = st.session_state.q_idx
        st.session_state.q_idx += 1
        st.session_state.answered = False
        st.session_state.last_recog = ""
        if f"audio_{old}" in st.session_state:
            del st.session_state[f"audio_{old}"]
        st.rerun()
