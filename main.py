import vk_api, pymysql, utils
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from datetime import datetime, timedelta

current = datetime.today().replace(microsecond=0)
nodost = "⚠Недостаточно прав! 😢"

host = 1 #host от базы данных
user = 1 #имя пользователя базы данных
passwd = 1 #пароль от базы данных
namebd = 1 #имя базы данных
groupid = 1 # сюда id группы, от которой будет работать бот.
token = 1 #токен от этой группы



connection = pymysql.connect(host=host, user=user, password=passwd, database=namebd, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


class VkBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(
            token=token)
        self.longpoll = MyLongPoll(self.vk_session, groupid)
    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message
                try:
                    check = event.object['message']['action']['member_id']
                    invite = event.object['message']['action']['type']
                    inv = 1
                except:
                    inv = 0

                text = msg['text']
                chatid = msg['peer_id'] - 2000000000
                print(text)

                def send(id, text): #функция отправки сообщений
                    self.vk_session.method('messages.send', {'chat_id': id, 'message': text, "random_id": 0})

                def target(tag): # вытаскиваем ID из тега вк
                    global targetname
                    screen = tag[1].split("|")[1][1:-1]
                    targetname = self.vk_session.method('utils.resolveScreenName', {'screen_name': screen})['object_id']

                if inv == 1:
                    if check == -218923880:
                        if invite == "chat_invite_user":
                            chat = utils.get_settings(chatid)
                            chat.chatid = chatid
                            chat.start = 0
                            chat.save()
                            send(chatid, "Ожидание выдачи прав администратора в беседе.")
                            while True:
                                time.sleep(3)
                                try:
                                    self.vk_session.method('messages.getConversationMembers', {'peer_id': 2000000000 + chatid})
                                    send(chatid, "Админка получена! Доступен весь функционал бота. Используйте !help для начала работы")
                                    chat.start = 1
                                    chat.save()
                                    break
                                except:
                                    print("Cant")

                user = utils.get_user_by_id(msg['from_id'])
                chat = utils.get_settings(chatid)
                if chat.start == 1:

                    if text == "!id":
                        send(chatid, f"🎲 ID беседы: {chatid}")


                    elif text == "!help":
                        send(chatid, "[BETA] 💥 Список доступных команд 💥\n\n!makefd [nick] [lvl] - установить уровень фулл-доступа\n!makeadminoff [nick] [level] - назначить администратора\n!editadmtag [nick] [prefix] - изменить префикс администратора\n!setnick [nick] [newnick] - изменить ник игрока\n!awarn [nick] [reason] - выдать админ-выговор\n!checkadm [nick] - посмотреть админ-статистику (Доступно для всех!)\n!check [nick] - просмотр статистики игрока\n!famdel [name] [reason] - удалить семью (Не работает)\n!giverub [nick] [amount] - увеличить игроку донат на\n!setrub [nick] [amount] - установить игроку донат\n!banoff [nick] [days] [reason // tag] - забанить игрока(не работает)\n!unban [nick] [reason] - разбанить игрока\n!adduser [@tagvk] - добавить пользователю возможность использовать бота\n!deluser [@tagvk] - удалить пользователю возможность использовать бота")

                    elif "!setnick" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!setnick [nick] [newnick] ")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                newnick = text[-1]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Игрока не существует')
                                else:
                                    cur.execute(f"UPDATE `Qelksekm` SET `NickName`= '{newnick}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Теперь {nick} известен, как {newnick}")
                        else:
                            send(chatid, nodost)

                    elif "!adduser" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!adduser [@tagvk]")
                            else:
                                if "@" in text[1]:
                                    target(text)
                                    tag = text
                                    screen = tag[1].split("|")[1][1:-1]
                                    targetname = self.vk_session.method('utils.resolveScreenName', {'screen_name': screen})[
                                        'object_id']
                                    setuser = utils.get_user_by_id(targetname)
                                    setuser.dost = 1
                                    setuser.save()
                                    send(chatid, f"Теперь @id{targetname} может пользоватся ботом.")
                                elif "[id" in text[1]:
                                    targetname = text[1]
                                    targetname = targetname.split("|")
                                    targetname = targetname[0][3:]
                                    setuser = utils.get_user_by_id(targetname)
                                    setuser.dost = 1
                                    setuser.save()
                                    send(chatid, f"Теперь @id{targetname} может пользоватся ботом.")
                        else:
                            send(chatid, nodost)

                    elif "!deluser" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!deluser [@tagvk]")
                            else:
                                if "@" in text[1]:
                                    target(text)
                                    setuser = utils.get_user_by_id(targetname)
                                    setuser.dost = 0
                                    setuser.save()
                                    send(chatid, f"Теперь @id{targetname} не может пользоватся ботом.")
                                elif "[id" in text[1]:
                                    targetname = text[1]
                                    targetname = targetname.split("|")
                                    print(targetname)
                                    targetname = targetname[0][3:]
                                    print(targetname)
                                    setuser = utils.get_user_by_id(targetname)
                                    setuser.dost = 1
                                    setuser.save()
                                    send(chatid, f"Теперь @id{targetname} не может пользоватся ботом.")
                        else:
                            send(chatid, nodost)


                    elif "!famdel" in text:
                        send(chatid, "Временно недоступно!")
                        #if user.dost >= 1:
                         #   text = text.split(" ")
                          #  if len(text) == 1:
                           #     send(chatid, "!famdel [Name] [Причина]")
                            #else:
                             #   cur = connection.cursor()
                              #  name = text[1]
                               # reason = text[2:]
                                #reason = ' '.join(reason)
                                #id = cur.execute(f"SELECT * FROM `Family` WHERE `name` = '{name}' LIMIT 1")
                                #print(f"{id}")
                                #if id == 0:
                                #    send(chatid, '[Ошибка] Семья с указанным названием не найдена')
                                #else:
                                #    cur.execute(f"DELETE FROM `Family` WHERE `ID` = '{id}'")
                                #    send(chatid, f"Вы удалили семью {name}. Причина: {reason}")
                        #else:
                         #   send(chatid, nodost)

                    elif "!awarn" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!awarn [nick] [reason] ")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                reason = text[2:]
                                reason = ' '.join(reason)
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Администратор с указанным ником не найден')
                                else:
                                    cur.execute(f"SELECT `NickName`, `FullDostup`, `AWarns`, `Admin`, `Reputation`, `Prefix` FROM `Qelksekm` WHERE NickName = '{nick}'")
                                    info = cur.fetchall()[0]
                                    awarn = info['AWarns'] + 1
                                    cur.execute(f"UPDATE `Qelksekm` SET `AWarns`= '{awarn}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Вы выдали выговор администратору {nick}. Причина: {reason} [{awarn} из 3]")
                                    if int(awarn) >= 3:
                                        cur.execute(f"UPDATE `Qelksekm` SET `Admin`= '0'  WHERE `ID` = '{id}'")
                                        cur.execute(f"UPDATE `Qelksekm` SET `FullDostup`= '0'  WHERE `ID` = '{id}'")
                                        send(chatid, f"Система сняла администратора {nick}. Причина: 3 из 3")
                                        cur.execute(f"UPDATE `Qelksekm` SET `AWarns`= '0'  WHERE `ID` = '{id}'")
                        else:
                            send(chatid, nodost)

                    elif "!makefd" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!makefd [nick] [lvl] ")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                level = text[-1]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Администратор с указанным ником не найден')
                                else:
                                    cur.execute(f"UPDATE `Qelksekm` SET `FullDostup`= '{level}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Вы установили {nick} {level} уровень фулл-доступа")
                        else:
                            send(chatid, nodost)

                    elif "!editadmtag" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!editadmtag [nick] [tag] ")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                tag = text[-1]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Администратор с указанным ником не найден')
                                else:
                                    cur.execute(f"UPDATE `Qelksekm` SET `Prefix`= '{tag}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Вы установили {nick} префикс {tag}")
                        else:
                            send(chatid, nodost)

                    elif "!makeadminoff" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!makeadminoff [nick] [lvl] ")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                level = text[-1]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Администратор с указанным ником не найден')
                                else:
                                    try:
                                        if level == "0":
                                            cur.execute(f"UPDATE `Qelksekm` SET `Admin`= '{level}'  WHERE `NickName` = '{nick}'")
                                            cur.execute(f"UPDATE `Qelksekm` SET `FullDostup`= '0'  WHERE `NickName` = '{nick}'")
                                            cur.execute(f"UPDATE `Qelksekm` SET `AWarns`= '0'  WHERE `ID` = '{id}'")
                                            cur.execute(f"UPDATE `Qelksekm` SET `Prefix`= ''  WHERE `NickName` = '{nick}'")
                                            send(chatid, f"Вы установили {nick} {level} уровень администратора (NeAdmin)")
                                        else:
                                            cur.execute(f"SELECT Prefix FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                            prefix = cur.fetchall()[0]['prefix']
                                            if prefix == '':
                                                cur.execute(f"UPDATE `Qelksekm` SET `Prefix`= 'Администратор'  WHERE `NickName` = '{nick}'")
                                                cur.execute(f"UPDATE `Qelksekm` SET `PrefixColor`= 'E94E4E'  WHERE `NickName` = '{nick}'")
                                            cur.execute(f"UPDATE `Qelksekm` SET `Admin`= '{level}'  WHERE `NickName` = '{nick}'")
                                            send(chatid, f"Вы установили {nick} {level} уровень администратора")
                                    except:
                                        send(chatid, f"[10] Lost connection to {connection}")
                        else:
                            send(chatid, nodost)

                    elif "!checkadm" in text:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!checkadm [nick]")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Такого игрока не существует')
                                else:
                                    cur.execute(f"SELECT `NickName`, `FullDostup`, `AWarns`, `Admin`, `Reputation`, `Prefix` FROM `Qelksekm` WHERE NickName = '{nick}'")
                                    info = cur.fetchall()[0]
                                    lvl = info['Admin']
                                    if info['Admin'] == 0:
                                        send(chatid, f"[Ошибка] Это не администратор")
                                    else:
                                        nick = info['NickName']
                                        fd = info['FullDostup']
                                        awarns = info['AWarns']
                                        rep = info['Reputation']
                                        prefix = info['Prefix']
                                        send(chatid, f"{nick} [L: {lvl} | FD: {fd}]\nВыговоры: {awarns} из 3\nРепутация: {rep}\nПрефикс: {prefix}")


                    elif "!check" in text:
                        text = text.split(" ")
                        if len(text) == 1:
                            send(chatid, "!checkadm [nick]")
                        else:
                            cur = connection.cursor()
                            nick = text[1]
                            id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                            if id == 0:
                                send(chatid, '[Ошибка] Такого игрока не существует')
                            else:
                                cur.execute(f"SELECT `NickName`, `Level`, `Money`, `Bank`, `VIP`, `Member`, `VirMoney`, `DonateMoney`, `ID` FROM `Qelksekm` WHERE NickName = '{nick}'")
                                info = cur.fetchall()[0]
                                nick = info['NickName']
                                lvl = info['Level']
                                mony = info['Money']
                                bank = info['Bank']
                                vip = info['VIP']
                                if vip <= 4:
                                    vip = "Нет"
                                elif vip == 4:
                                    vip = "TITAN"
                                elif vip == 5:
                                    vip = "PREMIUM"
                                elif vip == 6:
                                    vip = "Miking"
                                elif vip == 7:
                                    vip = "Super"
                                member = info['Member']
                                id = info['ID']
                                az = info['VirMoney']
                                azr = info['DonateMoney']
                                if member == 0:
                                    member = "нет"
                                send(chatid, f"{nick} [ID: {id}]\n\nУровень: {lvl}\nAZ: {az}\nAZ-Rub: {azr}\nВирты: {mony} [В банке: {bank}]\nВип-статус: {vip}\nОрганизация: {member}")
                                cur.execute(f"SELECT * FROM `BanNames` WHERE BINARY `Name` = '{nick}'")
                                try:
                                    ban = cur.fetchall()[0]
                                    if ban != "()":
                                        send(chatid, f"{nick} был заблокирован администратором {ban['BanAdmin']} до {ban['BanDate']}. Причина: {ban['BanReason']}")
                                except:
                                    pass

                    elif "!giverub" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!giverub [nick] [amount]")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                sum = text[2]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Такого игрока не существует')
                                else:
                                    cur.execute(f"SELECT `DonateMoney`, `ID` FROM `Qelksekm` WHERE NickName = '{nick}'")
                                    info = cur.fetchall()[0]
                                    rub = info['DonateMoney']
                                    a = int(rub)+int(sum)
                                    cur.execute(f"UPDATE `Qelksekm` SET `DonateMoney`= '{a}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Вы увеличили донат-счет игрока {nick} на {sum}. Его баланс: {a}")
                        else:
                            send(chatid, nodost)

                    elif "!setrub" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!setrub [nick] [amount]")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                sum = text[2]
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Такого игрока не существует')
                                else:
                                    cur.execute(f"UPDATE `Qelksekm` SET `DonateMoney`= '{sum}'  WHERE `NickName` = '{nick}'")
                                    send(chatid, f"Вы установили {sum} доната игроку {nick}")
                        else:
                            send(chatid, nodost)

                    elif "!banoff" in text:
                        a = 0
                        if a != 0:
                            if user.dost >= 1:
                                text = text.split(" ")
                                if len(text) == 1:
                                    send(chatid, "!banoff [nick] [days] [reason // tag]")
                                else:
                                    cur = connection.cursor()
                                    nick = text[1]
                                    days = int(text[2])
                                    reason = text[3:]
                                    reason = ' '.join(reason)
                                    id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                    if id == 0:
                                        send(chatid, '[Ошибка] Такого игрока не существует')
                                    else:
                                        cur.execute(f"SELECT * FROM `BanNames` WHERE BINARY `Name` = '{nick}'")
                                        try:
                                            a = cur.fetchall()[0]
                                            send(chatid, f"[Ошибка] Игрок уже заблокирован")
                                        except:
                                            cur.execute(f"SELECT id, MAX(id) FROM BanNames GROUP BY id")
                                            info = cur.fetchall()[-1]
                                            ids = info['id'] + 1
                                            current = datetime.today().replace(microsecond=0)
                                            time = int(datetime.timestamp(current))
                                            razban = 0
                                            for i in range(1):
                                                current += timedelta(days=days)
                                                print(current)
                                            current = str(current)
                                            razban = datetime.utcfromtimestamp(razban).strftime('%Y-%m-%d %H:%M:%S')
                                            cur.execute(f"INSERT INTO BanNames VALUES ({int(ids)}, '{nick}', 'MikingBot', '{reason}', '{time}', '{str(current)}');")
                                            send(chatid, f"Администратор MikingBot забанил игрока {nick} на {days} дней. Причина: {reason}")
                        else:
                            send(chatid, 'Nowork')

                    elif "!unban" in text:
                        if user.dost >= 1:
                            text = text.split(" ")
                            if len(text) == 1:
                                send(chatid, "!unban [nick] [reason // tag]")
                            else:
                                cur = connection.cursor()
                                nick = text[1]
                                reason = text[2:]
                                reason = ' '.join(reason)
                                id = cur.execute(f"SELECT * FROM `Qelksekm` WHERE `NickName` = '{nick}' LIMIT 1")
                                if id == 0:
                                    send(chatid, '[Ошибка] Такого игрока не существует')
                                else:
                                    cur.execute(f"SELECT * FROM `BanNames` WHERE BINARY `Name` = '{nick}'")
                                    try:
                                        ban = cur.fetchall()[0]
                                        cur.execute(f"DELETE FROM `BanNames` WHERE BINARY `Name` = '{nick}'")
                                        send(chatid, f"Администратор MikingBot разбанил игрока {nick}. Причина: {reason}")
                                    except:
                                        send(chatid, "[Ошибка] Игрок не забанен")
                                





if __name__ == '__main__':
    VkBot().run()
