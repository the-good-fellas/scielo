from scielo.items import ScieloItem
from scrapy import Selector
import logging
import scrapy

logger = logging.getLogger('scielo')


class ScieloSpider(scrapy.Spider):
  name = "scielo"

  def start_requests(self):
    parts = 3909
    urls = [
      'https://search.scielo.org/?fb=&q=*&lang=pt&count=50&from=1&output=site&sort=&format=summary&page=1&where=&filter_boolean_operator%5Bsubject_area%5D%5B%5D=OR&filter%5Bla%5D%5B%5D=pt&filter%5Bsubject_area%5D%5B%5D=Health+Sciences&filter%5Bsubject_area%5D%5B%5D=Biological+Sciences']
    for i in range(2, parts):
      from_ = (50 * i + 1) - 50
      urls.append(
        f'https://search.scielo.org/?fb=&q=*&lang=pt&count=50&from={from_}&output=site&sort=&format=summary&page={i}&where=&filter_boolean_operator%5Bsubject_area%5D%5B%5D=OR&filter%5Bla%5D%5B%5D=pt&filter%5Bsubject_area%5D%5B%5D=Health+Sciences&filter%5Bsubject_area%5D%5B%5D=Biological+Sciences',
      )

    logger.info(f'urls to scrap: {len(urls)}')

    for url in urls:
      logger.info(f'scrapping {url}')
      yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

  def parse(self, response):
    page_selector = Selector(text=response.body)
    ids_art = page_selector.xpath(
      "//div[@class='results']/div[@class='item']/@id"
    ).getall()

    for id_art in ids_art:
      _id_art = id_art[0:-4]
      url = f'http://www.scielo.br/scielo.php?script=sci_arttext&pid={_id_art}&lng=pt&tlng=pt'
      yield scrapy.Request(url=url, callback=self.parse_inner_page, meta={"url": url, "id": _id_art})

  def parse_inner_page(self, response):
    page_selector = Selector(text=response.body)
    content = page_selector.xpath("//article/div[@data-anchor='Text']/p/text()").getall()

    if content is None or len(content) == 0:
      content = []
      for i in range(1, 5):
        _cont = page_selector.xpath(f"//article/div[{i}]/p/text()").getall()
        size = 0 if _cont is None else len(_cont)
        if size > len(content):
          content = _cont

    if len(content) == 0:
      logger.warning(f'unable to extract content from {response.meta["url"]}')
      return None
    else:
      logger.info(f'content size: {len(content)} from {response.meta["url"]}')

    return ScieloItem(content=content, id_art=response.meta['id'])
