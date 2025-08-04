import streamlit as st

# Стилизация CSS
st.markdown("""
    <style>
        .title-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }
        .title-box {
            display: flex;
            gap: 5px;
        }
        .letter-box {
            width: 40px;
            height: 40px;
            background-color: yellow;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 20px;
            border: 1px solid black;
        }
        .reset-button {
            background-color: yellow;
            color: black;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .reset-button:hover {
            background-color: #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

# HTML для заголовка и кнопки сброса
st.markdown("""
    <div class="title-container">
        <div class="title-box">
            <div class="letter-box">5</div>
            <div class="letter-box">Б</div>
            <div class="letter-box">У</div>
            <div class="letter-box">К</div>
            <div class="letter-box">В</div>
        </div>
        <form action="">
            <button class="reset-button" type="submit">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)
