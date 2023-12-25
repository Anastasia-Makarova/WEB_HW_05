from datetime import date, timedelta
from pathlib import Path
import platform
import sys

import aiohttp
import asyncio

# https://api.privatbank.ua/p24api/exchange_rates?json&date=24.12.2023



def urls_list(period: int) -> list:
    url_dateless = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    today_url = f'{url_dateless}{date.today().day}.{date.today().month}.{date.today().year}'
    urls_list = [today_url]

    for i in range(1, period):
        day = date.today() - timedelta(i)
        urls_list.append(f'{url_dateless}{day.day}.{day.month}.{day.year}')
    
    return urls_list


async def main(urls: list):

    async with aiohttp.ClientSession() as session:
        results = []  
        for url in urls:
            async with session.get(url) as response:
                result = await response.json()
                # results.append(type(result['exchangeRate']))
                # for curr in result['exchangeRate']:
                    
                exchange_USD, *_ = filter(lambda curr: curr['currency'] == 'USD', result['exchangeRate'])
                exchange_EUR, *_ = filter(lambda curr: curr['currency'] == 'EUR', result['exchangeRate'])
                # results.append(f'{date.today()}: USD: buy: {exchange_USD["purchaseRateNB"]}, sale: {exchange_USD["saleRateNB"]}, EURO: buy: {exchange_EUR["purchaseRateNB"]}, sale: {exchange_EUR["saleRateNB"]}')
                currency_for_date = {url[-10 :-1]:{'USD:':{'buy:': exchange_USD["purchaseRateNB"], 'sale:':exchange_USD["saleRateNB"]},'EURO:':{'buy:': exchange_EUR["purchaseRateNB"], 'sale:':exchange_EUR["saleRateNB"]} }}
                results.append(currency_for_date)

        return results


if __name__ == "__main__":
    try:
        period = int(sys.argv[1])
        if period <= 10:
            if platform.system() == 'Windows':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            r = asyncio.run(main(urls_list(period)))
            for line in r:
                print(line)
        else:
            raise ValueError ('Only up to 10 days possible')
    except IndexError:
        print ('Please, give the number of days (10<=) as an argument')
    except ValueError:
        print('Only integers 10<= are allowed as an argument')

