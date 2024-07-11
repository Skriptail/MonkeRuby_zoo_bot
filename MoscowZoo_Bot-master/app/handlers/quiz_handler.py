# import json
# import os
# from aiogram import types, Router, F
# from aiogram.filters import Command, or_f
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.enums import ParseMode
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# from app.keyboards import reply
# from app.common.find_animal_quiz import find_totem_animal  # Импортируем вашу функцию из другого файла
# from app.handlers.user_private import about_guardianship
# quiz_router = Router()
#
# class QuizStates(StatesGroup):
#     waiting_for_answer = State()
#
#
# current_dir = os.path.dirname(__file__)
# questions_file_path = os.path.join('C:\\Users\\User\\PycharmProjects\\monkerubyy\\MoscowZoo_Bot-master\\app\\common\\questions_with_answers.json')
#
# with open(questions_file_path, 'r', encoding='utf-8') as f:
#     questions_data = json.load(f)
#
# questions = [question for question in questions_data]
#
# async def send_next_question(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     question_index = data.get('question_index', 0)
#
#     if question_index < len(questions):
#         question = questions[question_index]
#         response = f"*{question['question']}*\n" + "\n".join(question['answers'])
#         await message.answer(response, parse_mode=ParseMode.MARKDOWN, reply_markup=reply.quiz_answers_kb)
#     else:
#         answers_count = data.get('answers_count', {'A': 0, 'B': 0, 'C': 0, 'D': 0})
#         # Получаем список ответов
#         user_answers = [answers_count['A'], answers_count['B'], answers_count['C'], answers_count['D']]
#         animal_name, animal_image_url, about_animal = await find_totem_animal(user_answers)
#
#         await message.answer(
#             f"Викторина завершена! Спасибо за участие.\n\nВаше тотемное животное:"
#             f" *{animal_name}*\n\n{about_animal}\n",
#             parse_mode=ParseMode.MARKDOWN)
#         await message.answer_photo(animal_image_url, reply_markup=reply.start_kb)
#
#         # Создание кнопки "Поделиться"
#         share_text = f"Я прошел викторину и мое тотемное животное: {animal_name}!\n{about_animal}"
#         vk_share_url = f"https://vk.com/share.php?url=https://t.me/MoscowZoo_Filipp_bot&title={share_text}&image={animal_image_url}"
#         share_button = InlineKeyboardButton(text="Поделиться в VK", url=vk_share_url)
#         share_markup = InlineKeyboardMarkup(inline_keyboard=[[share_button]])
#
#         await message.answer(
#             "Поделитесь результатами в соцсетях!",
#             reply_markup=share_markup
#         )
#
#         await state.clear()
#         await about_guardianship(message)
#
# @quiz_router.message(or_f(Command('quiz'), F.text.lower().contains('Заполнить анкету')))
# async def start_quiz(message: types.Message, state: FSMContext):
#     await message.answer("*Подпишите здесь и здесь..\n\n"
#                          "Выбирайте подходящие для вас ответы!\n"
#                          "*Удачи!*",
#                          parse_mode=ParseMode.MARKDOWN, reply_markup=reply.start_quiz_kb)
#     await state.update_data(question_index=0, answers=[], answers_count={'A': 0, 'B': 0, 'C': 0, 'D': 0})
#     await state.set_state(QuizStates.waiting_for_answer)
#     await send_next_question(message, state)
# # @quiz_router.message(or_f(Command('quiz'), F.text.lower().contains('викторин')))
# # async def start_quiz(message: types.Message, state: FSMContext):
# #     await message.answer("*Добро пожаловать в викторину!*\n\n"
# #                          "*Тема викторины:* Какое у вас тотемное животное?\n\n"
# #                          "Просто тыкай на подходящие варианты ответов!\n"
# #                          "В конце викторины получишь тотемное животное)\n\n"
# #                          "*Удачи!*",
# #                          parse_mode=ParseMode.MARKDOWN, reply_markup=reply.start_quiz_kb)
# #     await state.update_data(question_index=0, answers=[], answers_count={'A': 0, 'B': 0, 'C': 0, 'D': 0})
# #     await state.set_state(QuizStates.waiting_for_answer)
# #     await send_next_question(message, state)
#
# @quiz_router.message(F.text.lower() == 'вернуться назад', QuizStates.waiting_for_answer)
# async def go_back(message: types.Message, state: FSMContext):
#     await message.answer("Вы завершили процесс. Если хотите начать, используйте команду /quiz.",
#                          reply_markup=reply.start_kb)
#     await state.clear()
#
# @quiz_router.message(QuizStates.waiting_for_answer)
# async def handle_answer(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     question_index = data.get('question_index', 0)
#     answers = data.get('answers', [])
#     answers_count = data.get('answers_count', {'A': 0, 'B': 0, 'C': 0, 'D': 0})
#
#     if message.text in answers_count:
#         answers_count[message.text] += 1
#
#     answers.append(message.text)
#     await state.update_data(answers=answers, question_index=question_index + 1, answers_count=answers_count)
#     await send_next_question(message, state)
import json
import os
from aiogram import types, Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards import reply
from app.common.find_animal_quiz import find_totem_animal  # Импортируем вашу функцию из другого файла
from app.handlers.user_private import about_guardianship
quiz_router = Router()

