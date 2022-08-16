import os
import telebot
from telebot import *

import riddle_solver
from riddle_solver import *

TOKEN = os.environ["TOKEN"]
ANSWER = os.environ["ANSWER"]
bot = telebot.TeleBot(TOKEN)

# print(solver_type1(current_riddle))

c_guesses = 0
c_arrays = 0
c_riddle_solved = 0
c_sure = 0
answer_check = False
array_check = False
last_message = -1


def create_actions_markup():
    markup = types.InlineKeyboardMarkup()
    ans1 = types.InlineKeyboardButton("Enter an answer", callback_data="Answer_Check")
    ans2 = types.InlineKeyboardButton("Enter an array", callback_data="Array_Check")
    markup.add(ans1)
    markup.add(ans2)
    return markup


@bot.message_handler(commands=["start"])
def start(m):
    global last_message
    markup = types.InlineKeyboardMarkup()
    ans1 = types.InlineKeyboardButton('Absolutely', callback_data="Start_Riddle")
    markup.add(ans1)
    if last_message != -1:
        bot.edit_message_reply_markup(m.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
    last_message = bot.send_message(m.chat.id, "Do you want to start the riddle?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.content_type == 'text')
def checker(m):
    global answer_check, array_check, c_arrays, c_guesses, c_riddle_solved, last_message

    if answer_check:
        if not c_riddle_solved:
            c_guesses += 1
        if m.text == ANSWER:
            if c_riddle_solved:
                bot.send_message(m.chat.id, "Unsurprisingly, you are completely right")
            else:
                c_riddle_solved = 1
                bot.send_message(m.chat.id, "You are completely right, awesome guess, it took you " + str(c_guesses) + " guesses and " + str(c_arrays) + " arrays to solve that riddle, good result!")
            markup = types.InlineKeyboardMarkup()
            ans1 = types.InlineKeyboardButton('Go ahead', callback_data="Start_Riddle")
            ans2 = types.InlineKeyboardButton('Stop', callback_data="Stop_Bot")
            markup.add(ans1)
            markup.add(ans2)
            # if last_message != -1:
            #     bot.edit_message_reply_markup(m.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
            last_message = bot.send_message(m.chat.id, "If you want to analyze this puzzle a bit more, press 'Go ahead', otherwise, press 'Stop' to stop the bot", reply_markup=markup)

        else:
            bot.send_message(m.chat.id, "Sadly, you're wrong, try again")
            markup = create_actions_markup()
            # if last_message != -1:
            #     bot.edit_message_reply_markup(m.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
            last_message = bot.send_message(m.chat.id, "What do you want to do?", reply_markup=markup)

        answer_check = 0

    if array_check:
        res = str(solver_type1(list(map(lambda x: x.split(" "), m.text.split("\n")))))
        bot.send_message(m.chat.id, res)
        markup = create_actions_markup()
        # if last_message != -1:
        #     bot.edit_message_reply_markup(m.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
        last_message = bot.send_message(m.chat.id, "What do you want to do?", reply_markup=markup)
        if res.split()[0] != "Invalid":
            c_arrays += 1
        array_check = 0


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global c_riddle_solved, c_sure, last_message
    if call.message:
        if call.data == "Start_Riddle":
            if c_riddle_solved and not c_sure:
                markup = types.InlineKeyboardMarkup()
                ans1 = types.InlineKeyboardButton('Yep', callback_data="Start_Riddle")
                markup.add(ans1)
                if last_message != -1:
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
                last_message = bot.send_message(call.message.chat.id, "Just a reminder, because you've already solved this puzzle, new results wouldn't be saved in records, do you still want to continue?", reply_markup=markup)
                c_sure = 1
            else:
                bot.send_message(call.message.chat.id, "Let's begin then")
                filepath = r"Riddle_Photos/Riddle1.jpg"
                photo = open(filepath, 'rb')
                bot.send_photo(call.message.chat.id, photo)
                markup = create_actions_markup()
                if last_message != -1:
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())
                last_message = bot.send_message(call.message.chat.id, "What do you want to do?", reply_markup=markup)

        elif call.data == "Answer_Check":
            global answer_check
            bot.send_message(call.message.chat.id, "Send your guess")
            answer_check = True
            if last_message != -1:
                bot.edit_message_reply_markup(call.message.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())

        elif call.data == "Array_Check":
            global array_check
            bot.send_message(call.message.chat.id, "Send your array, remember, it must contain 6 strings with 3 numbers in each")
            array_check = True
            if last_message != -1:
                bot.edit_message_reply_markup(call.message.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())

        elif call.data == "Stop_Bot":
            bot.send_message(call.message.chat.id, "I'm turning off, if you want to resume my work, just use the '/start' command in the chat, bye!")
            if last_message != -1:
                bot.edit_message_reply_markup(call.message.chat.id, message_id=last_message.id, reply_markup=types.InlineKeyboardMarkup())

    else:
        reply = "That's an inappropriate data "
        if call.message:
            reply += call.data
        bot.send_message(call.message.chat.id, reply)


bot.infinity_polling()
