import urllib
from itertools import cycle

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache_method = RedisLRU(client, max_size=100)

@cache_method
def is_supported(url: str) -> bool:
    """Check whether the provided URL can be accessed"""
    response = urllib.request.urlopen(url).getcode()
    if response == 200:
            print(f"The URL: {url} is valid ")
            return True
    return False


if __name__ == '__main__':
    urls = [ "https://www.zenrows.com/knowledge/scrape-from-a-list-of-urls",
             "https://www.freecodecamp.org/news/introduction-to-mongoose-for-mongodb-d2a7aa593c57/",
             "https://macdown.uranusjr.com/",
             "https://stackoverflow.com/questions/70961915/error-while-installing-pytq5-with-pip-preparing-metadata-pyproject-toml-did-n"
    ]
    urls_cycle = cycle(urls)

    def next_url():
        return next(urls_cycle)

    while True:
        input_url = next_url()
        is_supported = is_supported(input_url)
