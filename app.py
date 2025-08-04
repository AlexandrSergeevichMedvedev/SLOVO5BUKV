import streamlit as st
import os
import requests

# Скачивание словаря с Google Drive
def download_dictionary():
    url = 'https://drive.google.com/uc?export=download&id=1TlkCaAhP-SBEKzmWMkBbW9bx4yyAaM7D'
    if not os.path.exists('russian.dic'):
        with requests.get(url, stream=True) as r:
            with open('russian.dic', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

download_dictionary()

# Загрузка словаря
@st.cache_data
def load_dictionary():
    with open('russian.dic', 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f.readlines() if len(line.strip()) == 5]

dictionary = load_dictionary()

# --- Стилизация ---
st.markdown("""
    <style>
    .letter-box {
        width: 50px;
        height: 50px;
        font-size: 24px;
        text-align: center;
        border: 2px solid #999;
        border-radius: 5px;
        display: inline-block;
        margin: 5px;
    }
    .header-cube {
        background-color: yellow;
        display: inline-block;
        width: 30px;
        height: 30px;
        font-size: 20px;
        text-align: center;
        line-height: 30px;
        margin-right: 2px;
        border-radius: 4px;
        font-weight: bold;
    }
    .stButton > button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: yellow;
        padding: 8px 16px;
        border-radius: 5px;
        font-weight: bold;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- Заголовок ---
st.markdown("""
    <div>
        <span class="header-cube">5</span>
        <span class="header-cube">Б</span>
        <span class="header-cube">У</span>
        <span class="header-cube">К</span>
        <span class="header-cube">В</span>
    </div>
""", unsafe_allow_html=True)

# --- Кнопка сброса ---
if st.button("Сброс"):
    st.experimental_rerun()

# --- Поля для фиксированных позиций ---
fixed_positions = []
st.markdown("<div style='display: flex; gap: 5px;'>", unsafe_allow_html=True)
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed'))
st.markdown("</div>", unsafe_allow_html=True)

# --- Поля для включённых и исключённых букв ---
excluded_input = st.text_input("Исключённые буквы (через запятую)", "")
excluded_letters = set(x.strip() for x in excluded_input.lower().split(",") if x.strip())

included_input = st.text_input("Буквы, которые есть в слове (позиции неизвестны)", "")
included_letters = set(x.strip() for x in included_input.lower().split(",") if x.strip())

# --- Фильтрация слов ---
results = []
for word in dictionary:
    if excluded_letters & set(word):
        continue
    if not included_letters.issubset(set(word)):
        continue
    if any(fp and word[i] != fp for i, fp in enumerate(fixed_positions)):
        continue
    results.append(word)

# --- Результаты ---
st.write(f"Найдено {len(results)} слов:")
st.dataframe(results)
