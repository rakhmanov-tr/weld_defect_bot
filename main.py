import os
import time
import nest_asyncio
import logging
import telebot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import io
from collections import Counter

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Замените на ваш токен
TELEGRAM_TOKEN = 'Токен из BotFather'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Путь к модели YOLOv8s
MODEL_PATH = 'model/yolov8s.pt'

# Загрузка модели YOLOv8s
model = YOLO(MODEL_PATH)

# Определение цветов для каждого класса
colors = {
    0: (255, 0, 0),  # Красный
    1: (0, 255, 0),  # Зеленый
    2: (0, 0, 255),  # Синий
    3: (255, 255, 0),  # Желтый
    4: (0, 255, 255)  # Голубой
}

# Словарь с названиями классов
class_names = {
    0: "adj",
    1: "int",
    2: "geo",
    3: "pro",
    4: "non"
}

class_desc = {
    "adj": "прилегающие дефекты - брызги, прожоги от дуги",
    "int": "дефекты целостности - кратер, шлак, свищ, пора, прожог, включения",
    "geo": "дефекты геометрии   - подрез, непровар, наплыв, чешуйчатость, западание, неравномерность",
    "pro": "дефекты постобработки - заусенец, торец, задир, забоина",
    "non": "дефекты невыполнения - незаполнение раковины, несплавление"
}

# Разрешить вложенные циклы событий
nest_asyncio.apply()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    await bot.send_message(chat_id=update.message.chat.id,
                           text=f'Привет, <b>{update.message.from_user.first_name}</b>! Я мастер в мире изображений сварных швов, где моя речь — это детали, а мой диалог — поиск недостатков. В этой сфере я не разговариваю, я обнаруживаю',
                           parse_mode="html")
    await help_command(update, context)  # Вызов команды help при старте

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        'Я мастер в мире изображений сварных швов, где моя речь — это детали, а мой диалог — поиск недостатков. В этой сфере я не разговариваю, я обнаруживаю.\n '
        '\n'
        'Доступные команды:\n'
        '/start - Начать работу с ботом.\n'
        '/help - Показать эту справку.\n'
    )
    await update.message.reply_text(help_text)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"{user.id}_image.jpg"
    await photo_file.download_to_drive(photo_path)

    processing_message = await update.message.reply_text('Обрабатываю изображение...')

    start_time = time.time()

    # Загрузка изображения
    image = Image.open(photo_path)

    # Предсказание с использованием модели YOLOv8s
    results = model.predict(image)

    # Обработка результатов предсказания
    defect_counter = Counter()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Days.ttf", size=36)  # Увеличенный размер шрифта
    font_cls = ImageFont.truetype("arial.ttf", size=24)

    for result in results:
        boxes = result.boxes  # Получение bounding boxes
        for box in boxes:
            class_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Рисование bounding box на изображении
            draw.rectangle([x1, y1, x2, y2], outline=colors[class_id], width=3)

            # Добавление названия класса без фона
            text_bbox = draw.textbbox((0, 0), class_names[class_id], font=font_cls)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            draw.text((x1, y1 - text_height - 5), class_names[class_id], fill=colors[class_id], font=font_cls)

            # Подсчет дефектов
            defect_counter[class_id] += 1

    # Добавление водяного знака, если дефекты не обнаружены
    if not defect_counter:
        draw.text((10, 10), "Дефекты не обнаружены", fill=(0, 255, 0, 128), font=font)

    # Сохранение изображения в буфер
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    end_time = time.time()

    # Отправка обработанного изображения
    await update.message.reply_photo(photo=output_buffer,
                                     caption=f'Время выполнения: {end_time - start_time:.2f} секунд')

    # Формирование сообщения о дефектах
    if defect_counter:
        defect_message = f"На загруженном изображении найдены следующие виды дефектов:\n"
        for class_id, count in defect_counter.items():
            defect_message += f"{class_names[class_id]}: {count} - {class_desc[class_names[class_id]]}\n"
        await update.message.reply_text(defect_message)
    else:
        await update.message.reply_text("На изображении дефекты не обнаружены.")

    # Удаление временного файла и сообщения о обработке
    os.remove(photo_path)
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=processing_message.message_id)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    logger.info("Starting polling...")
    application.run_polling()


if __name__ == '__main__':
    main()