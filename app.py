import streamlit as st

# === CSS стили ===
st.markdown("""
    <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .title-box {
            display: flex;
            gap: 5px;
        }
        .title-letter {
            background-color: yellow;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
        }
        .reset-button {
            background-color: yellow;
            color: black;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        .input-container {
            display: flex;
            gap: 10px;
            margin-top: 40px;
        }
        .input-square input {
            width: 50px !important;
            height: 50px !important;
            text-align: center;
            font-size: 24px;
        }
    </style>
""", unsafe_allow_html=True)

# === Верхняя панель: 5БУКВ и кнопка СБРОС ===
st.markdown("""
    <div class="header-container">
        <div class="title-box">
            <div class="title-letter">5</div>
            <div class="title-letter">Б</div>
            <div class="title-letter">У</div>
            <div class="title-letter">К</div>
            <div class="title-letter">В</div>
        </div>
        <form action="" method="post">
            <button class="reset-button" type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# === Поля ввода фиксированных букв ===
st.markdown('<div class="input-container">', unsafe_allow_html=True)

fixed_positions = []
for i in range(5):
    letter = st.text_input("", max_chars=1, key=f"fixed_{i}", label_visibility='collapsed')
    fixed_positions.append(letter.upper())

st.markdown('</div>', unsafe_allow_html=True)
