#!/usr/bin/python
import sys, json, getopt
from format_strings import *

def main(argv):

	amount_bought = 0
	new_expenses = 0
	info = False

	try:
		opts, args = getopt.getopt(argv,"hiac:",["info=", "all=", "clear="])
	except getopt.GetoptError:
		print USAGE
		sys.exit(2)

	#parse through commandline args
	for opt, arg in opts:
		
		if opt == '-h':
			print USAGE
			sys.exit()

		elif opt in ("-c", "--clear"):
			
			#make sure the user knows what they're doing
			print PROMPT_COIN_DELETE % arg
			response = raw_input().upper()
			
			if(response == 'Y'):
			
				if(delete_crypto(arg)):
			
					sys.exit()
			
				print "Coin not found in portfolio"
			
			sys.exit()

		elif opt in ("-a", "--all"):
			
			coins = read_cryptos()

			#blank json_file, hence no portfolio exists
			if not coins:
				print "No portfolio"
				sys.exit(2)

			#display data of each coin in the portfolio
			for c in coins:
				update_and_display_crypto(coin=c, details=True)

			sys.exit()

		#inspect the coin during the value update in the json file
		elif opt in ("-i", "--info"):
			info = True			

	try:

		coin = args[0]

		#maxnum args
		if len(args) == 3:
			amount_bought = float(args[1])
			new_expenses = float(args[2])

		#inaccurate num of args
		elif not info or len(args) != 1:
			print USAGE
			sys.exit(2)

	except:
		print USAGE
		sys.exit(2)

	update_and_display_crypto(coin, amount_bought, new_expenses, info)

def read_cryptos():
	""" Returns a list of all the coins in the json """

	with open('CurrentExpenses', 'r+') as json_file:

		try:

			data = json.load(json_file)

		except:

			return []

		return [coin for coin in data.iterkeys()]

	return []

def delete_crypto(coin):
	""" Deletes an entry off the json from the file """

	with open('CurrentExpenses', 'r+') as json_file:

		try:

			data = json.load(json_file)

			if(data.pop(coin, None)):

				json_file.seek(0)
				json.dump(data, json_file)
				json_file.truncate()

				return True

		except:

			return False

	return False

def update_and_display_crypto(coin, bought=None, expenses=None, details=None):

	#set defaults if certain args aren't defined
	amount_bought = bought if bought else 0
	new_expenses = expenses if expenses else 0
	info = details if details else False

	coinmarketcap = Market()

	with open('CurrentExpenses', 'r+') as json_file:

		#attempt to read file data if any exists
		try:

			data = json.load(json_file)

		except:

			data = {}

		#check if there is previous data to work with
		#otherwise create new dictionary data
		if coin not in data:
			data[coin] = {}
			data[coin]["amount_owned"] = amount_bought
			data[coin]["total_paid"] = new_expenses
		else:
			data[coin]["amount_owned"] += amount_bought
			data[coin]["total_paid"] += new_expenses

		#inspect the coin through coinmarketcap
		if info:
			coin_data = json.loads(coinmarketcap.ticker(coin))[0]

			#check statistics and rates of the coin
			price = float(coin_data["price_usd"])
			hourperc = float(coin_data["percent_change_1h"])
			dayperc = float(coin_data["percent_change_24h"])
			weekperc = float(coin_data["percent_change_7d"])

			#print formatted string of the stats
			print '\n', coin.upper(), BREAK, TREND % (price, hourperc, dayperc, weekperc)

			#calculate profit earnings
			total_value = float(coin_data['price_usd']) * data[coin]['amount_owned']
			profit = total_value - data[coin]["total_paid"]

			#print profit earnings
			print '\n', COINS_SUMMARY % (data[coin]["amount_owned"], coin, total_value)
			print COINS_PROFIT % (coin, profit), '\n'
			
		json_file.seek(0)
		json.dump(data, json_file)
		json_file.truncate()

if __name__ == "__main__":

	try:
		
		from coinmarketcap import Market
	
	except:

		from massin import install

		install("coinmarketcap")

		from coinmarketcap import Market

	main(sys.argv[1:])