class QuizStates(StatesGroup):
    waiting_for_answer = State()


current_dir = os.path.dirname(__file__)
questions_file_path = os.path.join(current_dir, '..', 'common', 'questions_with_answers.json')

with open(questions_file_path, 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

questions = [question for question in questions_data]

async def send_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_index = data.get('question_index', 0)

    if question_index < len(questions):
        question = questions[question_index]
        response = f"*{question['question']}*\n" + "\n".join(question['answers'])
        await message.answer(response, parse_mode=ParseMode.MARKDOWN, reply_markup=reply.quiz_answers_kb)
    else:
        answers_count = data.get('answers_count', {'A': 0, 'B': 0, 'C': 0, 'D': 0})
        # Получаем список ответов
        user_answers = [answers_count['A'], answers_count['B'], answers_count['C'], answers_count['D']]
        animal_name, animal_image_url, about_animal = await find_totem_animal(user_answers)

        await message.answer(
            f"Спасибо за участие!\n\nВаше тотемное животное:"
            f" *{animal_name}*\n\n{about_animal}\n",
            parse_mode=ParseMode.MARKDOWN)
        await message.answer_photo(animal_image_url, reply_markup=reply.start_kb)

        # # Создание кнопки "Поделиться"
        # share_text = f"Мое тотемное животное: {animal_name}!\n{about_animal}"
        # vk_share_url = f"https://vk.com/share.php?url=https:&title={share_text}&image={animal_image_url}"
        # share_button = InlineKeyboardButton(text="Поделиться в VK", url=vk_share_url)
        # share_markup = InlineKeyboardMarkup(inline_keyboard=[[share_button]])
        #
        # await message.answer(
        #     "Поделитесь результатами в соцсетях!",
        #     reply_markup=share_markup
        # )

        await state.clear()
        await about_guardianship(message)

@quiz_router.message(or_f(Command('quiz'), F.text.lower().contains('Заполнить анкету')))
async def start_quiz(message: types.Message, state: FSMContext):
    await message.answer("*Подпишите здесь и здесь..*\n\n"
                         "*Тема анкеты:* Какое у вас тотемное животное?\n\n"
                         "Выбирайте подходящие варианты ответов!\n"
                         "В конце я смогу назвать ваше тотемное животное)\n\n"
                         "*Удачи!*",
                         parse_mode=ParseMode.MARKDOWN, reply_markup=reply.start_quiz_kb)
    await state.update_data(question_index=0, answers=[], answers_count={'A': 0, 'B': 0, 'C': 0, 'D': 0})
    await state.set_state(QuizStates.waiting_for_answer)
    await send_next_question(message, state)

@quiz_router.message(F.text.lower() == 'вернуться назад', QuizStates.waiting_for_answer)
async def go_back(message: types.Message, state: FSMContext):
    await message.answer("Вы завершили процесс. Если хотите начать, используйте команду /quiz.",
                         reply_markup=reply.start_kb)
    await state.clear()

@quiz_router.message(QuizStates.waiting_for_answer)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_index = data.get('question_index', 0)
    answers = data.get('answers', [])
    answers_count = data.get('answers_count', {'A': 0, 'B': 0, 'C': 0, 'D': 0})

    if message.text in answers_count:
        answers_count[message.text] += 1

    answers.append(message.text)
    await state.update_data(answers=answers, question_index=question_index + 1, answers_count=answers_count)
    await send_next_question(message, state)