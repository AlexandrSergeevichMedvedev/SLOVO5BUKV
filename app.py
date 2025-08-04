st.markdown("""
    <style>
    /* Контейнер для всех вводимых полей */
    .input-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 20px;
    }

    /* Ряд фиксированных позиций */
    .input-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    /* Квадратные ячейки */
    .input-square input {
        width: 50px !important;
        height: 50px !important;
        text-align: center;
        font-size: 24px;
        background-color: white !important;
        border: 2px solid #000000;
        border-radius: 5px;
    }

    /* Секция для "буквы есть в слове, но не в позиции" */
    .not-in-position-grid {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    /* Секция для исключённых букв */
    .excluded-letters {
        margin-bottom: 20px;
    }

    /* Стили кнопки сброса */
    .reset-button {
        position: absolute;
        top: 20px;
        right: 20px;
        background-color: yellow;
        color: black;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
    }

    </style>
""", unsafe_allow_html=True)
