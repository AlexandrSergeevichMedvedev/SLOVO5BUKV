import streamlit as st
import os
import requests

# --- Скачивание словаря ---
def download_dictionary():
    url = 'https://drive.google.com/uc?export=download&id=1TlkCaAhP-SBEKzmWMkBbW9bx4yyAaM7D'
    if not os.path.exists('russian.dic'):
        with requests.get(url, stream=True) as r:
            with open('russian.dic', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

download_dictionary()

# --- Загрузка словаря ---
@st.cache_data
def load_dictionary():
    with open('russian.dic', 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f.readlines() if len(line.strip()) == 5]

dictionary = load_dictionary()

# --- Сброс ---
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_fields():
    st.session_state.reset = True
    for i in range(5):
        st.session_state[f"pos_{i}"] = ""
        st.session_state[f"not_pos_{i}"] = ""
    st.session_state["excluded"] = ""

# --- Стили ---
st.markdown("""
<style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        flex-wrap: nowrap;
    }
    .header-box {
        display: inline-block;
        background-color: yellow;
        width: 24px;
        height: 24px;
        font-size: 16px;
        text-align: center;
        line-height: 24px;
        margin-right: 3px;
        border-radius: 3px;
        font-weight: bold;
    }
    .input-grid {
        display: flex;
        justify-content: center;
        gap: 3px;
        margin-bottom: 10px;
        flex-wrap: nowrap;
    }
    .input-square input {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        text-align: center;
        font-size: 18px;
        padding: 2px;
    }
    .input-column {
        flex: 1 1 18%;
        max-width: 18%;
    }
    .stButton>button {
        background-color: yellow;
        color: black;
        font-weight: bold;
        border-radius: 3px;
        width: 50px;
        height: 24px;
        font-size: 14px;
    }
    .stTextInput>div>div>input {
        padding: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- Заголовок ---
st.markdown("""
    <div class="header-container">
        <div style="display:flex;">
            <div class="header-box">5</div>
            <div class="header-box">Б</div>
            <div class="header-box">У</div>
            <div class="header-box">К</div>
            <div class="header-box">В</div>
        </div>
        <form action="" method="get">
            <button type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# --- Поля фиксированных позиций ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
fixed_positions = []
for i in range(5):
    fixed_positions.append(
        st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False)
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- Поля "буквы есть, но не в этой позиции" ---
st.markdown('<div class="input-grid">', unsafe_allow_html=True)
not_in_positions = []
for i in range(5):
    not_in_positions.append(
        st.text_input("", key=f"not_pos_{i}", label_visibility='collapsed', placeholder="", help="", disabled=False)
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- Исключённые буквы ---
excluded_input = st.text_input("Исключённые буквы (через запятую)", key="excluded")
excluded_letters = set(x.strip() for x in excluded_input.lower().split(",") if x.strip())

# --- Логика поиска ---
results = []
for word in dictionary:
    if excluded_letters & set(word):
        continue
    if any(fp and word[i] != fp.lower() for i, fp in enumerate(fixed_positions)):
        continue
    skip_word = False
    for i, field in enumerate(not_in_positions):
        if field.strip():
            letters = set(x.strip() for x in field.lower().split(",") if x.strip())
            if word[i] in letters:
                skip_word = True
                break
            if not letters & set(word):
                skip_word = True
                break
    if skip_word:
        continue
    results.append(word)

# --- Вывод ---
st.write(f"Найдено {len(results)} слов:")
st.dataframe(results, use_container_width=True)
