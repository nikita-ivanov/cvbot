import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(filename = 'CVBot.log', format='%(asctime)s %(message)s')
token = "665231913:AAEDjX_h-eQ53hgX440smV3ryy-MQYXBruI"
logging.warning('Bot started')

#define some helper funstions
def makeLink(link, post, style = 'HTML'):
    if style == 'HTML':
        return '<a href="' + link +  '">' + post + '</a>'
    else:
        return "[" + post + "](" + link + ")"

def getTopQuestions(topic):
    """
    Scrap top questions for the specific topic.

    topic: a string, 'math', 'so', 'stat' or 'quant'.
    """

    websites = dict(math = 'https://math.stackexchange.com/?tab=hot', 
                    stat = 'https://stats.stackexchange.com/?tab=hot',
                    so = 'https://stackoverflow.com/?tab=hot',
                    quant = 'https://quant.stackexchange.com/?tab=hot')

    url = websites.get(topic)
    votes = []
    links = []
    post_names = []
    page = BeautifulSoup(urlopen(url).read(), 'html.parser')
    posts = page.find_all('div', {'class': 'question-summary narrow'})
    for post in posts:
        votes.append(int(post.find('div', {'class': 'mini-counts'}).text)) #number of votes
        post_names.append(post.find('div', {'class': 'summary'}).find("h3").text)
        links.append(url[:-9] + post.find('a', {'class': "question-hyperlink"}).get('href'))

    return (votes, links, post_names)

def sendMessage(link, post, update, bot):
    try:
        text = makeLink(link, post, style = 'HTML')
        bot.send_message(chat_id = update.message.chat_id, text = text, parse_mode = 'HTML', 
                        disable_web_page_preview = False)
        print(datetime.now(), '\033[92m Success for request {} \033[0m'.format(update.message.text))
        logging.warning('Succes for request {}, chat id: {}, user id: {}, user: {} {}, username: {}'.format(
                update.message.text, update.message.chat_id, update.message.from_user.id,
                update.message.from_user.first_name, update.message.from_user.last_name,
                update.message.from_user.username))

    except telegram.error.BadRequest as e:
        text = makeLink(link, post, style = 'Markdown')
        bot.send_message(chat_id = update.message.chat_id, text = text, parse_mode = 'Markdown', 
                        disable_web_page_preview = False)
        print(datetime.now(), '\033[92m Success for request {} (using Markdown mode) \033[0m'.format(update.message.text))
        logging.warning('Succes for request {} (using Markdown), chat id: {}, user id: {}, user: {} {}, username: {}'.format(
                update.message.text, update.message.chat_id, update.message.from_user.id,
                update.message.from_user.first_name, update.message.from_user.last_name,
                update.message.from_user.username))

    except Exception as e:
        print(datetime.now(), '\033[93m There was the following exception: \n{} \033[0m '.format(e))
        logging.exception('Error for request {}, chat id: {}, user id: {}, user: {} {}, username: {}'.format(
                update.message.text, update.message.chat_id, update.message.from_user.id,
                update.message.from_user.first_name, update.message.from_user.last_name,
                update.message.from_user.username))

def getSortedLinks(votes, links, posts):
    links_sorted = [x for _,x in sorted(zip(votes,links), reverse = True, key = lambda pair: pair[0])]
    posts_sorted = [x for _,x in sorted(zip(votes,posts), reverse = True, key = lambda pair: pair[0])]
    
    return links_sorted, posts_sorted

def start(bot, update):

    text = 'Type one of the following: \n/math for MathStackExchange \n/stat for CrossValidated \n/quant for QuantitativeFinance \n/so for StackOverFlow'
    bot.send_message(chat_id = update.message.chat_id, text = text,
                    reply_markup = ReplyKeyboardMarkup([['/math', '/stat'], ['/quant', '/so']], one_time_keyboard = True))
    printToConsole('Success for request {}\n'.format(update.message.text))

def so(bot, update):
    votes, links, posts = getTopQuestions('so')
    links_sorted, posts_sorted = getSortedLinks(votes, links, posts)

    for link, post in zip(links_sorted[:10], posts_sorted[:10]):
        sendMessage(link, post, update, bot)

def stat(bot, update):
    votes, links, posts = getTopQuestions('stat')
    links_sorted, posts_sorted = getSortedLinks(votes, links, posts)

    for link, post in zip(links_sorted[:10], posts_sorted[:10]):
        sendMessage(link, post, update, bot)

def math(bot, update):
    votes, links, posts = getTopQuestions('math')
    links_sorted, posts_sorted = getSortedLinks(votes, links, posts)

    for link, post in zip(links_sorted[:10], posts_sorted[:10]):
        sendMessage(link, post, update, bot)

def quant(bot, update):
    votes, links, posts = getTopQuestions('quant')
    links_sorted, posts_sorted = getSortedLinks(votes, links, posts)

    for link, post in zip(links_sorted[:10], posts_sorted[:10]):
        sendMessage(link, post, update, bot)

updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('so', so))
dispatcher.add_handler(CommandHandler('stat', stat))
dispatcher.add_handler(CommandHandler('math', math))
dispatcher.add_handler(CommandHandler('quant', quant))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
print('='*50)
print('Poll started. You can use your bot :)')
input('Press enter to stop polling \n')
updater.stop()
logging.warning('Bot stopped.')
print(datetime.now(), '\033[94m The bot has been stoped. \033[0m')