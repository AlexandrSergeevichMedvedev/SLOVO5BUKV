import streamlit as st
import requests
import zipfile
import os

# Скачиваем файл с Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Загружаем словарь из архива
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

# CSS стили
st.markdown("""
    <style>
    .title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
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
        cursor: pointer;
    }
    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: nowrap;
    }
    .stTextInput > div > input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
    }
    .section-title {
        margin-top: 20px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Верхняя строка (5БУКВ и кнопка СБРОС)
st.markdown("""
    <div class="title-row">
        <div class="title-box">
            <div class="title-letter">5</div>
            <div class="title-letter">Б</div>
            <div class="title-letter">У</div>
            <div class="title-letter">К</div>
            <div class="title-letter">В</div>
        </div>
        <form action="" method="get">
            <button class="reset-button" type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Поля для фиксированных позиций (5 квадратов)
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed'))
st.markdown('</div>', unsafe_allow_html=True)

# Поля "буквы есть в слове, но не в этой позиции" (5 ячеек)
st.markdown('<div class="section-title">Буквы есть в слове, но не в этой позиции:</div>', unsafe_allow_html=True)
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
not_in_positions = []
for i in range(5):
    not_in_positions.append(st.text_input("", key=f"not_in_pos_{i}", placeholder="Б,Р"))
st.markdown('</div>', unsafe_allow_html=True)

# Поле для исключённых букв
excluded_letters = st.text_input("Исключённые буквы", key="excluded_letters", placeholder="Введите буквы")

# Загружаем словарь
dictionary = load_dictionary()

# Фильтрация слов по условиям
results = []
for word in dictionary:
    word_ok = True
    # Фиксированные позиции
    for idx, letter in enumerate(fixed_positions):
        if letter and word[idx] != letter.lower():
            word_ok = False
            break
    if not word_ok:
        continue
    # Исключённые буквы
    if any(l in excluded_letters.lower() for l in word):
        continue
    # Буквы есть в слове, но не в этой позиции
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

# Вывод найденных слов
st.write(f"Найдено слов: {len(results)}")
for w in results:
    st.write(w)
