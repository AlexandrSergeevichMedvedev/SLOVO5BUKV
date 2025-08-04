import streamlit as st
import os
import requests

# Скачивание словаря (если его нет)
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
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .header-box {
        display: inline-block;
        background-color: yellow;
        width: 30px;
        height: 30px;
        font-size: 20px;
        text-align: center;
        line-height: 30px;
        margin-right: 5px;
        border-radius: 5px;
        font-weight: bold;
    }
    .reset-btn {
        display: inline-block;
        background-color: yellow;
        width: 60px;
        height: 30px;
        font-size: 14px;
        text-align: center;
        line-height: 30px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        border: none;
    }
    .input-grid {
        display: flex;
        justify-content: center;
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
    .block-label {
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Шапка с 5БУКВ и кнопкой сброса ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <div class="header-container">
            <div>
                <div class="header-box">5</div>
                <div class="header-box">Б</div>
                <div class="header-box">У</div>
                <div class="header-box">К</div>
                <div class="header-box">В</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("СБРОС"):
        st.experimental_rerun()

# --- Поля фиксированных позиций ---
st.markdown('<div class="block-label">Буквы на своих местах</div>', unsafe_allow_html=True)
st.markdown("<div class='input-grid'>", unsafe_allow_html=True)
fixed_positions = []
cols = st.columns(5)
for i, col in enumerate(cols):
    with col:
        fixed_positions.append(st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, args=None, kwargs=None, class_name="input-square"))
st.markdown("</div>", unsafe_allow_html=True)

# --- Поля для букв, которые есть в слове, но не в этой позиции ---
st.markdown('<div class="block-label">Буквы есть в слове, но не в этой позиции</div>', unsafe_allow_html=True)
st.markdown("<div class='input-grid'>", unsafe_allow_html=True)
not_in_positions = []
cols = st.columns(5)
for i, col in enumerate(cols):
    with col:
        not_in_positions.append(st.text_input("", key=f"not_pos_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, args=None, kwargs=None, class_name="input-square"))
st.markdown("</div>", unsafe_allow_html=True)

# --- Ввод исключённых букв ---
excluded_input = st.text_input("Исключённые буквы (через запятую)", key="excluded")
excluded_letters = set(x.strip().lower() for x in excluded_input.split(",") if x.strip())

# --- Логика фильтрации ---
must_have_letters = set()
results = []

# Собираем все буквы из "буквы есть в слове, но не в этой позиции"
for i, field in enumerate(not_in_positions):
    if field.strip():
        letters = set(x.strip() for x in field.lower().split(",") if x.strip())
        must_have_letters.update(letters)

for word in dictionary:
    # Исключаем слова с запрещёнными буквами
    if excluded_letters & set(word):
        continue
    # Проверка фиксированных позиций
    if any(fp and word[i] != fp.lower() for i, fp in enumerate(fixed_positions)):
        continue
    # Проверка букв, которые не должны стоять в своей позиции
    skip_word = False
    for i, field in enumerate(not_in_positions):
        if field.strip():
            letters = set(x.strip() for x in field.lower().split(",") if x.strip())
            if word[i] in letters:
                skip_word = True
                break
    if skip_word:
        continue
    # Проверка, чтобы буквы были в слове в других позициях
    if not must_have_letters.issubset(set(word)):
        continue
    results.append(word)

# --- Вывод результатов ---
st.write(f"Найдено {len(results)} слов:")
st.dataframe(results)
