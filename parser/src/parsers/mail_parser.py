import requests
from bs4 import BeautifulSoup

from parser.src.services.add_article import add_article


def mail_parse():
    try:
        site_url = 'https://hi-tech.mail.ru/category/technology/'
        html = requests.get(site_url)

        soup = BeautifulSoup(html.text, 'html.parser')
        articles = soup.find_all('div',
                                 {'data-qa': 'ArticleThumb'})
    except:
        print("Error: Could not parse Hi-Tech Mail!")
        return

    for article in articles:
        try:
            article_url = 'https://hi-tech.mail.ru' + article.find(
                lambda tag: tag.name == 'div' and tag.get('data-qa') in ['Text', 'Title']).find("a").get("href")

            title = article.find(
                lambda tag: tag.name == 'div' and tag.get('data-qa') in ['Text', 'Title']).text.replace(u'\xa0',
                                                                                                        u' ')

            image = ""
            try:
                image = article.find("picture", {'data-qa': 'Picture'}).find('img').get("src")
            except:
                pass

            article_data = {
                "category": "hi-tech Mail.ru",
                "title": title,
                "image": image,
                "text": ""
            }

            article_html = requests.get(article_url)

            article_soup = BeautifulSoup(article_html.text, 'html.parser')

            article_text = article_soup.find('main', {'data-qa': 'ArticleLayout'}).find_all('div', {
                'article-item-type': 'html'})

            for block in article_text:
                text_array = block.find_all('p')

                for part in text_array:
                    article_data["text"] += part.get_text().replace(u'\xa0', u' ') + " "

            add_article(article_data)
            print(article_data)

        except:
            continue


if __name__ == '__main__':
    mail_parse()
