import time
import json
import telebot

# token details
TOKEN = "TRON"

BOT_TOKEN = "6055390089:AAHI43mzycXTS4pSg8ITSlujnPTk_WFlAWo"
PAYMENT_CHANNEL = "@testpostchnl"
OWNER_ID = 123456789
CHANNELS = ["@testpostchn"]

#adding bonus details
Daily_bonus = 1
Mini_withdraw = 1
Per_Refer = 0.0001

bot = telebot.TeleBot(BOT_TOKEN)

def check_user(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status == "left":
            pass
        else:
            return False
    return True

bonus = {}

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '🎁 Bonus', '💸 Withdraw')
    keyboard.row('⚙️ Set Wallet', '📊Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == "/start":
            user = str(user)
            data = json.load(open("users.json", 'r'))
            if user not in data['referred']:
                data['referrals'][user] = 0
                data['total'] = data['total'] + 1
            
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = "0"
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open("users.json", 'w'))
            print(data)

            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text = "👥 Join Channel"))
            msg_start = "Welcome to *TRON* Bot\n\n*🆔 Account ID:* `{}`\n*👥 Referrals:* `{}`\n*💸 Balance:* `{}` TRX\n*🎁 Bonus:* `{}` TRX\n*💰 Withdraw:* `{}` TRX\n\n*📊 Statistics*\n*👥 Total Users:* `{}`\n*👥 Total Referrals:* `{}`\n*💸 Total Withdraw:* `{}` TRX\n\n*📢 Note:* *You can withdraw your balance after 24 hours of joining.*".format(data['id'][user], data['referrals'][user], data['balance'][user], data['checkin'][user], data['withd'][user], data['total'], data['totalref'], data['totalwithd'])
            for i in CHANNELS:
                msg_start += f"\n➡️ {i}\n"
            msg_start += "*"

            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markup)
        else:
            data = json.load(open('users.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('users.json', 'w'))
            print(data)
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "Welcome to *TRON* Bot\n\n*🆔 Account ID:* `{}`\n*👥 Referrals:* `{}`\n*💸 Balance:* `{}` TRX\n*🎁 Bonus:* `{}` TRX\n*💰 Withdraw:* `{}` TRX\n\n*📊 Statistics*\n*👥 Total Users:* `{}`\n*👥 Total Referrals:* `{}`\n*💸 Total Withdraw:* `{}` TRX\n\n*📢 Note:* *You can withdraw your balance after 24 hours of joining.*".format(data['id'][user], data['referrals'][user], data['balance'][user], data['checkin'][user], data['withd'][user], data['total'], data['totalref'], data['totalwithd'])
            bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "Something went wrong, please try again later.")
        bot.send_message(OWNER_ID, "Your Bot got an error on command : " + message.text)
        return
    

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        ch = check_user(call.message.chat.id)
        if call.data == 'check':
            if ch == True:
                data = json.load(open('users.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id= = call.id,
                    text = "You have already joined all the channels, Now u can earn money",
                    show_alert = True)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                if user not in data['refer']:
                    data['refer'][user] = True

                    if user not in data['referby']:
                        data['referby'][user] = user
                        json.dump(data, open('users.json', 'w'))
                    if int(data['refereby'][user]) != user_id:
                        ref_id = data['referby'][user]
                        ref = str(ref_id)
                        if ref not in data['balance']:
                            data['balance'][ref] = 0
                        if ref not in data['referred']:
                            data['referred'][ref] = 0
                        json.dump(data, open('users.json', 'w'))
                        data['balance'][ref] += Per_Refer
                        data['referred'][ref] += 1

                        bot.send_message(
                            ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                        json.dump(data, open('users.json', 'w'))
                        return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)
            else:
                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)
        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='❌ You not Joined')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "Something went wrong, please try again later.")
        bot.send_message(OWNER_ID, "Your Bot got an error on command : " + call.data)
        return
    
