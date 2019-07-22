# cvbot
## This is a python telegram bot that scraps top popular questions from StackOverFlow.


_Requirements_
---
`python-telegram-bot`, `bs4`.


_Usage_
---
Clone a repository to a location of your preference via `git clone https://github.com/nikita-ivanov/cvbot.git`,
open a terminal and run `python3 cvbot.py` in a `.\cvbot` folder. In your telegram
app, use search to find a bot called `@CrossValidatedBot` and start a chat. 


_Functilonality_
---
There are four requests that the bot understands: `\so`, `\stat`, `\math` and `\quant`
that correspond to [Stack Overflow](https://stackoverflow.com), 
[Cross Valdiated](https://stats.stackexchange.com), 
[Mathematics](https://math.stackexchange.com) and 
[Quantitative Finance](https://quant.stackexchange.com)
topics from a [Stack Exchange](https://stackexchange.com) website. For each of them
the bot will go to a respective website and scrap top (ten by default) hot questions, sort them
based on the number of votes and send to you in your telegram chat. 