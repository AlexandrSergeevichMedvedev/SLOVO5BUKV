import streamlit as st

# === Стилизация ===
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
        .input-grid {
            display: flex;
            gap: 10px;
            margin-top: 40px;
        }
        .input-grid input {
            width: 50px;
            height: 50px;
            text-align: center;
            font-size: 24px;
            border: 2px solid #ccc;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# === Верхняя панель ===
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

# === 5 квадратов ввода букв ===
st.markdown('<div class="input-grid">', unsafe_allow_html=True)

fixed_positions = []
for i in range(5):
    # Прямое HTML поле ввода (обходит ограничения Streamlit)
    fixed_positions.append(
        st.text_input("", key=f"fixed_{i}", max_chars=1, label_visibility="collapsed")
    )

st.markdown('</div>', unsafe_allow_html=True)

# === Показываем для теста ===
st.write("Введённые буквы:", fixed_positions)
