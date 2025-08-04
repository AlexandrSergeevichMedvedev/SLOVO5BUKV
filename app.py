import streamlit as st
import zipfile
import os

# --- СТИЛИ CSS ---
st.markdown("""
    <style>
    .input-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 20px;
    }

    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .input-square input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
        background-color: white !important;
        border: 2px solid #000000;
        border-radius: 5px;
    }

    .not-in-position-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .excluded-letters {
        margin-bottom: 20px;
    }

    .reset-button {
        position: absolute;
        top: 20px;
        right: 20px;
        background-color: yellow;
        color: black;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
    }

    .title {
        display: flex;
        align-items: center;
        gap: 5px;
        margin-bottom: 30px;
    }

    .title-letter {
        width: 30px;
        height: 30px;
        background-color: yellow;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 18px;
        border-radius: 3px;
    }

    </style>
""", unsafe_allow_html=True)

# --- ЗАГОЛОВОК "5БУКВ" ---
st.markdown("""
    <div class="title">
        <div class="title-letter">5</div>
        <div class="title-letter">Б</div>
        <div class="title-letter">У</div>
        <div class="title-letter">К</div>
        <div class="title-letter">В</div>
    </div>
""", unsafe_allow_html=True)

# --- КНОПКА СБРОСА ---
query_params = st.query_params

if st.button("СБРОС", key="reset_button"):
    st.query_params.clear()
    st.rerun()


# --- ОБЕРТКА ДЛЯ ВСЕХ ПОЛЕЙ ВВОДА ---
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# --- ФИКСИРОВАННЫЕ ПОЗИЦИИ (5 КВАДРАТОВ) ---
fixed_positions = []
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
for i in range(5):
    fixed_positions.append(
        st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed', class_name="input-square")
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- "Буквы есть в слове, но не в этой позиции" (5 ЯЧЕЕК В СТРОКУ) ---
not_in_positions = []
st.markdown('<div class="not-in-position-grid">', unsafe_allow_html=True)
for i in range(5):
    not_in_positions.append(
        st.text_input("", key=f"not_in_pos_{i}", max_chars=20, label_visibility='collapsed', placeholder="Буквы")
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- Исключённые буквы ---
excluded_letters = st.text_input("Исключённые буквы", key="excluded_letters", placeholder="Например: А, Б, В")

st.markdown('</div>', unsafe_allow_html=True)  # Закрытие input-section

# --- ЗАГРУЗКА СЛОВАРЯ ИЗ АРХИВА ---
@st.cache_data
def load_dictionary():
    if not os.path.exists("russian.dic"):
        with zipfile.ZipFile("russian.dic.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
    with open("russian.dic", "r", encoding="windows-1251") as f:
        words = [line.strip().upper() for line in f if len(line.strip()) == 5]
    return words

# Подгружаем словарь
dictionary = load_dictionary()

# --- ЛОГИКА ФИЛЬТРАЦИИ СЛОВ ---
def filter_words():
    result = []
    excluded = set(excluded_letters.upper().replace(" ", "").split(","))
    mandatory_letters = set()

    # Собираем все обязательные буквы из not_in_positions
    for letters in not_in_positions:
        for letter in letters.upper().replace(" ", "").split(","):
            if letter:
                mandatory_letters.add(letter)

    for word in dictionary:
        if any(letter in excluded for letter in word):
            continue  # Пропускаем слова с исключёнными буквами

        # Проверяем фиксированные позиции
        mismatch = False
        for i in range(5):
            if fixed_positions[i] and word[i] != fixed_positions[i].upper():
                mismatch = True
                break
            if fixed_positions[i] == "" and any(word[i] == l.upper() for l in not_in_positions[i]):
                mismatch = True
                break
        if mismatch:
            continue

        # Проверяем наличие обязательных букв (в любом месте слова)
        if not mandatory_letters.issubset(set(word)):
            continue

        result.append(word)
    return result

# --- ВЫВОДИМ РЕЗУЛЬТАТ ---
filtered_words = filter_words()
st.write(f"Найдено слов: {len(filtered_words)}")
for word in filtered_words:
    st.write(word)
