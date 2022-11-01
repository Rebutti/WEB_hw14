import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Author, Quote, Tag, Table
import sqlite3


def parse_data():
    data = []
    url = 'https://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.select('div[class=quote]')

    for content in contents:
        tags = []
        about_author_link = url[:-1]+content.find('a')['href']
        quote = content.find('span', attrs={'class': 'text'}).text.replace('“', '').replace('”', '')
        author = content.find('small', attrs={'class': 'author'}).text
        tags.append(content.find('div', attrs={'class': 'tags'}).find('meta')['content'].split(','))
        data.append(
            {
                'author': author,
                'quote': quote,
                'about_author_link': about_author_link,
                'tags': tags[0],



            }
        )
    # print(data)
    return data


if __name__ == "__main__":
    data = parse_data()
    engine = create_engine("sqlite:///quotes.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # print(type(data))
    quote_tag_data1 = []
    for el in data:
        tags = []
        author = Author(name=el.get('author'))
        a = session.query(Author).filter(Author.name == author.name)
        if a.all() == []:
            session.add(author)

        # for author1 in session.query(Author).filter(Author.name == author.name):
        #     print(type(author1))
        for author in session.query(Author).filter(Author.name == author.name):
            author_id = author.id
            quote = Quote(name=el.get('quote'), author_id=author_id)
            a = session.query(Quote).filter(Quote.name == quote.name)
            if a.all() == []:
                session.add(quote)
            break
        for tag in el.get('tags'):
            author_tag = Tag(name=tag)
            a = session.query(Tag).filter(Tag.name == author_tag.name)
            if a.all() == []:
                session.add(author_tag)
                tags.append(author_tag.name)
        # for index, elem in enumerate(data):
            # quote = Quote(name=el.get('quote'), author_id=session.query(Author)
            #             .filter(Author.name == el.get('author')).one().id)
        # quote_tag = Table(name=el.get('quote'), author_id=author_id)
        # break
        # print(tags)
        a = session.query(Quote).filter(Quote.name == quote.name)
        quote_id = a.all()[0].id
        # print(quote_id)
        for tag in tags:
            a = session.query(Tag).filter(Tag.name == tag)
            tag_id = a.all()[0].id
            quote_tag_data = (quote_id, tag_id)
            quote_tag_data1.append(quote_tag_data)
    session.commit()
    session.close()
    with sqlite3.connect('quotes.db') as con:
                cur = con.cursor()
                sql_to_quote_tag = """INSERT INTO quote_tag (quote, tag)
                                    VALUES (?, ?);"""
                cur.executemany(sql_to_quote_tag, quote_tag_data1)
    