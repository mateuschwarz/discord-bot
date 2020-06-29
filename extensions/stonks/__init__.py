
import os
from os.path import realpath, dirname
import json
from datetime import datetime as dt
import requests

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

ccon = lambda : os.system('cls||clear')

class Scrapper:

    """ Wrapper object """

    class Base:

        """
        Classe interna base com variáveis
        e métodos de uso geral
        """

        title = ''
        ticker = ''
        ticker_lst = []
        data_frame = pd.DataFrame()
        date_created = dt.now()
        date_updated = dt.now()

        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/81.0.4044.41 Safari/537.36'}
        DF_COLUMNS = {
            'Company': np.dtype('object'),
            'Ticker': np.dtype('object'),
            'Weight': np.dtype('float'),
            'Price': np.dtype('float'),
            'Change': np.dtype('float'),
            'Change %': np.dtype('float')}
        EMPTY_JSON_RESPONSE = {
            "symbol":np.nan,
            "companyName":np.nan,
            "primaryExchange":np.nan,
            "calculationPrice":np.nan,
            "open":np.nan,
            "openTime":np.nan,
            "openSource":np.nan,
            "close":np.nan,
            "closeTime":np.nan,
            "closeSource":np.nan,
            "high":np.nan,
            "highTime":np.nan,
            "highSource":np.nan,
            "low":np.nan,
            "lowTime":np.nan,
            "lowSource":np.nan,
            "latestPrice":np.nan,
            "latestSource":np.nan,
            "latestTime":np.nan,
            "latestUpdate":np.nan,
            "latestVolume":np.nan,
            "iexRealtimePrice":np.nan,
            "iexRealtimeSize":np.nan,
            "iexLastUpdated":np.nan,
            "delayedPrice":np.nan,
            "delayedPriceTime":np.nan,
            "oddLotDelayedPrice":np.nan,
            "oddLotDelayedPriceTime":np.nan,
            "extendedPrice":np.nan,
            "extendedChange":np.nan,
            "extendedChangePercent":np.nan,
            "extendedPriceTime":np.nan,
            "previousClose":np.nan,
            "previousVolume":np.nan,
            "change":np.nan,
            "changePercent":np.nan,
            "volume":np.nan,
            "iexMarketPercent":np.nan,
            "iexVolume":np.nan,
            "avgTotalVolume":np.nan,
            "iexBidPrice":np.nan,
            "iexBidSize":np.nan,
            "iexAskPrice":np.nan,
            "iexAskSize":np.nan,
            "iexOpen":np.nan,
            "iexOpenTime":np.nan,
            "iexClose":np.nan,
            "iexCloseTime":np.nan,
            "marketCap":np.nan,
            "peRatio":np.nan,
            "week52High":np.nan,
            "week52Low":np.nan,
            "ytdChange":np.nan,
            "lastTradeTime":np.nan,
            "isUSMarketOpen":np.nan}
        API_KEY = \
            'pk_450082744a20416ba83aaee6b70be0a1'

        limit = lambda self, x, y: x[:y+1] + '...' if len(x) > y else x

        def sample(self, size=5):
            string = '\n' + self.ticker + ' Sample:\n' + \
                self.data_frame.head(size).to_string() + '\n...'
            return string    


        def api_request(self, ticker, base, function, querystr):
            url = '/'.join([base, ticker, function])
            response = requests.request('GET', url, headers=self.HEADERS, params=querystr)
            return response.text


        def tops_flops(self, string=False):
            table = self.data_frame
            table = table.sort_values('Change %', ascending=False)
            tops = table.iloc[:10, [0, 1, 3, 4, 5]]
            flops = table.iloc[-10:,[0, 1, 3, 4, 5]]
            
            if string:
                str_tops = tops.to_string(index=False, justify='left')
                str_flops = flops.to_string(index=False, justify='left')
                title = self.ticker.split(' ')[0]
                string = "\n{} Tops and Flops\n\nTops:\n{}\n\nFlops:\n{}\n" \
                    .format(title, str_tops, str_flops)
                return string
            else:
                return [tops, flops]   


        def get_quotes(self, tickers):
            base = 'https://cloud.iexapis.com/stable/stock'
            querystr = { 'token' : self.API_KEY }
            function = 'quote'
	
            if not isinstance(tickers, list):
                try:
                    data = self.api_request(tickers, base, function, querystr)
                    _js = json.loads(data)
                    yield _js
                except:
                    yield self.EMPTY_JSON_RESPONSE
            elif isinstance(tickers, list):
                for ticker in tickers:
                    try:
                        data = self.api_request(ticker, base, function, querystr)
                        _js = json.loads(data)
                    except:
                        print('Ticker not found')
                        _js = self.EMPTY_JSON_RESPONSE
                    yield _js
            else:
                print('Not valid data')


        """ Magic! """
        
        def __add__(self, other):
            if all([isinstance(x, Scrapper.Base) for x in [self, other]]):
                try:
                    result = pd.concat(
                        [self.data_frame, other.data_frame],
                        sort=False
                    )
                except:
                    print('Not valid types')
                    result = None

            return result

        def __len__(self):
            return self.data_frame.size

        def __str__(self):
            return self.title 

        def __repr__(self):
            if len(self.ticker_lst) > 5:
                ticker_lst_str = ", ".join(self.ticker_lst[:5]) + "..."
            else:
                ticker_lst_str = ", ".join(self.ticker_lst[:5])
            info = {
                'Name': self.title,
                'Ticker': self.ticker,
                'Ticker List': ticker_lst_str,
                'Ticker List Count': str(len(self.ticker_lst)),
                'Size': str(self.data_frame.size),
                'Shape': "x".join(map(str, self.data_frame.shape)),
                'Date/Time created': str(self.date_created)[:16],
                'Date/Time last updated': str(self.date_updated)[:16]
            }
            string = "\nObject info:\n" + \
                "\n".join([str(k + ': ' + v) for k, v in info.items()]) + \
                "\n"
            return string


    class IBOV(Base):

        """
        Cria um objeto que contem um panda data frame
        com a composicao da IBOVESPA retirado
        direto do site da B3
        """

        def __init__(self):
            self.ticker = 'IBOV'
            self.title = 'IBOV Composition Dataframe'

            # URL da própria B3 com os dados
            url='http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBOV&amp;idioma=pt-br'

            # Request da página e criação de objeto soup
            page = requests.get(url, headers=self.HEADERS)
            page_soup = soup(page.text, 'html.parser')

            # Atualizando data de update
            self.date_updated = dt.now()

            # Procurando e criando colunas no dataframe
            index = page_soup.find_all('th', {'scope':'col'})
            index_titles = [index[i].a.text for i, _ in enumerate(index)]
            for x in index_titles:
                self.data_frame[x] = ''

            # Encontrando a primeira linha e iterando para as demais colunas
            column = page_soup.find_all('tr', {'class':['rgRow', 'rgAltRow']})

            for c in range(0, len(column)):
                row = column[c].find_all('span')
                self.data_frame.loc[c] = [row[r].text for r, _ in enumerate(row)]

            # Transformando o peso de cada ação em um float
            fix_numb = lambda x : round(float(x.replace(',', '.')), 3)
            self.data_frame.iloc[:,4] = self.data_frame.iloc[:,4].apply(fix_numb)

            # Organizando os valores pelo seu peso na composição
            self.data_frame.sort_values('Part. (%)', ascending=False, inplace=True)

            # Salvando apenas as colunas relevantes e resetando index
            self.data_frame = self.data_frame.iloc[:,[1, 0, 4]]
            self.data_frame.reset_index(drop=True, inplace=True)
            
            # Renomeando nome das colunas
            self.data_frame.columns = ['Company', 'Ticker', 'Weight']

            # Atualizando ticker list
            self.ticker_lst = [x for x in self.data_frame.Ticker]


    class SPX(Base):

        """
        Cria um objeto que contem um panda data frame
        com a composicao do S&P 500
        """

        def __init__(self):
            self.ticker = 'SPX'
            self.title = 'SPX Composition Dataframe'

            # URL com os dados necessários
            url='https://www.slickcharts.com/sp500'

            # Request e soup
            page = requests.get(url, headers=self.HEADERS)
            page_soup = soup(page.text, 'html.parser')

            # Atualizando data de update
            self.date_updated = dt.now()

            # Criando data frame
            index_titles = ['#', 'Company', 'Ticker',
                            'Weight', 'Price', 'Change',
                            'Change %']
            for x in index_titles:
                self.data_frame[x] = ''

            # Encontrando e iterando por cada linha e coluna
            body = page_soup.find('tbody')
            column = body.find_all('tr')
            for c in range(0, len(column)):
                row = column[c].find_all('td')
                self.data_frame.loc[c] = [row[r].text for r, _ in enumerate(row)]

            # Retirando parenteses dos valores negativos 
            strip = lambda x : x.strip('()')
            self.data_frame.iloc[:,6] = self.data_frame.iloc[:,6].apply(strip)

            # Limitando numero maximo de caracteres do nome da companhia
            self.data_frame.iloc[:,1] = self.data_frame.iloc[:,1].apply(self.limit, y=8)

            # Salvando apenas as colunas relevantes
            self.data_frame = self.data_frame.iloc[:,1:]

            # Setando os data types corretos
            # self.data_frame.astype(self.DTYPES)

            # Atualizando ticker list
            self.ticker_lst = [x for x in self.data_frame.Ticker]

    
    class WatchList(Base):

        """
        Cria um objeto que contem um dataframe
        a partir da lista de tickers passada como argument
        """

        def __init__(self, tickers):

            # Informações iniciais
            self.title = 'Watch List'
            self.ticker = ''
            self.ticker_lst = tickers

            # Inserindo títulos
            for title in self.DF_COLUMNS.keys():
                self.data_frame[title] = ''

            # Colocando lista de tickers no dataframe
            self.data_frame['Ticker'] = self.ticker_lst

            # Pegando cotações e nome da companhia
            for row, quote in enumerate(self.get_quotes(self.ticker_lst)):
                if isinstance(quote['companyName'], str):
                    self.data_frame.loc[row][0] = self.limit(quote['companyName'], 8)
                else:
                    self.data_frame.loc[row][0] = ''

                _quote = [quote['latestPrice'], quote['change'], quote['changePercent']]
                self.data_frame.loc[row][3:6] = _quote

            format = lambda x : float(x) * 100
            self.data_frame['Change %'] = self.data_frame['Change %'].apply(format)

