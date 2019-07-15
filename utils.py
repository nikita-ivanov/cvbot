from datetime import datetime


def make_link(link, post_header, style):
    """
    Make a formatted link in either HTML or Markdown styles.
    :param link: str, link to a SO post
    :param post_header: str, short post name
    :param style: str, either 'HTML' or 'Markdown'
    :return: str
    """
    if style == 'HTML':
        return '<a href="' + link + '">' + post_header + '</a>'
    elif style == 'Markdown':
        return "[" + post_header + "](" + link + ")"
    else:
        raise ValueError(f'unknown `style` argument "{style}"')


def log_message(logger, update, success=True):
    if success:
        status = 'Success'
    else:
        status = 'Error'
    logger.warning(f"""{status} for request {update.message.text}, 
                        chat id: {update.message.chat_id}, 
                        user id: {update.message.from_user.id}, 
                        user: {update.message.from_user.first_name} {update.message.from_user.last_name}, 
                        username: {update.message.from_user.username}""")


def print_to_console(text, color):
    if color == 'green':
        print(f'{datetime.now()} \033[92m {text} \033[0m')
    elif color == 'red':
        print(f'{datetime.now()} \033[94m {text} \033[0m')
    else:
        raise ValueError(f'unknown `color` argument "{color}"')
