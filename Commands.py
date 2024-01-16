import logging
import API as botapi
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ApplicationBuilder, Updater

user_data = {}
# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_mention = f"<b>{update.message.from_user.mention_html()}</b>"
    message = await update.message.reply_html(text=f'Chào {user_mention} tôi là Support ReelsApp. '
                                         f'\n'
                                         f'Hãy dùng <b>/mission</b> để đăng kí nhiệm vụ.')
    context.user_data['original_message_id'] = message.message_id
    await update.effective_message.delete()
async def mission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton(f"1", callback_data="1"),
            InlineKeyboardButton(f"2", callback_data="2"),
            InlineKeyboardButton(f"3", callback_data="3"),
            InlineKeyboardButton(f"4", callback_data="4"),
            InlineKeyboardButton(f"5", callback_data="5"),
        ],
        [InlineKeyboardButton("Huỷ đăng kí", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    original_message_id = context.user_data.get('original_message_id')

    if original_message_id:
        await context.bot.delete_message(update.effective_chat.id, original_message_id)

    await update.effective_message.reply_text("Vui lòng chọn số nhiệm vụ muốn làm:", reply_markup=reply_markup)
    await update.effective_message.delete()
async def button_yesno(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    choice = query.data

    # Lấy giá trị từ tin nhắn người dùng
    user_input = update.callback_query.data

    if 'user_inputs' not in context.user_data:
        context.user_data['user_inputs'] = []
    # Lưu giá trị vào danh sách context.user_data
    context.user_data['user_inputs'].append(user_input)


    if choice in ["1", "2", "3", "4", "5"]:
        await keyboard(update, context)
        await update.effective_message.delete()
    elif choice == "back":
        await update.effective_message.delete()
    else:
        await yes_and_no(update, context)
async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    choice = f"<b>{query.data}</b>"
    keyboard_option_yesno = [
        [
            InlineKeyboardButton("Xác nhận✅", callback_data="y"),
            InlineKeyboardButton("Thay đổi❌", callback_data="n"),
        ],
        [
            InlineKeyboardButton("Quay lại↩️", callback_data="back_yesno"),
        ]
    ]
    reply_markup_yesno = InlineKeyboardMarkup(keyboard_option_yesno)
    await update.callback_query.message.reply_html(text=f"Bạn có chắc đăng kí {choice} nhiệm vụ không?",
                                                   reply_markup=reply_markup_yesno)
async def yes_and_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Lấy giá trị từ context.user_data
    user_inputs = context.user_data.get('user_inputs', [])
    yesno = query.data

    num = user_inputs[0]
    print(f"{num}")

    if yesno == "y":
            datetime_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            mention = f"<b>{query.from_user.mention_html()}</b>"

            await update.callback_query.message.reply_html(f"Đã đăng kí thành công✅."
                                                           f"\nName: {mention} "
                                                           f"\nSố nhiệm vụ: <b>{num}</b> "
                                                           f"\nThời gian: <b>{datetime_now}</b>")
            await update.effective_message.delete()

    elif yesno == "n" or yesno == "back_yesno":
        await mission(update, context)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html("Sử dụng <b>/start@SpReelsApp_bot</b> để bắt đầu bot.")
    await update.effective_message.delete()
def main() -> None:
    # Tạo và cấu hình ứng dụng
    application = Application.builder().token(botapi.API_Key).build()

    application.add_handler(CommandHandler("mission", mission))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_yesno))
    application.add_handler(CallbackQueryHandler(yes_and_no))
    application.add_handler(CallbackQueryHandler(keyboard))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
