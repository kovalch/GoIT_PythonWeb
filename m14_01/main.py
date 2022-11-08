import requests
from bs4 import BeautifulSoup
from src.db import session
from src.models import Tag, Author, Quote

url_base = 'https://quotes.toscrape.com'

def scrape_data(url_base):
    """Get quotes and authors information"""
    store_ = []

    #check the response status
    response_base = requests.get(f"{url_base}/")

    if response_base.status_code != 200:
        raise "The page is not available, please check"

    for page in range(1,10):
        response = requests.get(f"{url_base}/page/{page}/")
        soup = BeautifulSoup(response.text, 'lxml')

        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        authors_href = soup.find_all('div', class_='quote')

        for i in range(0, len(quotes)):
            # changing the quote text style
            quote = quotes[i].text.replace("“", "").replace("”", "").replace("\r", "").replace("\n", "")
            author = authors[i].text

            list_tag = []
            quote_tags = tags[i].find_all('a', class_='tag')
            for quote_tag in quote_tags:
                list_tag.append(quote_tag.text)

            for a in authors_href[i].find_all('a'):
                if a.text == '(about)':
                    href = f"{url_base}{a['href']}"

            store_.append({"quote": quote,
                           "author": author,
                           "tag": list_tag,
                           "href": href})
    return store_

def add_data_db(el):
    """Add scrape quotes and authors to DB"""

    if not quote_exists_db(el.get('quote')):
        author_from_db = session.query(Author).filter_by(name_author=el.get('author')).first()
        # check if author is already existing
        if author_from_db:
            author_id = author_from_db.id
        else:
            author = Author(name_author=el.get('author'), href_author=el.get('href'))
            session.add(author)
            session.commit()
            author_id = author.id

        quote = Quote(quote_phrase=el.get('quote'), author_id=author_id)
        session.add(quote)

        tag_for_quote = []
        for el_tag in el.get('tag'):
            tag_from_db = session.query(Tag).filter_by(name_tag=el_tag).first()
            if tag_from_db:
                tag_for_quote.append(tag_from_db)
            else:
                tag = Tag(name_tag=el_tag)
                tag_for_quote.append(tag)
                session.add(tag)
        quote.tags = tag_for_quote

        # write to db
        session.commit()


# Example of data usage
def quote_exists_db(quote_):
    quote_db = session.query(Quote).filter_by(quote_phrase=quote_).first()
    if quote_db:
        return True

    return False

def get_quotes(author_id_=None, tag_=None):
    if author_id_:
        quotes = session.query(Quote).filter(Author.id == author_id_).all()
    if tag_:
        quotes = session.query(Quote).join(Quote.tags).filter(Tag.name_tag == tag_).all()
    return quotes


if __name__ == '__main__':
    store = scrape_data(url_base)

    for el in store:
        add_data_db(el)

    # get quote phrase by tag
    for q in get_quotes(tag_='love'):
        #print(q.quote_phrase)
        pass

    # get all quote phrase for given author
    for q in get_quotes(author_id_=6):
        print(q.quote_phrase)

    session.close()