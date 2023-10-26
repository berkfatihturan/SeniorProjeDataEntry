from src.WebScraper import WebScraper

url = "https://www.arabam.com/ikinci-el?take=50"
CarScraper = WebScraper(url=url)
CarScraper.startScrapping()
