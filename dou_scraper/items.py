# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacancyItem(scrapy.Item):
    company_name = scrapy.Field()
    vacancy_title = scrapy.Field()
    job_locations = scrapy.Field()
    salary = scrapy.Field()
    technologies = scrapy.Field()
    required_exp = scrapy.Field()
