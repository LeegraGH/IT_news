import asyncio

from django.apps import AppConfig

# from src.parsers.parse_news import parse_news


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    # def ready(self):
    #     if not hasattr(self, 'already_started'):
    #         self.already_started = True
    #         # asyncio.create_task(parse_news())
    #         asyncio.run(parse_news())
