from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def save_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Lấy giá trị từ tin nhắn người dùng
    user_input = update.message.text

    # Kiểm tra xem 'user_inputs' đã được tạo chưa
    if 'user_inputs' not in context.user_data:
        context.user_data['user_inputs'] = []

    # Lưu giá trị vào danh sách context.user_data
    context.user_data['user_inputs'].append(user_input)

    await update.message.reply_text(f'Đã lưu giá trị: {user_input}')

async def show_values(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Lấy giá trị từ context.user_data
    user_inputs = context.user_data.get('user_inputs', [])

    if user_inputs:
        message_text = 'Các giá trị đã lưu:\n' + '\n'.join(user_inputs)
    else:
        message_text = 'Không có giá trị nào được lưu.'

    await update.message.reply_text(message_text)
async def clear_values(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'user_inputs' in context.user_data:
        del context.user_data['user_inputs']

    await update.message.reply_text('Đã xoá tất cả giá trị đã lưu.')

def main() -> None:
    application = Application.builder().token('6894175429:AAGgxk23QjFbHLxjAygeKrWJ0SKtp5AtBNk').build()

    application.add_handler(CommandHandler("save", save_value))
    application.add_handler(CommandHandler("show", show_values))
    application.add_handler(CommandHandler("clear", clear_values))
    application.run_polling()

if __name__ == "__main__":
    main()
