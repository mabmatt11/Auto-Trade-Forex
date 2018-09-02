import v20
import time
import logging
from tkinter import *
from datetime import datetime, timedelta

logging.basicConfig(filename='Bot_v1.log', filemode='w', level=logging.DEBUG)

# This will initialize the api that connects to oanda
api = v20.Context('api-fxpractice.oanda.com', '443', token='INSERT')

# Global variables changed after starting GUI, starting with default values.
minuteDelt = 4
tradeAmount = 1000
stloPerc = 0.0001
getgaPerc = 0.0001

# Global Variabls for if each trade is owned (Used in Exiting GUI)
EUR_USDowned = 0
USD_CADowned = 0
USD_CHFowned = 0
GBP_USDowned = 0
NZD_USDowned = 0
AUD_USDowned = 0
USD_JPYowned = 0

# Function to purchase forex. Two inputs: which trade and the amount.
# One output: Whether the trade was successful or not.
def purchase(trade, amount):
	buy = api.order.market('101-001-5991540-001', instrument=trade, units=amount)
	time.sleep(0.05)
	#print("Response: {} ({})".format(buy.status, buy.reason))
	return buy.status;

# Function to sell forex. Two inputs: which trade and the amount.
# One output: Whether the trade was successfull or not.
def sell(trade, amount):
	buy = api.order.market('101-001-5991540-001', instrument=trade, units=-amount)
	time.sleep(0.05)
	#print("Response: {} ({})".format(buy.status, buy.reason))
	return buy.status;

# Function to get 30 day moving average on this day for certain trade.
# One input: the trade. One output: The moving average on the current day.
def movingAverage1(trade):
	prices = []
	count = 0
	past_prices = api.instrument.candles(instrument=trade, granularity="D", count=30)
	time.sleep(0.04)
	candles = past_prices.get("candles")
	while(count<30):
		c = getattr(candles[count], "mid", None)
		prices.append(c.c)
		count = count + 1

	return sum(prices)/len(prices);

# Function to get 30 day moving average on day before for certain trade.
# One input: the trade. One output: The moving average on the day before.
def movingAverage2(trade):
	prices = []
	count = 0
	past_prices = api.instrument.candles(instrument=trade, granularity="D", count=31)
	time.sleep(0.04)
	candles = past_prices.get("candles")
	while(count<31):
		c = getattr(candles[count], "mid", None)
		prices.append(c.c)
		count = count + 1

	return (sum(prices) - prices[30])/(len(prices)-1);

# Function to get 30 day moving average for two days ago for certain trade.
# One input: the trade. One output: The moving average for two days ago.
def movingAverage3(trade):
	prices = []
	count = 0
	past_prices = api.instrument.candles(instrument=trade, granularity="D", count=32)
	time.sleep(0.04)
	candles = past_prices.get("candles")
	while(count<32):
		c = getattr(candles[count], "mid", None)
		prices.append(c.c)
		count = count + 1

	return (sum(prices) - prices[30] - prices[31])/(len(prices)-2);

# Function to get 30 day moving average for three days ago for certain trade.
# One input: the trade. One output: The moving average for three days ago.
def movingAverage4(trade):
	prices = []
	count = 0
	past_prices = api.instrument.candles(instrument=trade, granularity="D", count=33)
	time.sleep(0.04)
	candles = past_prices.get("candles")
	while(count<33):
		c = getattr(candles[count], "mid", None)
		prices.append(c.c)
		count = count + 1

	return (sum(prices) - prices[30] - prices[31] - prices[32])/(len(prices)-3);

# Function to get 30 day moving average for four days ago for certain trade.
# One input: the trade. One output: The moving average for four days ago.
def movingAverage5(trade):
	prices = []
	count = 0
	past_prices = api.instrument.candles(instrument=trade, granularity="D", count=34)
	time.sleep(0.04)
	candles = past_prices.get("candles")
	while(count<34):
		c = getattr(candles[count], "mid", None)
		prices.append(c.c)
		count = count + 1

	return (sum(prices) - prices[30] - prices[31] - prices[32] - prices[33])/(len(prices)-4);

# Function to get the current price of a certain trade. One input: the trade.
# One output: the price.
def currentPrice(trade):
	bad = True
	response = []

	while(bad):
		time1 = (datetime.utcnow() - timedelta(minutes=10)).isoformat('T')+'Z'
		response = api.pricing.get('101-001-5991540-001', instruments=trade, since=time1, includeUnitsAvailable=False)
		time.sleep(0.005)
		if len(response.get("prices")) == 0:
			bad = True
		else:
			bad = False


	return response.get("prices")[0].bids[0].price;

