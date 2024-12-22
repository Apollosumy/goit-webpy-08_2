import pika
import json
from models import Contact

# Імітація надсилання email (функція-заглушка)
def send_email(contact):
    print(f"Надсилання email до: {contact.email}")
    return True

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Обробка повідомлення
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']

    # Отримання контакту з бази
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if send_email(contact):  # Імітація надсилання
            contact.sent = True
            contact.save()  # Оновлюємо статус у базі
            print(f"Email надіслано контакту {contact.fullname}, статус оновлено.")
        else:
            print(f"Помилка надсилання email контакту {contact.fullname}.")
    else:
        print(f"Контакт із ID {contact_id} не знайдено.")

# Підписка на чергу
channel.basic_consume(
    queue='email_queue',
    on_message_callback=callback,
    auto_ack=True
)

print('Очікування повідомлень...')
channel.start_consuming()
