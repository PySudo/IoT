from main_api import *
from .core import db, cfg
from .core.buttons import *
from .core.functions import (
    isAdmin,
    bot,
)

@app.post('/Telegram')
async def GetDataFromTelegram(key: str, data: dict = Body(...,embed=False)):
    if key != cfg.KEY:
        return
  
    if 'message' in data:
        message = data['message']
        text = message['text']
        message_id = message['message_id']
        chat_type = message['chat']['type']
        user = message['from']['id']
        data_type = 1

    elif 'callback_query' in data:
        callback_query = data['callback_query']
        callback_data = callback_query['data']
        callback_id = callback_query['id']
        user = callback_query['from']['id']
        data_type = 2
    else:
        data_type = None

    step = (await db.GetStep(user)).split('/')
    mess_id = await db.GetMEssageID(user)
    if not (await isAdmin(user)):
        if user == cfg.ADMIN:
            await db.addAdmin(user)
        else:
          return

    if data_type == 1:

        if chat_type != 'private':
            return

        if text == '/start':
            if mess_id:
                bot.Delete(user, mess_id)
            mess = bot.SendMessage(user, '🐙 Hello welcome to the control panel', Menu)
            await db.SetMessageID(user, mess['result']['message_id'])
            await db.SetStep(user, 'home')

        else:
            bot.Delete(user, message_id)

        match step[0]:
            case 'addAdmin':
                if text.isdigit():
                    await db.addAdmin(text)
                    bot.EditMessage(user, f'✅ [Admin](tg://user?id={text}) added successfully', mess_id, Menu, 'MarkDown')
                    await db.SetStep(user, 'home')
                else:
                    bot.EditMessage(user, f'❌ Send a valid userid', mess_id, back)
            case 'addPin':
                if text.isdigit():
                    await db.SetStep(user, 'addPin2/'+text)
                    bot.EditMessage(user, '🏷 Enter a name for GPIO '+text, mess_id, back)
                else:
                    bot.EditMessage(user, f'❌ GPIO number should be a digit', mess_id, back)

            case 'addPin2':
                await DB.addPin(step[1], text)
                bot.EditMessage(user, '✅ Pin added successfully', mess_id, Menu)
                await db.SetStep(user, 'home')

    elif data_type == 2:

        command = callback_data.split('/')
        match command[0]:
            case 'back':
                bot.EditMessage(user, '👇🏼 use the below buttons.', mess_id, Menu)
                await db.SetStep(user, 'home')

            case 'pinSettings':
                bot.EditMessage(user, '⚙️  You can add or remove your MicroController pins to the bot using this panel', mess_id, PinSettings)

            case 'addAdmin':
                bot.EditMessage(user, '🆔 Okay send me the admin userid that you want to add', mess_id, back)
                await db.SetStep(user, callback_data)
                
            case 'removeAdmin':
                if user == cfg.ADMIN:
                    admins = await db.GetAllAdmins()
                    if len(admins) > 1:
                        text = '👇🏼 Choose the admin to remove'
                        button = GenerateButton([{str(admin_id):'RM/'+str(admin_id)} for admin_id in admins if admin_id != cfg.ADMIN]+[{'🔙': 'back'}])
                        bot.EditMessage(user, text, mess_id, button)
                    else:
                        bot.Answer(callback_id, '❌ There is no admin')
                else:
                    bot.Answer(callback_id, '❌ You don\'t have access to this section.')
              
            case 'RM':
                button = GenerateButton(
                    [
                        {
                            '✅': 'YRM/'+command[1],
                            '❌': 'back'
                        }
                    ]
                )
                bot.EditMessage(user, f'🤨 Are you sure about removing [{command[1]}](tg://user={command[1]})?', mess_id, button, 'MarkDown')
              
            case 'YRM':
                await db.delAdmin(command[1])
                bot.EditMessage(user, '✅ Admin removed successfully.', mess_id, Menu)
            
            case 'addPin':
                bot.EditMessage(user, '📍 Send the GPIO number of pin that you want to add', mess_id, back)
                await db.SetStep(user, callback_data)
            
            case 'removePin':
                text = '👇🏼 Choose the GPIO number to remove'
                GPIOs = await DB.GetAllPins()
                if len(GPIOs) > 0:
                    button = GenerateButton([{str(GPIO_number):'RMG/'+str(GPIO_number)} for GPIO_number in GPIOs]+[{'🔙': 'back'}])
                    bot.EditMessage(user, text, mess_id, button)
                else:
                    bot.Answer(callback_id, '❌ There is no pin')

            case 'RMG':
                button = GenerateButton(
                    [
                        {
                            '✅': 'YRMG/'+command[1],
                            '❌': 'back'
                        }
                    ]
                )
                bot.EditMessage(user, f'🤨 Are you sure about removing the GPIO{command[1]}?', mess_id, button)

            case 'YRMG':
                await DB.delPin(command[1])
                bot.EditMessage(user, '✅ Pin removed successfully', mess_id, Menu)
            
            case 'controlPanel':
                text = '👇🏼 The status of the pins is here, click the button to change the status\n\n🔴 = off\n🟢 = on'
                all_pins = await DB.GetAllPins2()
                button = GenerateButton([{str('🔴' if not i[2] else '🟢')+' '+str(i[1]):'Change/'+str(i[0])} for i in all_pins]+[{'🔙': 'back'}])
                bot.EditMessage(user, text, mess_id, button)

            case 'Change':
                await DB.ChangeValue(int(command[1]))
                all_pins = await DB.GetAllPins2()
                button = GenerateButton([{str('🔴' if not i[2] else '🟢')+' '+str(i[1]):'Change/'+str(i[0])} for i in all_pins]+[{'🔙': 'back'}])
                bot.EditMessage(user, f'👇🏼 The status of pin {command[1]} has changed, wait for the microcontroller\n\n🔴 = off\n🟢 = on', mess_id, button)