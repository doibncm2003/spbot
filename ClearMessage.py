from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import API as key
async def clear_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Tạo bảng điều khiển inline để xác nhận xóa tất cả tin nhắn
        keyboard = [[InlineKeyboardButton("Xác nhận", callback_data='confirm_clear')],
                    [InlineKeyboardButton("Hủy bỏ", callback_data='cancel_clear')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Gửi tin nhắn với bảng điều khiển
        await update.message.reply_text("Bạn có chắc muốn xóa tất cả tin nhắn không?", reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        query.answer()

        if query.data == 'confirm_clear':
            chat_id = update.effective_chat.id
            all_messages = await context.bot.get_chat(chat_id).get_all_members()

            for member in all_messages:
                await context.bot.delete_message(chat_id=chat_id, message_id=member.message_id)

            await query.edit_message_text("Đã xóa tất cả tin nhắn trong cuộc trò chuyện.")
        elif query.data == 'cancel_clear':
            await query.edit_message_text("Đã hủy xóa tất cả tin nhắn.")
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

def main() -> None:
    # Tạo và cấu hình ứng dụng
    application = Application.builder().token(key.API_Key).build()

    # Thêm handler cho lệnh /clearall
    application.add_handler(CommandHandler("clearall", clear_all_messages))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Chạy ứng dụng
    application.run_polling()

if __name__ == "__main__":
    main()
