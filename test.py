
ticker_lst = ['MSFT', 'AAPL']

ticker_lst.append('QQQ')

print('after append')
print(ticker_lst)

ticker_lst.remove('QQQ')

print('after remove')
print(ticker_lst)

print('trying to remove again')
try:
    ticker_lst.remove('QQQ')
except Exception as e:
    print(e)

new_lst = ticker_lst

new_lst.append('QQQ')

print(ticker_lst)