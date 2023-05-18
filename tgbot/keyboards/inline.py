from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminInlineKeyboard(InlineKeyboardMarkup):
    """Клавиатуры админа"""

    @classmethod
    def main_menu_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
            [InlineKeyboardButton(text='Заявки', callback_data='requests')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def home_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(text='🏡 Домой', callback_data='home')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def requests_kb(cls, requests_list: list) -> InlineKeyboardMarkup:
        keyboard = []
        for request in requests_list:
            request_id = request['id']
            request_type = request['type_request']
            keyboard.append([InlineKeyboardButton(text=f'ID: {request_id} || Тип запроса: {request_type}',
                                                  callback_data=f'request_id:{request_id}')])
        keyboard.append([InlineKeyboardButton(text='📋 Полный перечень', callback_data='requests_list')])
        keyboard.append([InlineKeyboardButton(text='🏡 Домой', callback_data='home')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard


class UserInlineKeyboard:
    """Клавиатуры юзера"""

    @classmethod
    def main_menu_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Скачать каталог недвижимости', callback_data='catalog')],
            [InlineKeyboardButton(text='Подобрать недвижимость', callback_data='pick_up')],
            [InlineKeyboardButton(text='Консультация по телефону', callback_data='phone_advice')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def home_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(text='🏡 Домой', callback_data='home')]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def property_type_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Апартаменты', callback_data='pick_up:property_type:Апартаменты')],
            [InlineKeyboardButton(text='Таунхаусы', callback_data='pick_up:property_type:Таунхаусы')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def target_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Для проживания', callback_data='pick_up:target:Для проживания')],
            [InlineKeyboardButton(text='В качестве инвестиций', callback_data='pick_up:target:В качестве инвестиций')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def stage_building_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='Готовые объекты', callback_data='pick_up:stage_building:Готовые объекты')],
            [InlineKeyboardButton(text='Строящиеся комплексы',
                                  callback_data='pick_up:stage_building:Строящиеся комплексы')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

    @classmethod
    def price_kb(cls) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(text='до $300 тыс', callback_data='pick_up:price:до $300 тыс')],
            [InlineKeyboardButton(text='$300-500 тыс', callback_data='pick_up:price:$300-500 тыс')],
            [InlineKeyboardButton(text='$500 тыс-1 $млн', callback_data='pick_up:price:$500 тыс-1 $млн')],
            [InlineKeyboardButton(text='более $1млн', callback_data='pick_up:price:более $1млн')],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return keyboard

