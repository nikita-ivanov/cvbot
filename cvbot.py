import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
from collections import OrderedDict
import utils


logging.basicConfig(filename='cvbot.log', format='%(asctime)s %(message)s')
token = "665231913:AAEDjX_h-eQ53hgX440smV3ryy-MQYXBruI"
logging.warning('Bot started.')

topic_url_mapping = OrderedDict([('math', 'https://math.stackexchange.com/?tab=hot'),
                                 ('stat', 'https://stats.stackexchange.com/?tab=hot'),
                                 ('so', 'https://stackoverflow.com/?tab=hot'),
                                 ('quant', 'https://quant.stackexchange.com/?tab=hot')])


def scrap_top_posts(topic, n_posts=10):
    """
    Scrap top questions for `topic`.
    :param topic: str, one of 'math', 'stat', 'so', 'quant'
    :param n_posts: int, number of posts to return, default 10
    :return: tuple, (n_votes, links, post_names)
    """

    url = topic_url_mapping[topic]
    page = BeautifulSoup(urlopen(url).read(), 'html.parser')
    posts = page.find_all('div', {'class': 'question-summary narrow'})

    votes = [int(post.find('div', {'class': 'mini-counts'}).text) for post in posts]
    links = [url[:-9] + post.find('a', {'class': "question-hyperlink"}).get('href') for post in posts]
    post_names = [post.find('div', {'class': 'summary'}).find("h3").text for post in posts]

    return sort_by_votes(votes, links, post_names, n_posts)


def send_message(link, post, update, bot):
    try:
        text = utils.make_link(link, post, style='HTML')
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode='HTML',
                         disable_web_page_preview=False)

        utils.print_to_console(f'Success for request {update.message.text}', color='green')
        utils.log_message(logging, update)

    except telegram.error.BadRequest:  # try in Markdown mode
        text = utils.make_link(link, post, style='Markdown')
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode='Markdown',
                         disable_web_page_preview=False)

        utils.print_to_console(f'Success for request {update.message.text} (using Markdown mode)', color='green')
        utils.log_message(logging, update)

    except Exception as e:
        utils.print_to_console(f'There was the following exception for request {update.message.text}, skipping... \n{e}', color='blue')
        utils.log_message(logging, update, success=False)
        pass


def sort_by_votes(votes, links, post_names, n_posts):
    """
    Sort posts by a number of votes
    :param votes: list of integers, number of votes for a post
    :param links: list of strings, links to scraped posts
    :param post_names: list of strings, post titles
    :param n_posts: int, number of posts to return
    :return: tuple, (links, posts)
    """
    links_sorted = [link for _, link in sorted(zip(votes, links), reverse=True, key=lambda pair: pair[0])]
    posts_sorted = [post for _, post in sorted(zip(votes, post_names), reverse=True, key=lambda pair: pair[0])]
    
    return links_sorted[:n_posts], posts_sorted[:n_posts]


def start(bot, update):

    text = """
Type one of the following: 
/math for MathStackExchange 
/stat for CrossValidated 
/quant for QuantitativeFinance 
/so for StackOverFlow"""

    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     reply_markup=ReplyKeyboardMarkup([['/math', '/stat'], ['/quant', '/so']], one_time_keyboard=True))

    utils.print_to_console('Success for request {}\n'.format(update.message.text), color='green')


# define handlers
def so(bot, update):
    links, posts = scrap_top_posts('so')

    for link, post in zip(links, posts):
        send_message(link, post, update, bot)


def stat(bot, update):
    links, posts = scrap_top_posts('stat')

    for link, post in zip(links, posts):
        send_message(link, post, update, bot)


def math(bot, update):
    links, posts = scrap_top_posts('math')

    for link, post in zip(links, posts):
        send_message(link, post, update, bot)


def quant(bot, update):
    links, posts = scrap_top_posts('quant')

    for link, post in zip(links, posts):
        send_message(link, post, update, bot)


# register handlers
updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('so', so))
dispatcher.add_handler(CommandHandler('stat', stat))
dispatcher.add_handler(CommandHandler('math', math))
dispatcher.add_handler(CommandHandler('quant', quant))
dispatcher.add_handler(CommandHandler('start', start))


if __name__ == '__main__':
    updater.start_polling()
    print('='*50)
    print('Poll started. You can use your bot :)')
    input('Press enter to stop polling \n')
    utils.print_to_console('Stopping...', color='green')
    updater.stop()
    logging.warning('Bot being stopped by a user.')
    utils.print_to_console('The bot has been stopped.', color='blue')
