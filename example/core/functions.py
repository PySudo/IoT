from . import cfg, db
from requests import post
from json import dumps

async def isAdmin(id):
    return id in (await db.GetAllAdmins())

def GenerateButton(buttons):
    out = list()
    for button in buttons:
        buffer = list()
        for text, callback_data in button.items():
            buffer.append({'text': text, 'callback_data': callback_data})
        out.append(buffer)
    return dumps({'inline_keyboard': out})

class Bot:
    def __init__(self, token):
        self.token = token
        self.API = f'https://api.telegram.org/bot{token}/'

    def __send_req(self, method, data):
        return post(self.API+method, data=data).json()

    def SendMessage(self, chat_id, message, buttons=None, parse_mode=None):
        data = {
            'chat_id': chat_id,
            'text': message,
            'reply_markup': buttons,
            'parse_mode': parse_mode
        }
        return self.__send_req('sendmessage', data)
    
    def Delete(self, chat_id, message_id):
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        return self.__send_req('deleteMessage', data)

    def EditMessage(self, chat_id, message, message_id, buttons=None, parse_mode=None):
        data = {
            'chat_id': chat_id,
            'text': message,
            'message_id': message_id
        }
        if buttons:
            data['reply_markup'] = buttons
        if parse_mode:
            data['parse_mode'] = parse_mode
        return self.__send_req('editMessageText', data)
    
    def Answer(self, callback_query_id, message):
        data = {
            'callback_query_id': callback_query_id,
            'text': message
        }
        return self.__send_req('answerCallbackQuery', data)
    

bot = Bot(cfg.TOKEN)