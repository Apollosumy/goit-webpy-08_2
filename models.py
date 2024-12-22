from mongoengine import Document, StringField, BooleanField, connect

# Підключення до бази даних
connect(host="mongodb+srv://sumyultras88:Ghbdtn_123456@cluster0.4nl1k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Модель контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)
