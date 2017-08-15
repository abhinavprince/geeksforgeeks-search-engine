import os
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.url
import mimetypes


class FullSpider(CrawlSpider):
    name = 'FullSpider'

    dict_extensions = {
        'document': {'.doc', '.docx', '.pdf', '.ppt','.pwz', '.pptx', '.odt', '.ott', '.rtf', '.txt'},
        'image': {'.jpeg', '.jpg', '.jpe', '.png', '.tif', '.tiff', '.gif', '.webp', '.svg', '.bmp'},
    }

    repo_links = re.compile(
        "")

    if not os.path.exists('Links/Full/responsed'):
        os.makedirs('Links/Full/responsed')

    if not os.path.exists('Links/Full/found'):
        os.makedirs('Links/Full/found')

    content_link_file = open(r'Links/Full/responsed/content_links.txt', 'a+')
    doc_link_file = open(r'Links/Full/responsed/doc_links.txt', 'a+')
    image_link_file = open(r'Links/Full/responsed/image_links.txt', 'a+')
    other_link_file = open(r'Links/Full/responsed/other_links.txt', 'a+')
    repo_link_file = open(r'Links/Full/responsed/repo_links.txt', 'a+')

    name_link_file = open(r'Links/Full/found/name_links.txt', 'a+')
    doc_name_link_file = open(r'Links/Full/found/doc_name_links.txt', 'a+')
    image_name_link_file = open(r'Links/Full/found/image_name_links.txt', 'a+')
    other_name_link_file = open(r'Links/Full/found/other_name_links.txt', 'a+')
    repo_name_link_file = open(r'Links/Full/found/repo_name_links.txt', 'a+')

    start_urls = [
        'http://harrypotter.wikia.com/wiki/Main_Page',
    ]
    rules = (Rule(LinkExtractor(allow='harrypotter.wikia.com',
                                deny=(),
                                canonicalize=True,
                                deny_extensions=(),
                                ),
                  follow=True,
                  # process_request='lets_see',
                  process_links='print_before_requesting',
                  callback='parse_item'
                  ),
             )

    def print_before_requesting(self, links):

        for i in range(len(links)):
            clean_url = w3lib.url.url_query_cleaner(links[i].url)
            links[i].url = clean_url
            (ty, en) = mimetypes.guess_type(clean_url)
            ext2 = ''
            if ty is not None:
                ext2 = mimetypes.guess_extension(type=ty)

            if ext2 in FullSpider.dict_extensions['document']:
                FullSpider.doc_name_link_file.write(clean_url + '\n')
            elif ext2 in FullSpider.dict_extensions['image']:
                FullSpider.image_name_link_file.write(clean_url + '\n')
            elif FullSpider.repo_links.match(clean_url):
                FullSpider.repo_name_link_file.write(clean_url + '\n')
            else:
                FullSpider.name_link_file.write(clean_url + '\n')
            FullSpider.other_name_link_file.write(clean_url + '\n')
        return links

    def lets_see(self, request):
        FullSpider.other_link_file.write(request.url + '\n')
        return request

    def parse_item(self, response):

        # FullSpider.other_link_file.write(response.request.headers.get('Referer', None) + '\n')
        ext = mimetypes.guess_extension(response.headers['content-type'])

        if ext in FullSpider.dict_extensions['document']:
            FullSpider.doc_link_file.write(response.url + '\n')
        elif ext in FullSpider.dict_extensions['image']:
            FullSpider.image_link_file.write(response.url + '\n')
        elif FullSpider.repo_links.match(response.url):
            FullSpider.repo_link_file.write(response.url + '\n')
        else:
            FullSpider.content_link_file.write(response.url + '\n')

        FullSpider.other_link_file.write(response.url + '\n')
        return None
