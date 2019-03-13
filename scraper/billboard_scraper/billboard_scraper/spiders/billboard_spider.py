import scrapy


class QuotesSpider(scrapy.Spider):
    name = "billboard"
    allowed_domains = ['billboard.com']

    def start_requests(self):
        urls = {
            'country': 'https://www.billboard.com/charts/year-end/2018/hot-country-songs',
            'pop': 'https://www.billboard.com/charts/year-end/2018/pop-songs',
            'hiphop': 'https://www.billboard.com/charts/year-end/2018/hot-r-and-and-b-hip-hop-songs',
            'latin': 'https://www.billboard.com/charts/year-end/2018/top-latin-artists',
            'electronic': 'https://www.billboard.com/charts/year-end/2018/hot-dance-electronic--songs',
            'christian': 'https://www.billboard.com/charts/year-end/2018/hot-christian-songs',
            'rock': 'https://www.billboard.com/charts/year-end/2018/hot-rock-songs'
        }
        for genre, url in urls.items():
            yield scrapy.Request(url=url, callback=self.parse, meta={'genre': genre})

    def parse(self, response):
      genre = response.meta['genre']
      for song in response.css('div.ye-chart-item__text'):
        yield {
            'song': song.css('div.ye-chart-item__title::text').get(),
            'artist': song.css('div.ye-chart-item__artist::text').get(),
            'genre': genre
        }
      next_pages = response.css('a.year-link::attr(href)').getall()
      if next_pages:
        for page in next_pages:
          next = response.urljoin(page)
          yield scrapy.Request(next, callback=self.parse, meta={'genre': genre})
      
