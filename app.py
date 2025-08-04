
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

# Интерфейс
st.title("Поиск слов по условиям (5 букв)")

cols = st.columns(5)
fixed_positions = [''] * 5
for i in range(5):
    fixed_positions[i] = cols[i].text_input(f"Позиция {i+1}", max_chars=1).lower()

excluded_input = st.text_input("Исключённые буквы (через запятую)", "")
excluded_letters = set(x.strip() for x in excluded_input.lower().split(",") if x.strip())

included_input = st.text_input("Буквы, которые есть в слове (позиции неизвестны)", "")
included_letters = set(x.strip() for x in included_input.lower().split(",") if x.strip())

# Фильтрация слов
results = []
for word in dictionary:
    if excluded_letters & set(word):
        continue
    if not included_letters.issubset(set(word)):
        continue
    if any(fp and word[i] != fp for i, fp in enumerate(fixed_positions)):
        continue
    results.append(word)

# Результаты
st.write(f"Найдено {len(results)} слов:")
st.dataframe(results)
