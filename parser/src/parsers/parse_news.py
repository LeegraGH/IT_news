import asyncio
from collections import deque

from parser.src.parsers.habr_parser import habr_parse
from parser.src.parsers.mail_parser import mail_parse


def parse_news():
    habr_parse()
    mail_parse()

    # posted_articles = deque(maxlen=32)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.create_task(habr_parse(posted_articles))
    # loop.create_task(mail_parse(posted_articles))
    #
    # loop.run_forever()

    # await asyncio.gather(
    #     habr_parse(posted_articles),
    #     mail_parse(posted_articles)
    # )


if __name__ == '__main__':
    parse_news()
