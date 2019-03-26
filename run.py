import sys
sys.path.insert(0, ".")

import logging
logging.getLogger().setLevel(logging.INFO)

from slackbot.bot import Bot

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('start slackbot')
    main()
