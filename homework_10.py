import telebot

bot = telebot.TeleBot(" ", parse_mode=None)


# Commands :

# question - ask your question
# list - all questions

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello buddy')


def write_question(message):
    file = 'Questions.txt'
    with open (file, 'a', encoding = 'utf-8') as data:
        data.write(f'user_id: {message.from_user.id} username: {message.from_user.username} question: {message.text}\n')
    bot.send_message(message.chat.id, 'Your question was submited, retype "question", if you want to ask another question')
   

def answer_question(message):
    bot.send_message(message.chat.id, f"Your choice is stroke number: {message.text}")
    file = 'Questions.txt'
    with open (file, 'r', encoding = 'utf-8') as data:
        text = data.readlines()
        i = int(message.text) - 1
        q = text[i]
        id_for_answer = q.split()[1]
        question = " ".join(q.split()[5:])
        bot.send_message(message.chat.id, 'Question:')
        bot.send_message(message.chat.id, q)
    bot.send_message(message.chat.id, 'Enter your answer:')
    bot.register_next_step_handler(message, post_answer, id_for_answer, question)

def post_answer(message, id_for_answer, question):
    bot.send_message(id_for_answer, 'Here is an answer for your question: ')
    bot.send_message(id_for_answer, f'question: {question}')
    bot.send_message(id_for_answer, f'answer: {message.text}')


@bot.message_handler(content_types=['text'])
def start(message):
    if 'question' in message.text:
        bot.reply_to(message, 'Enter your question:')
        bot.register_next_step_handler(message, write_question)
    elif 'list' in message.text:
        bot.reply_to(message, 'Here is list of questions')
        file = 'Questions.txt'
        with open (file, 'r', encoding = 'utf-8') as data:
            li = data.read()
        bot.send_message(message.chat.id, li)
        bot.send_message(message.chat.id, "Enter number of stroke to answer question")
        bot.register_next_step_handler(message, answer_question)
    
bot.infinity_polling()
