import streamlit as st

# ================= CSS стили ====================
st.markdown("""
    <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-title {
            display: flex;
            gap: 5px;
        }
        .header-title div {
            width: 30px;
            height: 30px;
            background-color: yellow;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            font-size: 18px;
            border-radius: 5px;
        }
        .reset-button button {
            background-color: yellow !important;
            color: black !important;
            font-weight: bold;
            border-radius: 5px;
            height: 30px;
            width: 60px;
        }
        .input-grid {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            margin-top: 10px;
            flex-wrap: nowrap;
        }
        input[id^="pos_"], input[id^="notinpos_"], input[id="excluded_letters"] {
            width: 50px !important;
            height: 50px !important;
            text-align: center;
            font-size: 24px;
            background-color: white !important;
            border: 2px solid #000000;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ============= Шапка: "5БУКВ" и Кнопка "СБРОС" ============
col1, col2 = st.columns([8, 2])
with col1:
    st.markdown("""
        <div class="header-title">
            <div>5</div>
            <div>Б</div>
            <div>У</div>
            <div>К</div>
            <div>В</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    query_params = st.query_params
    if st.button("СБРОС", key="reset_button"):
        st.query_params.clear()
        st.rerun()

# ============= Поля ввода фиксированных позиций =============
st.write("Фиксированные позиции (если известны):")
fixed_positions = []
with st.container():
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            fixed_positions.append(st.text_input("", max_chars=1, key=f"pos_{i}", label_visibility='collapsed'))

# ============= Поля "Буквы есть в слове, но не в этой позиции" =============
st.write("Буквы есть в слове, но не в этой позиции (по позициям):")
not_in_positions = []
with st.container():
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            not_in_positions.append(st.text_input("", max_chars=20, key=f"notinpos_{i}", label_visibility='collapsed'))

# ============= Поле исключённых букв =============
excluded_letters = st.text_input("Исключённые буквы (через запятую):", key="excluded_letters")

# ============= Словарь слов (пример) =============
dictionary = ["мышка", "штраф", "медик", "пирог", "пилав", "плакат", "плюха", "фигура", "фирма", "пирса"]

# ============= Алгоритм фильтрации =============
excluded_letters = set([l.strip().upper() for l in excluded_letters.split(",") if l.strip()])

# Формируем список подходящих слов
results = []
for word in dictionary:
    if len(word) != 5:
        continue
    w = word.upper()

    # Проверка фиксированных позиций
    is_valid = True
    for i, fixed in enumerate(fixed_positions):
        if fixed and w[i] != fixed.upper():
            is_valid = False
            break
    if not is_valid:
        continue

    # Проверка исключённых букв
    if any(l in w for l in excluded_letters):
        continue

    # Проверка "буквы есть, но не в этой позиции"
    for i, not_in in enumerate(not_in_positions):
        letters = [l.strip().upper() for l in not_in.split(",") if l.strip()]
        for letter in letters:
            if letter not in w or w[i] == letter:
                is_valid = False
                break
        if not is_valid:
            break

    # Проверка наличия всех букв из "буквы есть, но не в этой позиции"
    all_letters = set()
    for not_in in not_in_positions:
        letters = [l.strip().upper() for l in not_in.split(",") if l.strip()]
        all_letters.update(letters)
    if not all(letter in w for letter in all_letters):
        continue

    # Добавляем слово в результаты
    results.append(word)

# ============= Вывод результатов =============
if results:
    st.write("Возможные слова:")
    for res in results:
        st.write(res)
else:
    st.write("Нет подходящих слов.")

