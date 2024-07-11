from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

from app.common.save_feedback import save_feedback
from app.keyboards import reply
from app.common.texts_list import about_text, guardianship_text


user_private_router = Router()


class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()


@user_private_router.message(or_f(Command('intro'), F.text.lower() == 'интро'), StateFilter(None))
async def start_cmd(message: types.Message):
    user = message.from_user
    await message.answer(f'Приветствую,{user.first_name}! Детектив Руби. Могу я задать вам пару вопросов? \n'
                         ' Дошли вести, что у кого-то все еще не определено тотемное животное. Вам что нибудь известно об этом?',
                         reply_markup=reply.intro_kb)

@user_private_router.message(or_f(Command('start'), F.text.lower() == 'здравствуйте, детектив, кажется, что у меня..'), StateFilter(None))
async def start_cmd(message: types.Message):
    await message.answer('В таком случае, заполните, пожалуйста, эту анкету ниже, она поможет вам определить ваше тотемное животное \n'
                         'Кстати, если хотите познакомиться с обитателями зоопарка, я могу вам показать фотографии наших прекрасных жителей',
                         reply_markup=reply.start_kb)

@user_private_router.message(or_f(Command("guardianship"), F.text.lower().contains('опекун')), StateFilter(None))
async def about_guardianship(message: types.Message):
    await message.answer(guardianship_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply.start_kb)


@user_private_router.message(or_f(Command("about"), F.text.lower() == 'о нас'), StateFilter(None))
async def about_cmd(message: types.Message):
    await message.answer(about_text,
                         parse_mode=ParseMode.MARKDOWN)


@user_private_router.message(or_f(Command("contact"), F.text.lower().contains('связаться')), StateFilter(None))
async def contact_with_us(message: types.Message):
    await message.answer("Контактные данные нашего сотрудника:\n"
                         "*Номер:* ************\n"
                         "*Почта:* denbespalov65@gmail.com", parse_mode=ParseMode.MARKDOWN,reply_markup=reply.start_kb)


@user_private_router.message(or_f(Command("feedback"), F.text.lower().contains('отзыв')), StateFilter(None))
async def feedback_cmd(message: types.Message, state: FSMContext):
    await message.answer('Чтобы оставить отзыв, просто напишите его в этом чате⬇️⬇️', reply_markup=reply.back_kb,)
    await state.set_state(FeedbackStates.waiting_for_feedback)

@user_private_router.message(F.text.lower() == 'вернуться назад', FeedbackStates.waiting_for_feedback)
async def go_back(message: types.Message, state: FSMContext):
    await message.answer(text='Вы вышли из режима отзывов',
                         reply_markup=reply.start_kb)
    await state.clear()

@user_private_router.message(FeedbackStates.waiting_for_feedback)
async def handle_feedback(message: types.Message, state: FSMContext):
    feedback_info = {
        'user_id': message.from_user.id,
        'feedback': message.text
    }
    await save_feedback(feedback_info)
    await message.answer('Спасибо за ваш отзыв!', reply_markup=reply.start_kb)
    await state.clear()


