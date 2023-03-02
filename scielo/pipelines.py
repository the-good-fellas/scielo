# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import traceback
import logging
import os
import re

logger = logging.getLogger('scielo')

ARTICLES_FOLDER = 'articles'


class ScieloPipeline:

  def process_item(self, item, spider):
    try:
      os.makedirs('articles', exist_ok=True)

      joint_content = ' '.join(item['content'])
      joint_content = re.sub(r'[\n]+', '', joint_content)
      joint_content = joint_content.strip()

      id_art = item['id_art']
      with open(f'{ARTICLES_FOLDER}/{id_art}.txt', 'w') as article_file:
        article_file.write(joint_content)
    except Exception as e:
      traceback.print_exc()
      logger.error(e)

    return item
