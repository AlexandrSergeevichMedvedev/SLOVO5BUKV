import streamlit as st

# === Стилизация ТОЛЬКО фиксированных позиций ===
st.markdown("""
    <style>
        .fixed-positions {
            display: flex;
            gap: 10px;
            align-items: flex-start;
            margin-left: 20px;
            margin-top: 40px;
        }
        .fixed-positions input {
            width: 50px !important;
            height: 50px !important;
            text-align: center;
            font-size: 24px;
            border: 2px solid #ccc;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# === Заголовок и СБРОС ===
st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="display: flex; gap: 5px;">
            <div style="background-color: yellow; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">5</div>
            <div style="background-color: yellow; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">Б</div>
            <div style="background-color: yellow; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">У</div>
            <div style="background-color: yellow; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">К</div>
            <div style="background-color: yellow; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold;">В</div>
        </div>
        <form action="" method="get" style="margin-left: 20px;">
            <button style="background-color: yellow; color: black; padding: 5px 10px; border-radius: 5px; font-weight: bold; border: none; cursor: pointer;">СБРОС</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# === Поля фиксированных позиций (5 квадратов) ===
st.markdown('<div class="fixed-positions">', unsafe_allow_html=True)

fixed_positions = []
for i in range(5):
    fixed_positions.append(
        st.text_input("", key=f"fixed_{i}", max_chars=1, label_visibility="collapsed")
    )

st.markdown('</div>', unsafe_allow_html=True)

# === Для проверки что ввели ===
st.write("Введённые фиксированные позиции:", fixed_positions)
