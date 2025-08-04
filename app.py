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
            border: none;
            cursor: pointer;
        }
        .square-container {
            display: flex;
            gap: 10px;  /* Расстояние между квадратами */
            justify-content: flex-start; /* Ставим квадраты слева */
            margin-top: 40px;
        }
        .empty-square {
            width: 50px;
            height: 50px;
            border: 2px solid #000;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: white;
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
        <form action="" method="get">
            <button class="reset-button" type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# === 5 пустых квадратов в одну строку ===
st.markdown('<div class="square-container">', unsafe_allow_html=True)

# Пять пустых квадратов
squares_html = ''.join(['<div class="empty-square"></div>' for _ in range(5)])
st.markdown(squares_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
