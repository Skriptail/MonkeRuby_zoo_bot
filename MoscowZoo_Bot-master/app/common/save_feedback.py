import json
import os

current_dir = os.path.dirname(__file__)
feedback_file_path = os.path.join(current_dir, 'feedback.json')

async def save_feedback(feedback_info: dict):
    filename = feedback_file_path

    # Если файл существует, загружаем его содержимое
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                feedback_data = json.load(f)
            except json.JSONDecodeError:
                feedback_data = []
    else:
        feedback_data = []

    # Добавляем новый отзыв в список
    feedback_data.append(feedback_info)

    # Сохраняем обновленный список в файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, ensure_ascii=False, indent=4)
