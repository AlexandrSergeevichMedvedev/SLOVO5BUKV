import streamlit as st
import requests
import zipfile
import os

# --- Скачивание файла с Google Drive ---
def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)

# --- Получение подтверждающего токена для скачивания ---
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

# --- Сохранение скачанного файла ---
def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# --- Загрузка словаря (скачиваем с Google Drive) ---
@st.cache_data
def load_dictionary():
    if not os.path.exists('russian.dic.zip'):
        st.write("Скачиваем словарь с Google Диска...")
        download_file_from_google_drive('1TlkCaAhP-SBEKzmWMkBbW9bx4yyAaM7D', 'russian.dic.zip')
    with zipfile.ZipFile('russian.dic.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    with open('russian.dic', 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return set(words)

# --- CSS стили для интерфейса ---
st.markdown("""
    <style>
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .title-box {
        display: flex;
        gap: 5px;
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
        border: 1px solid black;
    }
    .reset-button {
        background-color: yellow;
        padding: 5px 10px;
        font-weight: bold;
        border: 1px solid black;
    }
    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: nowrap;
    }
    .input-square input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
    }
    .below-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Заголовок и кнопка сброса ---
col1, col2 = st.columns([5,1])
with col1:
    st.markdown("""
    <div class="title-box">
        <div class="title-letter">5</div>
        <div class="title-letter">Б</div>
        <div class="title-letter">У</div>
        <div class="title-letter">К</div>
        <div class="title-letter">В</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("СБРОС", key="reset", help="Сбросить все поля"):
        st.experimental_rerun()

# --- Поля для фиксированных позиций ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, class_name="input-square"))
st.markdown('</div>', unsafe_allow_html=True)

# --- Поля "буквы есть в слове, но не в этой позиции" ---
st.write("Буквы есть в слове, но не в этой позиции:")
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
not_in_positions = []
for i in range(5):
    not_in_positions.append(st.text_input("", key=f"not_in_pos_{i}", placeholder="Б", max_chars=10))
st.markdown('</div>', unsafe_allow_html=True)

# --- Поле для исключённых букв ---
excluded_letters = st.text_input("Исключённые буквы", key="excluded_letters", placeholder="Введите буквы")

# --- Загрузка словаря ---
dictionary = load_dictionary()

# --- Фильтрация слов по условиям ---
results = []
for word in dictionary:
    word_ok = True
    # Проверяем фиксированные позиции
    for idx, letter in enumerate(fixed_positions):
        if letter and word[idx] != letter.lower():
            word_ok = False
            break
    if not word_ok:
        continue
    # Проверяем исключённые буквы
    if any(l in excluded_letters.lower() for l in word):
        continue
    # Проверяем обязательные буквы не в своих позициях
    for idx, field in enumerate(not_in_positions):
        if field:
            letters = [l.lower() for l in field.replace(" ", "").split(",") if l]
            for l in letters:
                if l not in word:
                    word_ok = False
                    break
                if word[idx] == l:
                    word_ok = False
                    break
        if not word_ok:
            break
    if word_ok:
        results.append(word)

# --- Вывод результатов ---
st.write(f"Найдено слов: {len(results)}")
for w in results:
    st.write(w)
