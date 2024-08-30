from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot_config import database

survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    gender = State()
    occupation = State()


@survey_router.message(Command("opros"))
async def start_opros(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(BookSurvey.name)


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет ?")
    await state.set_state(BookSurvey.age)


@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Вводите только цифры")
        return
    age = int(age)
    if age < 17:
        await message.answer("Вы не можете участвовать в опросе!!!")
        await state.clear()
        return
    await state.update_data(age=message.text)
    await state.set_state(BookSurvey.gender)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Мужской")
            ],
            [
                types.KeyboardButton(text="Женский")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Какого Вы пола?", reply_markup=kb)


@survey_router.message(BookSurvey.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(BookSurvey.occupation)
    await message.answer("Ваш любимый род занятий ?", reply_markup=types.ReplyKeyboardRemove())


@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    data = await state.get_data()
    print(data)

    database.execute(
        query="INSERT INTO survey (name, age, gender, occupation) "
              "VALUES (?, ?, ?, ?)",
        params=(
            data.get('name'),
            data.get('age'),
            data.get('gender'),
            data.get('occupation')
        )

    )

    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")


