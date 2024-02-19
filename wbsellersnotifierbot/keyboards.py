from telegram import (
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
    )

#Кнопка Регистрация для приветственного сообщения
registration_keyboard = [[InlineKeyboardButton('Регистрация', callback_data='registration_seller')]]
registration_markup = InlineKeyboardMarkup(registration_keyboard)


#Кнопки Главного меню для пользователей
menu_users_keyboard = [[InlineKeyboardButton('Мои API ключи🔑', callback_data='wb_api_keys'),
                        InlineKeyboardButton('Статистика📊', callback_data='statisctics')],
                        [InlineKeyboardButton('Настройка уведомлений⚙️', callback_data='set_notifications')],
                        [InlineKeyboardButton('Как работать с ботом?🧐', url='https://teletype.in/@maxim-xoxlov/lVlFgZX_Q6Z')],
                        [InlineKeyboardButton('Канал автора бота', url='https://t.me/+EMEv_uPgQ7k5ZGI6')]]
menu_users_markup = InlineKeyboardMarkup(menu_users_keyboard)

#Кнопки Главного меню для админов
menu_admin_keyboard = [[InlineKeyboardButton('Все пользователи бота', callback_data='get_all_users_in_bot')],
                        [InlineKeyboardButton('Сообщение всем пользователям 📩', callback_data='send_message_all_users_in_bot')]]
for _ in menu_users_keyboard[:-2]:
    menu_admin_keyboard.append(_)
menu_admin_markup = InlineKeyboardMarkup(menu_admin_keyboard)


#Кнопки Меню Мои API ключи для пользователей
add_key = InlineKeyboardButton('➕🔑', callback_data='add_new_wb_api_key')
remove_key = InlineKeyboardButton('➖🔑', callback_data='remove_wb_api_key')
main_menu = InlineKeyboardButton('В меню↩️', callback_data='menu')
remove_add_key_users_keyboard = [add_key, remove_key]
api_keys_users_markup_add = InlineKeyboardMarkup([[main_menu, add_key]]) 
api_keys_users_markup_full = InlineKeyboardMarkup([[add_key,remove_key],[main_menu]])
button_main_menu_markup = InlineKeyboardMarkup([[main_menu]])
button_main_menu_markup_and_add_keys = InlineKeyboardMarkup([[main_menu, add_key]])
#Кнопки Да/нет для удаления API ключей пользователей
yes_no_keyboard = [
        [
            InlineKeyboardButton('Да', callback_data='confirmation_key_delition'),
            InlineKeyboardButton('Нет', callback_data='wb_api_keys'),
        ],
        [main_menu],
    ]
yes_no_delete_keys_markup = InlineKeyboardMarkup(yes_no_keyboard)
#Кнопки Да/нет для подтверждения/отмены отправки сообщения всем пользователям бота
yes_no_keyboard_for_sending_msg = [
        [
            InlineKeyboardButton('👌🏽', callback_data='confirmation_sending_msg'),
            InlineKeyboardButton('🙅', callback_data='menu'),
        ]
    ]
yes_no_sending_msg_markup = InlineKeyboardMarkup(yes_no_keyboard_for_sending_msg)
#Кнопки в меню при выгрузке базы пользователей для админов
download_users_xlsx_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Выгрузить в .xlsx 🧾', callback_data='download_users_xlsx_button')],[main_menu]])