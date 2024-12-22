import pika
import json
from faker import Faker
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Генерація контактів
faker = Faker()
for _ in range(10):  # Змінюйте кількість для генерації потрібної кількості контактів
    contact = Contact(
        fullname=faker.name(),
        email=faker.email()
    )
    contact.save()  # Зберігаємо контакт у базі

    # Відправляємо повідомлення у RabbitMQ
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps(message)
    )
    print(f"Відправлено в чергу: {message}")

# Закриття підключення
connection.close()
