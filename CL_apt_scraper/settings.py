
BOT_NAME = 'CLScraper'

SPIDER_MODULES = ['CL_apt_scraper.spiders']
NEWSPIDER_MODULE = 'CL_apt_scraper.spiders'

ITEM_PIPELINES = {
    'CL_apt_scraper.pipelines.CLAptScrapePipeline': 300,
}

DOWNLOADER_MIDDLEWARES = { 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None }
COOKIES_ENABLED = 0 
