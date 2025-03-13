from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TOKEN, MASTER_IDS
from database import connect_db

# Главное меню
def get_keyboard(role):
    if role == 'Мастер':
        buttons = [['✅ Выдать задание', '📋 Список рабочих'],
                   ['🗑️ Обнулить прогресс', '❌ Удалить рабочего'],
                   ['📊 Детали по рабочему']]
    else:
        buttons = [['📥 Получить задание', '➕ Добавить деталь'],
                   ['🔧 Заявка на ремонт станка', '📞 Вызов мастера'],
                   ['📊 Мой прогресс']]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Обработка команды /start
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    role = 'Мастер' if user_id in MASTER_IDS else 'Рабочий'
    update.message.reply_text(f"Привет, {role}!", reply_markup=get_keyboard(role))

# Обработка всех кнопок
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == '📥 Получить задание':
        update.message.reply_text('Получил задание ✅')
    elif text == '➕ Добавить деталь':
        update.message.reply_text('Введите название детали:')
    elif text == '🔧 Заявка на ремонт станка':
        update.message.reply_text('Введите номер станка и причину поломки:')
    elif text == '📞 Вызов мастера':
        update.message.reply_text('🔔 Мастер вызван!')

    elif text == '✅ Выдать задание':
        update.message.reply_text('Введите деталь, количество и срок:')
    elif text == '📋 Список рабочих':
        update.message.reply_text('🛠️ Список всех рабочих')
    elif text == '🗑️ Обнулить прогресс':
        update.message.reply_text('Прогресс рабочих обнулён 🔥')
    elif text == '❌ Удалить рабочего':
        update.message.reply_text('Введите ID рабочего для удаления:')
    elif text == '📊 Детали по рабочему':
        update.message.reply_text('Выберите рабочего для просмотра его деталей:')
    elif text == '📊 Мой прогресс':
        update.message.reply_text('Ваш прогресс по деталям:')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()