from peewee import *

db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_table = 'Users'
    vk_id = IntegerField()
    dost = IntegerField()

class Setting(Model):
    class Meta():
        database = db
        db_table = 'Settings'
    chatid = IntegerField()
    start = IntegerField()

if __name__ == '__main__':
    db.create_tables([User])
    db.create_tables([Setting])
