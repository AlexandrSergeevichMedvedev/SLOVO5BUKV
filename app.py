import streamlit as st
import pandas as pd
import zipfile
import os

# --- Стилизация интерфейса ---
st.markdown("""
    <style>
    /* Название 5БУКВ в квадратных ячейках */
    .title-grid {
        display: flex;
        gap: 5px;
        margin-bottom: 20px;
    }
    .title-letter {
        width: 30px;
        height: 30px;
        background-color: yellow;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 20px;
    }
    /* Кнопка сброса */
    .reset-button {
        margin-left: 20px;
        height: 30px;
        background-color: yellow;
        color: black;
        font-weight: bold;
        border: none;
        padding: 0 10px;
        cursor: pointer;
    }
    /* Сетка квадратных ячеек */
    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        margin-top: 40px;
    }
    .input-square input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
    }
    .section-title {
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Название 5БУКВ и кнопка сброса ---
st.markdown('<div class="title-grid">' +
            ''.join([f'<div class="title-letter">{l}</div>' for l in "5БУКВ"]) +
            '<form action="" method="get"><button class="reset-button" type="submit">СБРОС</button></form>' +
            '</div>', unsafe_allow_html=True)

# --- 5 квадратных ячеек для фиксированных букв ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, class_name="input-square"))
st.markdown('</div>', unsafe_allow_html=True)

# --- 5 ячеек для букв, которые точно есть, но не в этой позиции ---
st.markdown('<div class="section-title">Буквы есть, но не в позиции:</div>', unsafe_allow_html=True)
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
not_in_positions = []
for i in range(5):
    not_in_positions.append(st.text_input("", key=f"notin_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, class_name="input-square"))
st.markdown('</div>', unsafe_allow_html=True)

# --- Поле для исключённых букв ---
excluded_letters = st.text_input("Исключённые буквы (через запятую):", key="excluded")

# --- Загружаем словарь с Google Диска (ZIP) ---
@st.cache_data
def load_dictionary():
    with zipfile.ZipFile('/mount/src/slovo5bukv/russian.dic.zip', 'r') as zip_ref:
        zip_ref.extractall('/tmp/dictionary')
    with open('/tmp/dictionary/russian.dic', 'r', encoding='utf-8') as f:
        words = [line.strip().upper() for line in f if len(line.strip()) == 5]
    return words

dictionary = load_dictionary()

# --- Логика фильтрации слов ---
excluded_set = set(excluded_letters.replace(' ', '').upper().split(','))
mandatory_letters = set()

for field in not_in_positions:
    if field:
        mandatory_letters.update([l.strip().upper() for l in field.split(',') if l.strip()])

# Фильтрация
results = []
for word in dictionary:
    if any(l in excluded_set for l in word):
        continue
    match = True
    # Проверка фиксированных позиций
    for idx, letter in enumerate(fixed_positions):
        if letter and word[idx] != letter.upper():
            match = False
            break
    # Проверка букв, которые есть, но не в этой позиции
    for idx, field in enumerate(not_in_positions):
        if field:
            letters = [l.strip().upper() for l in field.split(',')]
            if any(word[idx] == l for l in letters):
                match = False
                break
    # Проверка наличия обязательных букв
    if not mandatory_letters.issubset(set(word)):
        match = False
    if match:
        results.append(word)

# --- Вывод списка слов ---
st.markdown(f"### Найдено слов: {len(results)}")
for word in results:
    st.write(word)
