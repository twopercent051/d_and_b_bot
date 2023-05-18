from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class UserReplyKeyboard:
    """Клавиатура юзера для передачи телефона"""

    @classmethod
    def phone_keyboard(cls):
        kb = [
            [KeyboardButton(text="Оставить телефон", request_contact=True)],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard
