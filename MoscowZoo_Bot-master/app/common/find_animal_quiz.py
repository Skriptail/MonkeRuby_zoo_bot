import json
import os


async def find_totem_animal(user_answers):
    current_dir = os.path.dirname(__file__)
    animals_file_path = os.path.join(current_dir, 'animals_for_quiz.json')

    with open(animals_file_path, 'r', encoding='utf-8') as f:
        animals = json.load(f)

    min_deviation = float('inf')
    best_match = None

    for animal in animals:
        deviation = sum(abs(user_answers[i] - animal['answers'][i]) for i in range(4))

        if deviation == 0:
            return animal['name'], animal['image_url']  # Полное совпадение

        if deviation < min_deviation:
            min_deviation = deviation  # Обновляем min_deviation, если текущее отклонение меньше
            best_match = animal

    return best_match['name'], best_match['image_url'], best_match['about_animal']
