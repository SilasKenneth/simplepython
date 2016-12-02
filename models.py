from peewee import *
from datetime import datetime
from crypt import crypt
db=SqliteDatabase("./db/coding.db")
class User(Model):
    id=PrimaryKeyField()
    username=CharField()
    emailaddress=CharField(unique=True)
    password=CharField()
    created_on= DateTimeField(default=datetime.now)
    class Meta:
        database=db
class Post(Model):
    id=PrimaryKeyField()
    user=ForeignKeyField(User)
    title=CharField()
    content=TextField()
    date_posted=DateTimeField(default=datetime.now)
    class Meta:
        database=db
def initialize_db():
    db.connect()
    db.create_tables([User,Post],safe=True)
def create_data():
    user=User.create(username="Silas Kenneth",emailaddress="silaskenn@gmail.com",password=crypt("Nyamwaro2012"))
    user1=User.create(username="James Makori",emailaddress="jamesmakori@gmail.com",password=crypt("Nyamwaro2012"))
    user2=User.create(username="John Kennedy",emailaddress="johnkennedy@gmail.com",password=crypt("Nyamwaro2012"))
initialize_db()

