import streamlit as st

# Стилизация CSS
st.markdown("""
    <style>
        .input-container {
            display: flex;
            justify-content: flex-start;
            gap: 10px;
            margin-top: 40px;
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

# Контейнер для 5 ячеек ввода
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# 5 квадратных полей ввода (фиксированные буквы)
fixed_positions = []
for i in range(5):
    letter = st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed')
    fixed_positions.append(letter.upper())

st.markdown('</div>', unsafe_allow_html=True)