# Function to determine if the slope of the last 5 days moving averages is sloping up.
# One input: moving averages array. One output: Whether it is sloping up or not.
def movingAverageSlopeUp(movingAve):
	if movingAve[0] <= movingAve[1]:
		if movingAve[1] <= movingAve[2]:
			if movingAve[2] <= movingAve[3]:
				if movingAve[3] <= movingAve[4]:
					return True;
	



	return False;

# Function to determine if the slope of the last 5 days moving averages is sloping down.
# One input: moving averages array. One output: Whether or not it is sloping down.
def movingAverageSlopeDown(movingAve):
	if movingAve[0] >= movingAve[1]:
		if movingAve[1] >= movingAve[2]:
			if movingAve[2] >= movingAve[3]:
				if movingAve[3] >= movingAve[4]:
					return True;
	



	return False;

# Function to determine if the last 5 days moving averages are changing trend to slope up again.
# One input: moving averages array. One output: Whether or not it is changing trend up.
def movingAveChangeUp(movingAve):
	if movingAve[0] > movingAve[1]:
		if movingAve[1] >= movingAve[2]:
			if movingAve[3] >= movingAve[2] and movingAve[4] > movingAve[2]:
				return True;


		if movingAve[1] < movingAve[2] and movingAve[2] < movingAve[3] and movingAve[3] < movingAve[4]:
			return True;


	return False;

# Function to determine if the last 5 days moving averages are changing trend to slope down again.
# One input: moving averages array. One output: Whether or not it is changing trend down.
def movingAveChangeDown(movingAve):
	if movingAve[0] < movingAve[1]:
		if movingAve[1] <= movingAve[2]:
			if movingAve[3] <= movingAve[2] and movingAve[4] < movingAve[2]:
				return True;


		if movingAve[1] > movingAve[2] and movingAve[2] > movingAve[3] and movingAve[3] > movingAve[4]:
			return True;


	return False;

# Function to determine if the recent prices are trending up.
# One input: array of recent prices. One output: Whether or not it is trending up.
def recentPriceUp(prices):
	if len(prices) >= 4:
		if prices[len(prices)-1] > prices[len(prices)-2]: 
			if prices[len(prices)-2] > prices[len(prices)-3]:
				if prices[len(prices)-3] > prices[len(prices)-4]:
					return True;
			



	return False;
		
# Function to determine if the recent prices are trending down.
# One input: array of recent prices. One output: Whether or not it is trending down.
def recentPriceDown(prices):
	if len(prices) >= 5:
		if prices[len(prices)-1] < prices[len(prices)-2]:
			return True;


	return False;

