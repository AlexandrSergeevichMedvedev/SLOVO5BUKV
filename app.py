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
        margin-left: 20px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        border: none;
    }
    .letter-input input {
        width: 50px !important;
        height: 50px;
        text-align: center;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Шапка с 5БУКВ и СБРОС ---
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
        <div>
            <span class="header-box">5</span>
            <span class="header-box">Б</span>
            <span class="header-box">У</span>
            <span class="header-box">К</span>
            <span class="header-box">В</span>
        </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("СБРОС"):
        st.session_state["pos_0"] = ""
        st.session_state["pos_1"] = ""
        st.session_state["pos_2"] = ""
        st.session_state["pos_3"] = ""
        st.session_state["pos_4"] = ""
        st.session_state["excluded"] = ""
        st.session_state["included"] = ""

# --- Поля для фиксированных позиций ---
st.markdown("<div style='display: flex; gap: 5px; margin-top: 20px;'>", unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed'))
st.markdown("</div>", unsafe_allow_html=True)

# --- Поля для включённых и исключённых букв ---
excluded_input = st.text_input("Исключённые буквы (через запятую)", key="excluded")
included_input = st.text_input("Буквы, которые есть в слове (позиции неизвестны)", key="included")

excluded_letters = set(x.strip() for x in excluded_input.lower().split(",") if x.strip())
included_letters = set(x.strip() for x in included_input.lower().split(",") if x.strip())

# --- Фильтрация слов ---
results = []
for word in dictionary:
    if excluded_letters & set(word):
        continue
    if not included_letters.issubset(set(word)):
        continue
    if any(fp and word[i] != fp.lower() for i, fp in enumerate(fixed_positions)):
        continue
    results.append(word)

# --- Вывод результатов ---
st.write(f"Найдено {len(results)} слов:")
st.dataframe(results)
