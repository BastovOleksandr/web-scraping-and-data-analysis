import re
import time

import scrapy
from scrapy import signals
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper_config import CATEGORY, TECHNOLOGIES, SLEEP_TIMER
from dou_scraper.items import VacancyItem


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = [f"https://jobs.dou.ua/vacancies/?category={CATEGORY}"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options)
        self.wait = WebDriverWait(self.driver, SLEEP_TIMER)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(
            VacanciesSpider, cls
        ).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.spider_closed,
            signal=signals.spider_closed
        )
        return spider

    def spider_closed(self, spider):
        self.driver.quit()
        if self.driver.session_id:
            print("Driver is active")
        else:
            print("Driver is not active")
        spider.logger.info("Spider closed: %s", spider.name)

    def parse(self, response, **kwargs):
        experience_urls = response.css(
            "div.b-region-filter ul:first-of-type li a::attr(href)"
        ).getall()
        urls_exp_map = self.get_urls_exp_mapper(experience_urls)
        for url, exp in urls_exp_map.items():
            yield scrapy.Request(
                url=url, callback=self.parse_vacancy, meta={"experience": exp}
            )

    def get_urls_exp_mapper(self, experience_urls):
        url_exp_mapper = {}

        for url in experience_urls:
            experience = url.split("=")[-1]
            self.driver.get(url)
            if self.driver.find_elements(By.CLASS_NAME, "b-inner-page-header"):
                try:
                    while True:
                        button = self.wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "div.more-btn > a")
                            )
                        )
                        button.click()
                        time.sleep(SLEEP_TIMER)
                except TimeoutException:
                    pass
                quotes = self.driver.find_elements(By.CLASS_NAME, "l-vacancy")
                for quote in quotes:
                    url = quote.find_element(
                        By.CLASS_NAME, "vt"
                    ).get_attribute("href")
                    url_exp_mapper[url] = experience

        return url_exp_mapper

    def parse_vacancy(self, response):
        vacancy = VacancyItem()
        vacancy["company_name"] = response.css(".l-n a::text").get()
        vacancy["vacancy_title"] = response.css(".g-h2::text").get()
        vacancy["job_locations"] = self.parse_job_locations(response)
        vacancy["salary"] = self.parse_salary(response)
        description = self.parse_description(response)
        vacancy["technologies"] = self.find_technologies(description)
        vacancy["required_exp"] = response.meta.get("experience")
        yield vacancy

    @staticmethod
    def parse_salary(response):
        salary = response.css(".salary::text").get()
        if salary:
            salary = list(map(int, re.findall(r"\d+", salary)))[-1]
        return salary

    @staticmethod
    def parse_job_locations(response):
        job_location = response.css(".bi-geo-alt-fill::text").get().strip()
        if job_location:
            job_location = [
                re.sub(r"\(.*?\)", "", loc).strip().capitalize()
                for loc in job_location.split(",")
            ]
        return job_location

    @staticmethod
    def parse_description(response):
        return "".join(
            [
                text.strip()
                for text in response.css(".vacancy-section *::text").getall()
                if text.strip()
            ]
        ).replace("\xa0", " ")

    @staticmethod
    def find_technologies(description):
        technologies = []

        for technology in TECHNOLOGIES:
            for option in technology.split(":"):
                pattern = r"\b" + re.escape(option) + r"\b"
                if bool(re.search(pattern, description, re.IGNORECASE)):
                    technologies.append(option)
                    break

        return technologies
