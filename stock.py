from yahoo_finance import Share
from datetime import timedelta, date
from math import floor

money = float(raw_input("Money to invest?\n>"))
starty = int(raw_input("Year to start in?\n>"))
endy = int(raw_input("Year to end in?\n>"))
tick = raw_input("Ticker to use?\n>")

def share_price(ticker,date):
# Takes date and returns closing price of ticker on that date.
# Date takes datetime.date format yyyy-mm-dd
	return Share(ticker).get_historical(str(date-timedelta(days=5)),
										str(date))[0][u'Adj_Close']


def price_list_quarters(ticker,startyear,endyear):
	plist = []
	plist.append(float(share_price(ticker,date(startyear,1,1))))
	for num in range(0,endyear-startyear+1):
		plist.append(float(share_price(ticker,date(startyear+num,3,31))))
		plist.append(float(share_price(ticker,date(startyear+num,6,30))))
		plist.append(float(share_price(ticker,date(startyear+num,9,30))))
		plist.append(float(share_price(ticker,date(startyear+num,12,31))))
	return plist

def sig3(invested,ticker,startyear,endyear):
	# Determines total portfolio value using 3sig method.
	to_invest = invested*0.8
	money_in_stocks = pricelist[0]*floor(to_invest/pricelist[0])
	sidelines = invested - money_in_stocks
	shares = [None]*len(pricelist)
	shares[0] = floor(to_invest/pricelist[0])
	
	for num in range(1,len(pricelist)):
		shares[num] = shares[num-1]+round((shares[num-1]*(pricelist[num-1]
										*1.03-pricelist[num]))/pricelist[num])
	
	fund = 0
	for num in range(1,len(shares)):
		fund = fund + (shares[num]-shares[num-1])*pricelist[num]
	sidelines = sidelines - fund
	return sidelines + shares[len(shares)-1]*pricelist[len(pricelist)-1]
	
def all_in(invested,ticker,startyear,endyear):
	shares = floor(invested/pricelist[0])
	sell_price_per_share = pricelist[len(pricelist)-1]
	uninvested = invested - shares*pricelist[0]
	return shares*sell_price_per_share + uninvested
											
def dollaz(number):
	return '${:,.2f}'.format(number)

pricelist = price_list_quarters(tick,starty,endy)
print "price list:", pricelist
print "3sig total:", dollaz(sig3(money,tick,starty,endy))
print "all in total:", dollaz(all_in(money,tick,starty,endy))
print "80% in: ", dollaz(all_in(money*.8,tick,starty,endy))