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
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        flex-wrap: wrap;
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
        margin-left: 20px;
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
    }
    .input-square input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Шапка с 5БУКВ и СБРОС ---
st.markdown("""
    <div class="header-container">
        <div class="header-box">5</div>
        <div class="header-box">Б</div>
        <div class="header-box">У</div>
        <div class="header-box">К</div>
        <div class="header-box">В</div>
        <form action="" method="post">
            <button class="reset-btn" name="reset" type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# --- Логика сброса ---
if st.session_state.get("reset_triggered"):
    st.session_state["pos_0"] = ""
    st.session_state["pos_1"] = ""
    st.session_state["pos_2"] = ""
    st.session_state["pos_3"] = ""
    st.session_state["pos_4"] = ""
    st.session_state["excluded"] = ""
    st.session_state["included"] = ""
    st.session_state["reset_triggered"] = False

if "reset" in st.query_params:
    st.session_state["reset_triggered"] = True
    st.query_params.clear()  # очищаем URL

# --- Поля для фиксированных позиций ---
st.markdown("<div class='input-grid'>", unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False, args=None, kwargs=None, class_name="input-square"))
st.markdown("</div>", unsafe_allow_html=True)

# --- Ввод включённых и исключённых букв ---
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