class Stonks(commands.Cog):

    def __init__(self, client):

        self.client = client

        self.CWD = realpath(dirname(dirname(dirname(__file__))))
        
        self.STONKS_PATH = os.path.join(self.CWD, "data/stonks.json")

        with open(self.STONKS_PATH) as f:
            self.cfg = json.load(f)

        self.WLIST = self.cfg['Watch List']
        self.Scrapper = Scrapper

    @commands.command()
    @has_permissions(administrator=True)
    async def watchlist(self, ctx, cmd=None, args=None):

        """
        watchlist commands and configurations 
        [cmd]:
        add: adds [args] to watchlist
        remove: remove [args] from watchlist
        quotes: returns todays quotes
        None: returns watchlist tickers
        """

        self.console_print(ctx)
        await ctx.message.delete()

        # !watchlist add {TICKER}
        if cmd == 'add':

            self.WLIST.append(args)
            await ctx.send(f'```diff\n+ {args} added to watchlist\n```')
            with open(self.STONKS_PATH, 'w') as f:
                json.dump(self.cfg, f, indent=4)


        # !watchlist remove {TICKER}
        if cmd == 'remove':

            try:

                self.WLIST.remove(args)
                await ctx.send(f'```diff\n- {args} removed from watchlist\n```')
                with open(self.STONKS_PATH, 'w') as f:
                    json.dump(self.cfg, f, indent=4)

            except:
                await ctx.send(f'```diff\n- {args} ticker not found in list\n```')


        # !watchlist quotes
        if cmd == 'quotes':

            wlist = self.Scrapper.WatchList(self.WLIST)
            await ctx.send(f'```diff\n+ quotes:\n{wlist.data_frame.to_string()}\n```')

        # no command
        if cmd == None:
            await ctx.send(f'```diff\n+ watchlist:\n{self.WLIST}```')



    @commands.command()
    async def stonks(self, ctx):

        """ returns quotes from watchlist """

        self.console_print(ctx)
        await ctx.message.delete()
        wlist = self.Scrapper.WatchList(self.cfg['Watch List'])
        await ctx.send(f'```diff\n+ watchlist quotes:\n{wlist.data_frame.to_string()}\n```')

    
    # FUNCTIONS

    def console_print(self, ctx):

        """ prints message info to console """

        now = dt.now().strftime("%m/%d/%y %H:%M:%S")
        print(f'[{now}] {ctx.message.author.name} called {ctx.message.content[1:]}')


    @staticmethod
    def ccon():
        os.system('cls||clear')


def setup(client):
    client.add_cog(Stonks(client))