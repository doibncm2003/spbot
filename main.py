# File: main.py

from telegram.ext import Updater, CommandHandler
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder, Updater
from Commands import start, help_command, button_yesno, mission
import API as botAPI

def main():
    # Tạo và cấu hình ứng dụng
    application = Application.builder().token(botAPI.API_Key).build()

    application.add_handler(CommandHandler("mission", mission))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_yesno))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