# The driver of our program. All important things happen here.
def main():

	# Get the global variables
	global minuteDelt
	global tradeAmount
	global stloPerc 
	global getgaPerc

	#Initialize and set up the SETUP GUI
	master = Tk()
	master.configure(bg='gray76')
	master.minsize(width=400, height=400)
	master.maxsize(width=400, height=400)
	master.wm_title("Oanda Bot Set Up")
	
	#Title Information on how to use
	space1 = Label(master, height = 3, width = 34, bg="gray76").grid(row=0)
	Open = Label(master, text='Enter Values and Press Button to Begin the Bot', width = 60, bg="gray76", fg="black", anchor=W, font="Verdana 10 underline").place(x=50, y = 10)
	
	#Labels for what to enter in the GUI
	L1 = Label(master, text='Time Check Constant (2-8): ', anchor=E, bg="black", fg="white", relief = GROOVE, width = 34).grid(row = 1)
	space2 = Label(master, height = 3, width = 34, bg="gray76").grid(row=2)
	L2 = Label(master, text='Amount of Currency to Trade per Trade (100-5000): ', anchor=E, bg="black", fg="white", relief = GROOVE, width = 34).grid(row = 3)
	space3 = Label(master, height = 3, width = 34, bg="gray76").grid(row=4)
	L3 = Label(master, text='Stop Loss Percentage (0.0004 - 0.002): ', anchor=E, bg="black", fg="white", relief = GROOVE, width = 34).grid(row = 5)
	space4 = Label(master, height = 3, width = 34, bg="gray76").grid(row=6)
	L4 = Label(master, text='Get Gain Percentage (0.0004 - 0.002): ', anchor=E, bg="black", fg="white", relief = GROOVE, width = 34).grid(row = 7)

	#Called when setup gui is told to set and finish
	def set():
		global minuteDelt
		global tradeAmount
		global stloPerc 
		global getgaPerc
		
		#Sets the respective values from the entries
		if E1.get() != '':
			minuteDelt = int(E1.get())

		if E2.get() != '':
			tradeAmount = int(E2.get())

		if E3.get() != '':
			stloPerc = float(E3.get())

		if E4.get() != '':
			getgaPerc = float(E4.get())

		master.destroy()
		
		return;
	
	#Make sure when closing window, gui still sets
	master.protocol("WM_DELETE_WINDOW", set)
			
	#Entry slots for user input
	E1 = Entry(master, width = 25)
	E1.grid(row = 1, column = 1)
	E2 = Entry(master, width = 25)
	E2.grid(row = 3, column = 1)
	E3 = Entry(master, width = 25)
	E3.grid(row = 5, column = 1)
	E4 = Entry(master, width = 25)
	E4.grid(row = 7, column = 1)

	#The button that says to set the program values and closes the GUI
	B1 = Button(master, text="Start Bot", relief=RAISED, bd=5, bg='red', fg='black', command=set).place(x = 185, y = 325)
	
	#Runs the SETUP gui until the button is pressed.
	master.mainloop()

	####################################
	logging.info('Minute Spacing: ' + str(minuteDelt))
	logging.info('Trade Amount: ' + str(tradeAmount))
	logging.info('Stop Loss: ' + str(stloPerc))
	logging.info('Get Gain: ' + str(getgaPerc))
	
	#print(minuteDelt) 
	#print(tradeAmount)
	#print(stloPerc)
	#print(getgaPerc)
	####################################
	
	# The account number that connects the online account
	account_id = '101-001-5991540-001'
	#################################################

	# The CURRENT possible trades
	trades = ['EUR_USD', 'USD_CAD', 'USD_CHF', 'GBP_USD', 'NZD_USD', 'AUD_USD', 'USD_JPY']
	
	# Indicators on whether each trade is owned and at what price it was bought
	global EUR_USDowned
	global USD_CADowned
	global USD_CHFowned
	global GBP_USDowned
	global NZD_USDowned
	global AUD_USDowned
	global USD_JPYowned

	# Tracks short term prices as indicator
	EUR_USDprices = []
	USD_CADprices = []
	USD_CHFprices = []
	GBP_USDprices = []
	NZD_USDprices = []
	AUD_USDprices = []
	USD_JPYprices = []

	# initialize time tracking array
	time1 = [0]

	#Initialize the running GUI
	root = Tk()

	# Called when exiting the GUI. Sells all owned trades and ends the program.
	def exit():
		global EUR_USDowned
		global USD_CADowned
		global USD_CHFowned
		global GBP_USDowned
		global NZD_USDowned
		global AUD_USDowned
		global USD_JPYowned

		if EUR_USDowned != 0:
			sell('EUR_USD', tradeAmount)
			
		if USD_CADowned != 0:
			sell('USD_CAD', tradeAmount)
			
		if USD_CHFowned != 0:
			sell('USD_CHF', tradeAmount)
			
		if GBP_USDowned != 0:
			sell('GBP_USD', tradeAmount)
			
		if NZD_USDowned != 0:
			sell('NZD_USD', tradeAmount)
			
		if AUD_USDowned != 0:
			sell('AUD_USD', tradeAmount)
			
		if USD_JPYowned != 0:
			sell('USD_JPY', tradeAmount)
			
		logging.info('Application Ended...')
		
		root.destroy()
		

	# Sets up how the GUI looks and runs.
	root.protocol("WM_DELETE_WINDOW", exit)
	root.configure(bg='gray76')
	root.minsize(width=900, height=410)
	root.maxsize(width=900, height=410)
	root.wm_title("Oanda Bot Current Summary")

	# Variables in the GUI measuring amount of a trade owned.
	EUR_USDgui = IntVar()
	EUR_USDgui.set(0)
	USD_CADgui = IntVar()
	USD_CADgui.set(0)
	USD_CHFgui = IntVar()
	USD_CHFgui.set(0)
	GBP_USDgui = IntVar()
	GBP_USDgui.set(0)
	NZD_USDgui = IntVar()
	NZD_USDgui.set(0)
	AUD_USDgui = IntVar()
	AUD_USDgui.set(0)
	USD_JPYgui = IntVar()
	USD_JPYgui.set(0)

	# Variables in the GUI measuring the price the trade was bought at.
	EUR_USDbought = IntVar()
	EUR_USDbought.set(0)
	USD_CADbought = IntVar()
	USD_CADbought.set(0)
	USD_CHFbought = IntVar()
	USD_CHFbought.set(0)
	GBP_USDbought = IntVar()
	GBP_USDbought.set(0)
	NZD_USDbought = IntVar()
	NZD_USDbought.set(0)
	AUD_USDbought = IntVar()
	AUD_USDbought.set(0)
	USD_JPYbought = IntVar()
	USD_JPYbought.set(0)

	# Variables in the GUI measuring the current price of trades.
	EUR_USDp = IntVar()
	EUR_USDp.set(0)
	USD_CADp = IntVar()
	USD_CADp.set(0)
	USD_CHFp = IntVar()
	USD_CHFp.set(0)
	GBP_USDp = IntVar()
	GBP_USDp.set(0)
	NZD_USDp = IntVar()
	NZD_USDp.set(0)
	AUD_USDp = IntVar()
	AUD_USDp.set(0)
	USD_JPYp = IntVar()
	USD_JPYp.set(0)

	# Variables in the GUI measuring the plus/loss on a certain trade.
	EUR_USDpm = IntVar()
	EUR_USDpm.set(0)
	USD_CADpm = IntVar()
	USD_CADpm.set(0)
	USD_CHFpm = IntVar()
	USD_CHFpm.set(0)
	GBP_USDpm = IntVar()
	GBP_USDpm.set(0)
	NZD_USDpm = IntVar()
	NZD_USDpm.set(0)
	AUD_USDpm = IntVar()
	AUD_USDpm.set(0)
	USD_JPYpm = IntVar()
	USD_JPYpm.set(0)

	#Text to instruct the user.
	top = Label(root, height = 3, width = 10, bg="gray76")
	top.grid(row=0)
	instruction = Label(root, text='Live Results from the online Bot. Press End to Sell All and Exit.', width = 100, bg="gray76", anchor=W, font="Verdana 10 underline").place(x=210, y = 10)
	
	#The top of the grid defining each column.
	blank1 = Label(root, text='', bg="gray78", width=10, height=2).grid(row=1)
	grid1 = Label(root, text='Trade', anchor=E, bg="black", fg="white", relief = GROOVE, width=20, height =2)
	grid1.grid(row=1, column=1)
	grid2 = Label(root, text='Amount Owned', anchor=E, bg="black", fg="white", relief=GROOVE, width=17, height=2)
	grid2.grid(row=1, column=2)
	grid3 = Label(root, text='Price Bought At Last', anchor=E, bg="black", fg="white", relief=GROOVE, width = 26, height = 2)
	grid3.grid(row=1, column=3)
	grid4 = Label(root, text='Recent Price', anchor = E, bg="black", fg="white", relief = GROOVE, width = 20, height =2)
	grid4.grid(row=1, column=4)
	grid5 = Label(root, text='Money Made', anchor=E, bg="black", fg="white", relief =GROOVE, width = 18, height=2)
	grid5.grid(row=1, column=5)
	
	#Row 1 of the trades in GUI.
	blank2 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=2)
	EU1 = Label(root, text='EUR/USD: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	EU1.grid(row=2, column=1)
	EU2 = Label(root, textvariable=EUR_USDgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	EU2.grid(row=2, column=2)
	EU3 = Label(root, textvariable=EUR_USDbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	EU3.grid(row=2, column=3)
	EU4 = Label(root, textvariable=EUR_USDp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	EU4.grid(row=2, column=4)
	EU5 = Label(root, textvariable=EUR_USDpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	EU5.grid(row=2,  column=5)

	#Row 2 of the trades in GUI.
	blank3 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=3)
	UC1 = Label(root, text='USD/CAD: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	UC1.grid(row=3, column=1)
	UC2 = Label(root, textvariable=USD_CADgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	UC2.grid(row=3, column=2)
	UC3 = Label(root, textvariable=USD_CADbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	UC3.grid(row=3, column=3)
	UC4 = Label(root, textvariable=USD_CADp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	UC4.grid(row=3, column=4)
	UC5 = Label(root, textvariable=USD_CADpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	UC5.grid(row=3,  column=5)

	#Row 3 of the trades in GUI.
	blank4 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=4)
	UCH1 = Label(root, text='USD/CHF: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	UCH1.grid(row=4, column=1)
	UCH2 = Label(root, textvariable=USD_CHFgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	UCH2.grid(row=4, column=2)
	UCH3 = Label(root, textvariable=USD_CHFbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	UCH3.grid(row=4, column=3)
	UCH4 = Label(root, textvariable=USD_CHFp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	UCH4.grid(row=4, column=4)
	UCH5 = Label(root, textvariable=USD_CHFpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	UCH5.grid(row=4,  column=5)

	#Row 4 of the trades in GUI.
	blank5 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=5)
	GU1 = Label(root, text='GBP/USD: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	GU1.grid(row=5, column=1)
	GU2 = Label(root, textvariable=GBP_USDgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	GU2.grid(row=5, column=2)
	GU3 = Label(root, textvariable=GBP_USDbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	GU3.grid(row=5, column=3)
	GU4 = Label(root, textvariable=GBP_USDp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	GU4.grid(row=5, column=4)
	GU5 = Label(root, textvariable=GBP_USDpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	GU5.grid(row=5,  column=5)

	#Row 5 of the trades in GUI.
	blank6 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=6)
	NU1 = Label(root, text='NZD/USD: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	NU1.grid(row=6, column=1)
	NU2 = Label(root, textvariable=NZD_USDgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	NU2.grid(row=6, column=2)
	NU3 = Label(root, textvariable=NZD_USDbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	NU3.grid(row=6, column=3)
	NU4 = Label(root, textvariable=NZD_USDp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	NU4.grid(row=6, column=4)
	NU5 = Label(root, textvariable=NZD_USDpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	NU5.grid(row=6,  column=5)
	
	#Row 6 of the trades in GUI.
	blank7 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=7)
	AU1 = Label(root, text='AUD/USD: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	AU1.grid(row=7, column=1)
	AU2 = Label(root, textvariable=AUD_USDgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	AU2.grid(row=7, column=2)
	AU3 = Label(root, textvariable=AUD_USDbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	AU3.grid(row=7, column=3)
	AU4 = Label(root, textvariable=AUD_USDp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	AU4.grid(row=7, column=4)
	AU5 = Label(root, textvariable=AUD_USDpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	AU5.grid(row=7,  column=5)

	#Row 7 of the trades in GUI.
	blank8 = Label(root, text='', bg="gray76", width=10, height=2).grid(row=8)
	UJ1 = Label(root, text='USD/JPY: ', anchor=E, bg = "gray76", fg="black", relief = GROOVE, width= 20, height = 2)
	UJ1.grid(row=8, column=1)
	UJ2 = Label(root, textvariable=USD_JPYgui, anchor=E, bg = "gray76", fg="black", relief =GROOVE, width = 17, height=2)
	UJ2.grid(row=8, column=2)
	UJ3 = Label(root, textvariable=USD_JPYbought, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=26, height=2)
	UJ3.grid(row=8, column=3)
	UJ4 = Label(root, textvariable=USD_JPYp, anchor=E, bg="gray76", fg="black", relief=GROOVE, width=20, height = 2)
	UJ4.grid(row=8, column=4)
	UJ5 = Label(root, textvariable=USD_JPYpm, anchor=E, bg="green", fg="white", relief=GROOVE, width=18, height=2)
	UJ5.grid(row=8,  column=5)

	runningLabel = Label(root, text='The Bot is Running When I am Changing Colors Regularly!', anchor=W, bg="gray76", fg="Blue", width=100, height=2)
	runningLabel.place(x=150, y=360)
	
	#Button that sells all owned and exits the program.
	allDone = Button(root, text="Sell All and End", relief=RAISED, bd=5, bg='red', fg='black', command=exit).place(x=480, y = 360)

	##############################
	n = 0
	m = 0
	##############################
	
	#Determines if the code should end.
	exit = False

	while not exit: # This runs a loop until user exits
		try:
			#updates the GUI
			root.update_idletasks()
			root.update()
			
			#Used in updating information
			newTime = False
		
			# to get the minute we are running the iteration at
			now = datetime.utcnow().isoformat('T')+'Z'
			time.sleep(0.001)
			hold = now.split(":")
			minute = int(hold[1])
		
			# only add minute time if predetermined time later than last input
			if (minute > (time1[len(time1)-1]+minuteDelt) and minute <= 58):
				time1.append(minute)
				logging.info('New time: ' + str(minute))
				newTime = True

			# reset time counter if at end of hour
			if minute > 58:
				logging.info('Time array has been reset')
				time1 = [0]
				
			# run algorithm for each possible trade
			for i in trades:
				mSlopeUp = False	# reset all indicators to false
				mSlopeDown = False
				mChangeUp = False
				mChangeDown = False
				lookBuy = False
				lookSell = False

				#Get current price of trade being compared (too save processing time)
				cPrice = currentPrice(i)
				
				#Update the GUI
				root.update_idletasks()
				root.update()
	
				if n%4 == 0:
					# get past five days 30 day moving ave for current trade
					mAve = []
					mAve.append(movingAverage5(i))
					mAve.append(movingAverage4(i))
					mAve.append(movingAverage3(i))
					mAve.append(movingAverage2(i))
					mAve.append(movingAverage1(i))
	
					# get indicators for current trade
					mSlopeUp = movingAverageSlopeUp(mAve)
					mSlopeDown = movingAverageSlopeDown(mAve)
					mChangeUp = movingAveChangeUp(mAve)
					mChangeDown = movingAveChangeDown(mAve)	

					if m == 0:
						runningLabel.configure(fg="red")
						m = m+1
					elif m == 1:
						runningLabel.configure(fg="yellow")
						m = m+1
					elif m == 2:
						runningLabel.configure(fg="orange")
						m = m+1
					elif m == 3:
						runningLabel.configure(fg="white")
						m = m+1
					elif m == 4:
						runningLabel.configure(fg="black")
						m = m+1
					elif m == 5:
						runningLabel.configure(fg="violet")
						m = m+1
					elif m == 6:
						runningLabel.configure(fg="blue")
						m = 0
				
				#Update the GUI
				root.update_idletasks()
				root.update()

				#When there is a real update happening:
				#For each trade, add the newest price to their current prices...
				#Set the newest price gathered to the GUI...
				#Check conditions to see if buy or sell should happen.
				if newTime:
					if i == 'EUR_USD':
						EUR_USDprices.append(cPrice)
						EUR_USDp.set(cPrice)
						if EUR_USDowned == 0:		
							lookBuy = recentPriceUp(EUR_USDprices)
				
						if EUR_USDowned != 0:
							lookSell = recentPriceDown(EUR_USDprices)


					if i == 'USD_CAD':
						USD_CADprices.append(cPrice)
						USD_CADp.set(cPrice)
						if USD_CADowned == 0:			
							lookBuy = recentPriceUp(USD_CADprices)
				
						if USD_CADowned != 0:
							lookSell = recentPriceDown(USD_CADprices)


					if i == 'USD_CHF':
						USD_CHFprices.append(cPrice)
						USD_CHFp.set(cPrice)
						if USD_CHFowned == 0:
							lookBuy = recentPriceUp(USD_CHFprices)
				
						if USD_CHFowned != 0:
							lookSell = recentPriceDown(USD_CHFprices)


					if i == 'GBP_USD':
						GBP_USDprices.append(cPrice)
						GBP_USDp.set(cPrice)
						if GBP_USDowned == 0:
							lookBuy = recentPriceUp(GBP_USDprices)
								
						if GBP_USDowned != 0:
							lookSell = recentPriceDown(GBP_USDprices)


					if i == 'NZD_USD':
						NZD_USDprices.append(cPrice)
						NZD_USDp.set(cPrice)
						if NZD_USDowned == 0:		
							lookBuy = recentPriceUp(NZD_USDprices)
				
						if NZD_USDowned != 0:
							lookSell = recentPriceDown(NZD_USDprices)
	

					if i == 'AUD_USD':
						AUD_USDprices.append(cPrice)
						AUD_USDp.set(cPrice)
						if AUD_USDowned == 0:
							lookBuy = recentPriceUp(AUD_USDprices)
				
						if AUD_USDowned != 0:
							lookSell = recentPriceDown(AUD_USDprices)


					if i == 'USD_JPY':
						USD_JPYprices.append(cPrice)
						USD_JPYp.set(cPrice)
						if USD_JPYowned == 0:
							lookBuy = recentPriceUp(USD_JPYprices)
							
						if USD_JPYowned != 0:
							lookSell = recentPriceDown(USD_JPYprices)
			
			
				root.update_idletasks()
				root.update()
				
###### BUYING AND SELLING ALGORITHM ###### 
				if i == 'EUR_USD':
					if (cPrice <= EUR_USDowned*(1-stloPerc) or (EUR_USDowned > 0 and (mChangeDown or mSlopeDown or cPrice >= EUR_USDowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							EUR_USDpm.set((cPrice-EUR_USDowned+EUR_USDpm.get())*tradeAmount) ## CHECK CHANGES HERE FOR FURTHER CHANGES
							logging.info('EUR_USD sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(EUR_USDowned*(1-stloPerc)) + '. Get Gain Price = ' + str(EUR_USDowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown) + '. Plus Minus: ' + str(EUR_USDpm.get()))
							EUR_USDowned = 0
							EUR_USDbought.set(0)
							EUR_USDgui.set(0)
							if EUR_USDpm.get() < 0:
								EU5.configure(bg="red")
							else:
								EU5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and EUR_USDowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							EUR_USDowned = currentPrice(i) + 0.00015
							logging.info('EUR_USD bought! Current Price = ' + str(EUR_USDowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							EUR_USDbought.set(EUR_USDowned)
							EUR_USDgui.set(tradeAmount)


					if len(EUR_USDprices) > 10:
						logging.info('EUR_USD Prices Array Reset')
						EUR_USDprices = [EUR_USDprices[len(EUR_USDprices)-4], EUR_USDprices[len(EUR_USDprices)-3], EUR_USDprices[len(EUR_USDprices)-2], EUR_USDprices[len(EUR_USDprices)-1]]
	

				if i == 'USD_CAD':
					if (cPrice <= (USD_CADowned*(1.0-stloPerc)) or (USD_CADowned > 0 and (mChangeDown or mSlopeDown or cPrice >= USD_CADowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('USD_CAD sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(USD_CADowned*(1-stloPerc)) + '. Get Gain Price = ' + str(USD_CADowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							USD_CADpm.set((cPrice-USD_CADowned+USD_CADpm.get())*tradeAmount)
							USD_CADowned = 0
							USD_CADbought.set(0)
							USD_CADgui.set(0)
							if USD_CADpm.get() < 0:
								UC5.configure(bg="red")
							else:
								UC5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and USD_CADowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							USD_CADowned = currentPrice(i) + 0.00020
							logging.info('USD_CAD bought! Current Price = ' + str(USD_CADowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							USD_CADbought.set(USD_CADowned)
							USD_CADgui.set(tradeAmount)


					if len(EUR_USDprices) > 10:
						logging.info('USD_CAD Prices Array Reset')
						USD_CADprices = [USD_CADprices[len(USD_CADprices)-4], USD_CADprices[len(USD_CADprices)-3], USD_CADprices[len(USD_CADprices)-2], USD_CADprices[len(USD_CADprices)-1]]


				if i == 'USD_CHF':
					if (cPrice <= (USD_CHFowned*(1.0-stloPerc)) or (USD_CHFowned > 0 and (mChangeDown or mSlopeDown or cPrice >= USD_CHFowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('USD_CHF sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(USD_CHFowned*(1-stloPerc)) + '. Get Gain Price = ' + str(USD_CHFowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							USD_CHFpm.set((cPrice-USD_CHFowned+USD_CHFpm.get())*tradeAmount)
							USD_CHFowned = 0
							USD_CHFbought.set(0)
							USD_CHFgui.set(0)
							if USD_CHFpm.get() < 0:
								UCH5.configure(bg="red")
							else:
								UCH5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and USD_CHFowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							USD_CHFowned = currentPrice(i) + 0.00026
							logging.info('USD_CHF bought! Current Price = ' + str(USD_CHFowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							USD_CHFbought.set(USD_CHFowned)
							USD_CHFgui.set(tradeAmount)


					if len(USD_CHFprices) > 10:
						logging.info('USD_CHF Prices Array Reset')
						USD_CHFprices = [USD_CHFprices[len(USD_CHFprices)-4], USD_CHFprices[len(USD_CHFprices)-3], USD_CHFprices[len(USD_CHFprices)-2], USD_CHFprices[len(USD_CHFprices)-1]]


				if i == 'GBP_USD':
					if (cPrice <= (GBP_USDowned*(1.0-stloPerc)) or (GBP_USDowned > 0 and (mChangeDown or mSlopeDown or cPrice >= GBP_USDowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('GBP_USD sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(GBP_USDowned*(1-stloPerc)) + '. Get Gain Price = ' + str(GBP_USDowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							GBP_USDpm.set((cPrice-GBP_USDowned+GBP_USDpm.get())*tradeAmount)
							GBP_USDowned = 0
							GBP_USDbought.set(0)
							GBP_USDgui.set(0)
							if GBP_USDpm.get() < 0:
								GU5.configure(bg="red")
							else:
								GU5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and GBP_USDowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							GBP_USDowned = currentPrice(i) + 0.00035
							logging.info('GBP_USD bought! Current Price = ' + str(GBP_USDowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							GBP_USDbought.set(GBP_USDowned)
							GBP_USDgui.set(0)


					if len(GBP_USDprices) > 10:
						logging.info('GBP_USD Prices Array Reset')
						GBP_USDprices = [GBP_USDprices[len(GBP_USDprices)-4], GBP_USDprices[len(GBP_USDprices)-3], GBP_USDprices[len(GBP_USDprices)-2], GBP_USDprices[len(GBP_USDprices)-1]]


				if i == 'NZD_USD':
					if (cPrice <= (NZD_USDowned*(1.0-stloPerc)) or (NZD_USDowned > 0 and (mChangeDown or mSlopeDown or cPrice >= NZD_USDowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('NZD_USD sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(NZD_USDowned*(1-stloPerc)) + '. Get Gain Price = ' + str(NZD_USDowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							NZD_USDpm.set((cPrice-NZD_USDowned+NZD_USDpm.get())*tradeAmount)
							NZD_USDowned = 0
							NZD_USDbought.set(0)
							NZD_USDgui.set(0)
							if NZD_USDpm.get() < 0:
								NU5.configure(bg="red")
							else:
								NU5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and NZD_USDowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							NZD_USDowned = currentPrice(i) + 0.00019
							logging.info('NZD_USD bought! Current Price = ' + str(NZD_USDowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							NZD_USDbought.set(NZD_USDowned)
							NZD_USDgui.set(tradeAmount)


					if len(NZD_USDprices) > 10:
						logging.info('NZD_USD Prices Array Reset')
						NZD_USDprices = [NZD_USDprices[len(NZD_USDprices)-4], NZD_USDprices[len(NZD_USDprices)-3], NZD_USDprices[len(NZD_USDprices)-2], NZD_USDprices[len(NZD_USDprices)-1]]


				if i == 'AUD_USD':
					if (cPrice <= (AUD_USDowned*(1.0-stloPerc)) or (AUD_USDowned > 0 and (mChangeDown or mSlopeDown or cPrice >= AUD_USDowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('AUD_USD sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(AUD_USDowned*(1-stloPerc)) + '. Get Gain Price = ' + str(AUD_USDowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							AUD_USDpm.set((cPrice-AUD_USDowned+AUD_USDpm.get())*tradeAmount)
							AUD_USDowned = 0
							AUD_USDbought.set(0)
							AUD_USDgui.set(0)
							if AUD_USDpm.get() < 0:
								AU5.configure(bg = "red")
							else:
								AU5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and AUD_USDowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							AUD_USDowned = currentPrice(i) + 0.00015
							logging.info('AUD_USD bought! Current Price = ' + str(AUD_USDowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							AUD_USDbought.set(AUD_USDowned)
							AUD_USDgui.set(tradeAmount)


					if len(AUD_USDprices) > 10:
						logging.info('AUD_USD Prices Array Reset')
						AUD_USDprices = [AUD_USDprices[len(AUD_USDprices)-4], AUD_USDprices[len(AUD_USDprices)-3], AUD_USDprices[len(AUD_USDprices)-2], AUD_USDprices[len(AUD_USDprices)-1]]


				if i == 'USD_JPY':
					if (cPrice <= (USD_JPYowned*(1.0-stloPerc)) or (USD_JPYowned > 0 and (mChangeDown or mSlopeDown or cPrice >= USD_JPYowned*(1+getgaPerc)))):
						check = sell(i, tradeAmount)
						if check == 201:
							logging.info('USD_JPY sold! Current Price = ' + str(cPrice) + '. Stop Loss Price = ' + str(USD_JPYowned*(1-stloPerc)) + '. Get Gain Price = ' + str(USD_JPYowned*(1+getgaPerc)) + '. mChangeDown = ' + str(mChangeDown) + '. mSlopeDown = ' + str(mSlopeDown))
							USD_JPYpm.set((cPrice-USD_JPYowned+USD_JPYpm.get())*tradeAmount)
							USD_JPYowned = 0
							USD_JPYbought.set(0)
							USD_JPYgui.set(0)
							if USD_JPYpm.get() < 0:
								UJ5.configure(bg="red")
							else:
								UJ5.configure(bg="green")


					if (lookBuy and (mSlopeUp or mChangeUp) and USD_JPYowned == 0):
						check = purchase(i, tradeAmount)
						if check == 201:
							USD_JPYowned = currentPrice(i) + 0.016
							logging.info('USD_JPY bought! Current Price = ' + str(USD_JPYowned) + '. mSlopeUp = ' + str(mSlopeUp) + '. mChangeUp = ' + str(mChangeUp))
							USD_JPYbought.set(USD_JPYowned)
							USD_JPYgui.set(0)


					if len(USD_JPYprices) > 10:
						logging.info('USD_JPY Prices Array Reset')
						USD_JPYprices = [USD_JPYprices[len(USD_JPYprices)-4], USD_JPYprices[len(USD_JPYprices)-3], USD_JPYprices[len(USD_JPYprices)-2], USD_JPYprices[len(USD_JPYprices)-1]]

				
			#Update the GUI
			root.update_idletasks()
			root.update()
			
			############################
			#print(n)
			logging.info('Loop iteration: ' + str(n))
			n = n+1
			############################
			
		except IndexError:
			########################################
			#print("Caught Index Error")
			logging.info('INDEX ERROR CAUGHT!')
			########################################
		except v20.errors.V20Timeout:
			########################################
			#print("GOTCHA!")
			logging.info('CAUGHT A V20Timeout ERROR')
			########################################
			api = v20.Context('api-fxpractice.oanda.com', '443', token='b153af56babe09b97822dde3bdc746e3-e52d835fbd5c2d49e262d33e9581af77')
			time.sleep(2)
		except v20.errors.V20ConnectionError:
			########################################
			#print("GOTCHA 2!")
			logging.info('CAUGHT A V20ConnectionError ERROR')
			########################################
			api = v20.Context('api-fxpractice.oanda.com', '443', token='b153af56babe09b97822dde3bdc746e3-e52d835fbd5c2d49e262d33e9581af77')
			time.sleep(2)
		except TclError:
			exit = True
			########################################
			#print("DONE!")
			logging.info('TclError CAUGHT. PROGRAM ENDING')
			########################################

	return;

main()
