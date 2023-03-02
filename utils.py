import datetime
from models import User, Setting

def get_settings(idchat):
    try:
        return Setting().get(chatid=idchat)
    except:
        Setting(
            chatid=idchat,
            start=0
        ).save()
        return Setting().get(chatid=idchat)

def get_user_by_id(user_id):
    try:
        return User().get(vk_id=user_id)
    except:
        User(
            vk_id=user_id,
            dost=0
        ).save()
        return User().get(vk_id=user_id)
