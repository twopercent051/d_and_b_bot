import os

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.filters.state import StateFilter

from create_bot import bot, admin_group
from tgbot.filters.admin import AdminMessageFilter, AdminCallbackQueryFilter
from tgbot.keyboards.inline import AdminInlineKeyboard as inline_kb
from tgbot.misc.file_create import create_excel
from tgbot.misc.states import AdminFSM
from tgbot.models.redis_connector import RedisConnector
from tgbot.models.sql_connector import DBRequestsDAO

router = Router()
router.message.filter(AdminMessageFilter())
router.callback_query.filter(AdminCallbackQueryFilter())


@router.message(Command('start'), StateFilter('*'))
async def admin_start_msg(message: Message, state: FSMContext):
    """Главное меню по старту"""
    text = 'Здравствуйте. Это главное меню. Выберите нужное действие'
    kb = inline_kb.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == 'home', StateFilter('*'))
async def admin_start_clb(callback: CallbackQuery, state: FSMContext):
    """Главное меню по коллбеку"""
    text = 'Здравствуйте. Это главное меню. Выберите нужное действие'
    kb = inline_kb.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == 'catalog', AdminFSM.home)
async def keywords_list(callback: CallbackQuery, state: FSMContext):
    """Вывод существующего каталога"""
    catalog_id = await RedisConnector.get_catalog()
    kb = inline_kb.home_kb()
    if catalog_id:
        try:
            text = 'Сейчас основной каталог такой. Чтобы его заменить отправьте новый каталог ответным сообщением'
            await bot.send_document(chat_id=admin_group, document=catalog_id, caption=text, reply_markup=kb)
        except TelegramBadRequest:
            text = 'Сейчас не задан каталог. Отправьте PDF-файл ответным сообщением'
            await callback.message.answer(text, reply_markup=kb)
    else:
        text = 'Сейчас не задан каталог. Отправьте PDF-файл ответным сообщением'
        await callback.message.answer(text, reply_markup=kb)
    await state.set_state(AdminFSM.get_catalog)
    await bot.answer_callback_query(callback.id)


@router.message(F.document, AdminFSM.get_catalog)
async def get_catalog(message: Message, state: FSMContext):
    """Сохранение нового каталога"""
    new_catalog = message.document.file_id
    await RedisConnector.update_catalog(new_catalog)
    text = 'Изменения сохранены.'
    kb = inline_kb.home_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == 'requests', AdminFSM.home)
async def get_requests(callback: CallbackQuery):
    """Список последних 7 обращений и полного списка"""
    requests_list = await DBRequestsDAO.get_all(limit=7)
    text = 'Последние 7 обращений. Также вы можете запросить весь список обращений в формате Excel'
    kb = inline_kb.requests_kb(requests_list=requests_list)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(':')[0] == 'request_id')
async def get_one_request(callback: CallbackQuery):
    """Карточка обращения"""
    request_id = int(callback.data.split(':')[1])
    request_profile = await DBRequestsDAO.get_one_or_none(request_id=request_id)
    text = [
        f'<b>Обращение номер <i>{request_id}</i></b>\n',
        f"<u>Клиент:</u> <i>{request_profile['name']} {request_profile['phone']}</i>",
        f"<u>Тип обращения:</u> <i>{request_profile['type_request']}</i>"
    ]
    fields = ["property_type", "target", "stage_building", "price", "time_to_call"]
    for field in fields:
        if request_profile[field]:
            text.append(f"<i>{request_profile[field]}</i>")
    kb = inline_kb.home_kb()
    await callback.message.answer('\n'.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == 'requests_list')
async def get_full_list(callback: CallbackQuery):
    """Полный список обращений"""
    requests_list = await DBRequestsDAO.get_all(limit=None)
    await create_excel(requests_list=requests_list)
    kb = inline_kb.home_kb()
    file = FSInputFile(path=f'{os.getcwd()}/all_tickets.xlsx', filename="all_tickets.xlsx")
    await bot.send_document(chat_id=admin_group, document=file, reply_markup=kb)
    await bot.answer_callback_query(callback.id)
