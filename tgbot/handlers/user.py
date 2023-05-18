from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot, admin_group
from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb
from tgbot.keyboards.reply import UserReplyKeyboard as reply_kb
from tgbot.misc.states import UserFSM
from tgbot.models.redis_connector import RedisConnector
from tgbot.models.sql_connector import DBRequestsDAO

router = Router()


@router.message(Command('start'))
async def admin_start_msg(message: Message, state: FSMContext):
    """Главное меню по старту"""
    text = 'Здравствуйте! Я бот-консультант компании D and B Properties. Чем я могу вам помочь?'
    kb = inline_kb.main_menu_kb()
    await state.set_state(UserFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == 'home')
async def admin_start_clb(callback: CallbackQuery, state: FSMContext):
    """Главное меню по коллбеку"""
    text = 'Здравствуйте! Я бот-консультант компании D and B Properties. Чем я могу вам помочь?'
    kb = inline_kb.main_menu_kb()
    await state.set_state(UserFSM.home)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == 'catalog', UserFSM.home)
@router.callback_query(F.data == 'pick_up', UserFSM.home)
@router.callback_query(F.data == 'phone_advice', UserFSM.home)
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Запрос имени"""
    chapter = callback.data
    text = 'Как вас зовут?'
    # kb = inline_kb.home_kb()
    await state.update_data(chapter=chapter)
    await state.set_state(UserFSM.name)
    await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, UserFSM.name)
async def chapter_fork(message: Message, state: FSMContext):
    """Разветвление глав"""
    name = message.text
    state_data = await state.get_data()
    chapter = state_data['chapter']
    if chapter in ['catalog', 'phone_advice']:
        text = 'Оставьте свой телефон'
        kb = reply_kb.phone_keyboard()
        await state.set_state(UserFSM.contact)
    else:
        text = 'Какой тип недвижимости вас интересует?'
        kb = inline_kb.property_type_kb()
    await message.answer(text, reply_markup=kb)
    await state.update_data(name=name)


@router.message(UserFSM.contact)
async def get_contact(message: Message, state: FSMContext):
    """Получаем контакт"""
    state_data = await state.get_data()
    chapter = state_data['chapter']
    if message.contact:
        user_id = str(message.from_user.id)
        if chapter == 'catalog':
            catalog_id = await RedisConnector.get_catalog()
            text = 'Спасибо. Вот каталог недвижимости'  # Возможно отредактировать
            await bot.send_document(chat_id=user_id, document=catalog_id, caption=text,
                                    reply_markup=ReplyKeyboardRemove())
            await DBRequestsDAO.create(
                user_id=user_id,
                name=state_data['name'],
                phone=message.contact.phone_number,
                type_request='Каталог недвижимости'
            )
            await state.set_state(UserFSM.home)
        elif chapter == 'pick_up':
            text = 'Спасибо. Наш менеджер свяжется с вами в ближайшее время'  # Возможно отредактировать
            admin_text = [
                '⚠️ У Вас заявка на подбор недвижимости\n',
                f"Имя: <i>{state_data['name']}</i>",
                f"Телефон: <i>{message.contact.phone_number}</i>",
                f"Тип недвижимости: <i>{state_data['property_type']}</i>",
                f"Цель покупки: <i>{state_data['target']}</i>",
                f"Этап строительства: <i>{state_data['stage_building']}</i>",
                f"Цена: <i>{state_data['price']}</i>",
            ]
            await DBRequestsDAO.create(
                user_id=user_id,
                name=state_data['name'],
                phone=message.contact.phone_number,
                type_request='Подбор недвижимости',
                property_type=state_data['property_type'],
                target=state_data['target'],
                stage_building=state_data['stage_building'],
                price=state_data['price']
            )
            await message.answer(text, reply_markup=ReplyKeyboardRemove())
            await bot.send_message(admin_group, '\n'.join(admin_text), reply_markup=inline_kb.home_kb())
            await state.set_state(UserFSM.home)
        else:
            text = 'Укажите удобное время для связи'
            await message.answer(text, reply_markup=ReplyKeyboardRemove())
            await state.update_data(phone=message.contact.phone_number)
            await state.set_state(UserFSM.time_to_call)
    else:
        text = 'Нажмите пожалуйста кнопку Оставить телефон'
        await message.answer(text)


@router.callback_query(F.data.split(':')[0] == 'pick_up')
async def pick_up_info(callback: CallbackQuery, state: FSMContext):
    """Сбор данных для индивидуального каталога"""
    if callback.data.split(':')[1] == 'property_type':
        await state.update_data(property_type=callback.data.split(':')[2])
        text = 'Вы выбираете недвижимость для проживания или в качестве инвестиций?'
        kb = inline_kb.target_kb()
    elif callback.data.split(':')[1] == 'target':
        await state.update_data(target=callback.data.split(':')[2])
        text = 'Недвижимость на каком этапе строительства вас интересует?'
        kb = inline_kb.stage_building_kb()
    elif callback.data.split(':')[1] == 'stage_building':
        await state.update_data(stage_building=callback.data.split(':')[2])
        text = 'Недвижимость в каком ценовом диапазоне вы рассматриваете?'
        kb = inline_kb.price_kb()
    else:
        await state.update_data(price=callback.data.split(':')[2])
        text = 'Оставьте свой телефон'
        kb = reply_kb.phone_keyboard()
        await state.set_state(UserFSM.contact)
    await callback.message.answer(text, reply_markup=kb)


@router.message(F.text, UserFSM.time_to_call)
async def get_time_to_call(message: Message, state: FSMContext):
    """Получение времени для звонка"""
    text = 'Спасибо. Наш менеджер свяжется с вами в ближайшее время'
    state_data = await state.get_data()
    user_id = str(message.from_user.id)
    admin_text = [
        '⚠️ У Вас заявка на подбор недвижимости\n',
        f"Имя: <i>{state_data['name']}</i>",
        f"Телефон: <i>{state_data['phone']}</i>",
        f"Время для звонка: <i>{message.text}</i>",
    ]
    await DBRequestsDAO.create(
        user_id=user_id,
        name=state_data['name'],
        phone=state_data['phone'],
        type_request='Консультация по телефону',
        time_to_call=message.text
    )
    await message.answer(text)
    await bot.send_message(admin_group, '\n'.join(admin_text), reply_markup=inline_kb.home_kb())