@bot.message_handler(commands_types=['text'])
def send_text(message):
    try:
        if message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('users.json', 'w'))
            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.chat.first_name, wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
        if message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Refferrals System\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referral Link ⬇️\n{}*"
            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = 'https://telegram.me/{}?start={}'.format(
                bot_name, message.chat.id)
            
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
        
        if message.text == "⚙️ Set Wallet":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🔙 Back')
            send = bot.send_message(message.chat.id, "_⚠️Send your TRX Wallet Address._",
                                parse_mode="Markdown", reply_markup=keyboard)
            bot.register_next_step_handler(message, trx_address)
        
        if message.text == "🎁 Bonus":
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('users.json', 'r'))

            if(user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 60 * 60 * 24):
                data['balance'][user] += Daily_bonus
                bot.send_message(
                    user_id, f"Congrats You have just received {Daily_bonus} {TOKEN}")
                bonus[user_id] = cur_time
                json.dump(data, open('users.json', 'w'))
            else:
                bot.send_message(
                    user_id, f"Sorry You have already received your daily bonus for the day", parse_mode="Markdown")
            
            return
    
        if message.text == "💸 Withdraw":
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('users.json', 'w'))

            bal = data['balance'][user]
            wall = data['wallet'][user]
            if wall == "none":
                bot.send_message(message.chat.id, "⚠️ You need to set your wallet address first.")
                return
            if bal >= Mini_withdraw:
                bot.send_message(user_id, "_Enter Your Amount to Withdraw._", parse_mode="Markdown")
                bot.register_next_step_handler(message, amo_with)
            else:
                bot.send_message(user_id, f"⚠️ You need to have at least {Mini_withdraw} {TOKEN} to withdraw.")
                return

    except:
        bot.send_message(message.chat.id, "Something went wrong, please try again later.")
        bot.send_message(OWNER_ID, "Your Bot got an error on command : " + message.text)
        return
    
def trx_address(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if len(message.text) == 34:
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            data['wallet'][user] = message.text

            bot.send_message(message.chat.id, "*💹Your Trx wallet set to " +
                         data['wallet'][user]+"*", parse_mode="Markdown")
            json.dump(data, open('users.json', 'w'))
            return menu(message.chat.id)
        else:
            bot.send_message(message.chat.id, "⚠️ Invalid Wallet Address.", parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "Something went wrong, please try again later.")
        bot.send_message(OWNER_ID, "Your Bot got an error on command : " + message.text)
        return
    
def amo_with(message):
    try:
        user_id = message.chat.id
        user = str(user_id)
        amo = message.text
        data = json.load(open('users.json', 'r'))
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        json.dump(data, open('users.json', 'w'))

        bal = data['balance'][user]
        # wall = data['wallet'][user]
        msg = message.text

        if msg.isdigit() == False:
            bot.send_message(message.chat.id, "⚠️ Please enter a valid amount." parse_mode="Markdown")
            return
        if int(message.text) < Mini_withdraw:
            bot.send_message(message.chat.id, f"⚠️ You need to have at least {Mini_withdraw} {TOKEN} to withdraw.")
            return
        if int(message.text) > bal:
            bot.send_message(message.chat.id, f"⚠️ You don't have enough balance to withdraw.")
            return
        amo = int(amo)
        data['balance'][user] -= int(amo)
        data['totalwith'] += int(amo)
        bot_name = bot.get_me().username
        json.dump(data, open('users.json', 'w'))
        bot.send_message(message.chat.id, f"✅ You have successfully withdrawn {amo} {TOKEN} to your wallet.")

        markupp = telebot.types.InlineKeyboardMarkup()
        markupp.add(telebot.types.InlineKeyboardButton(text='🍀 BOT LINK', url=f'https://telegram.me/{bot_name}?start={OWNER_ID}'))

        # send = bot.send_message(PAYMENT_CHANNEL,  "✅* New Withdraw\n\n⭐ Amount - "+str(amo)+f" {TOKEN}\n🦁 User - @"+message.from_user.username+"\n💠 Wallet* - `"+data['wallet'][user]+"`\n☎️ *User Referrals = "+str(
        #     data['referred'][user])+"\n\n🏖 Bot Link - @"+bot_name+"\n⏩ Please wait our owner will confrim it*", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markupp)
        bot.send_message(PAYMENT_CHANNEL,  "✅* New Withdraw\n\n⭐ Amount - "+str(amo)+f" {TOKEN}\n🦁 User - @"+message.from_user.username+"\n💠 Wallet* - `"+data['wallet'][user]+"`\n☎️ *User Referrals = "+str(
            data['referred'][user])+"\n\n🏖 Bot Link - @"+bot_name+"\n⏩ Please wait our owner will confrim it*", parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markupp)
    
    except:
        bot.send_message(message.chat.id, "Something went wrong, please try again later.")
        bot.send_message(OWNER_ID, "Your Bot got an error on command : " + message.text)
        return
    

if __name__ == '__main__':
    bot.polling(none_stop=True)