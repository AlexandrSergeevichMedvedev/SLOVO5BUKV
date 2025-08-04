import streamlit as st
import pandas as pd
import zipfile
import os

# --- Стилизация интерфейса ---
st.markdown("""
    <style>
    .title-grid {
        display: flex;
        align-items: center;
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
    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        margin-top: 40px;
    }
    .input-wrapper {
        width: 50px;
        height: 50px;
        border: 1px solid #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .input-wrapper input {
        width: 100%;
        height: 100%;
        text-align: center;
        font-size: 24px;
        border: none;
        outline: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Название и кнопка сброса ---
st.markdown('<div class="title-grid">' +
            ''.join([f'<div class="title-letter">{l}</div>' for l in "5БУКВ"]) +
            '<form action="" method="get"><button class="reset-button" type="submit">СБРОС</button></form>' +
            '</div>', unsafe_allow_html=True)

# --- 5 квадратных ячеек для фиксированных букв ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed'))
st.markdown('</div>', unsafe_allow_html=True)

# --- 5 ячеек "Буквы есть, но не в позиции" ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
not_in_positions = []
for i in range(5):
    not_in_positions.append(st.text_input("", key=f"notin_{i}", label_visibility='collapsed'))
st.markdown('</div>', unsafe_allow_html=True)

# --- Поле для исключённых букв ---
excluded_letters = st.text_input("Исключённые буквы (через запятую):", key="excluded")

# --- Словарь из ZIP ---
@st.cache_data
def load_dictionary():
    with zipfile.ZipFile('/mount/src/slovo5bukv/russian.dic.zip', 'r') as zip_ref:
        zip_ref.extractall('/tmp/dictionary')
    with open('/tmp/dictionary/russian.dic', 'r', encoding='utf-8') as f:
        words = [line.strip().upper() for line in f if len(line.strip()) == 5]
    return words

dictionary = load_dictionary()

# --- Логика фильтрации ---
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
    for idx, letter in enumerate(fixed_positions):
        if letter and word[idx] != letter.upper():
            match = False
            break
    for idx, field in enumerate(not_in_positions):
        if field:
            letters = [l.strip().upper() for l in field.split(',')]
            if any(word[idx] == l for l in letters):
                match = False
                break
    if not mandatory_letters.issubset(set(word)):
        match = False
    if match:
        results.append(word)

# --- Вывод списка слов ---
st.markdown(f"### Найдено слов: {len(results)}")
for word in results:
    st.write(word)
