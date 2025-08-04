# --- Логика фильтрации ---
must_have_letters = set()  # Буквы, которые точно есть в слове
results = []

for i, field in enumerate(not_in_positions):
    if field.strip():
        letters = set(x.strip() for x in field.lower().split(",") if x.strip())
        must_have_letters.update(letters)

for word in dictionary:
    # Исключённые буквы
    if excluded_letters & set(word):
        continue
    # Фиксированные позиции
    if any(fp and word[i] != fp.lower() for i, fp in enumerate(fixed_positions)):
        continue
    # Буквы, которые не могут стоять в данной позиции
    skip_word = False
    for i, field in enumerate(not_in_positions):
        if field.strip():
            letters = set(x.strip() for x in field.lower().split(",") if x.strip())
            if word[i] in letters:
                skip_word = True
                break
    if skip_word:
        continue
    # Буквы, которые точно есть в слове (из ячеек not_in_positions)
    if not must_have_letters.issubset(set(word)):
        continue
    results.append(word)
