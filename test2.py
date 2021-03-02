# Example connection to Trader Workstation (TWS) or IB Gateway (IBG)
from ib_insync import *
from time import sleep

from ib_insync import *
from os import listdir, remove
from time import sleep
import pickle
from helper_functions import *

# Don't forget to open TWS or IBG and sign into a paper account!
# Also don't forget to allow API connections in Global Configuration > API Settings.

# For TWS Paper account, default port is 7497
# For IBG Paper account, default port is 4002
port = 7497
# choose a client id:
client_id = 8923

# Create an IB app; i.e., an instance of the IB() class from the ib_insync package
ib = IB()
# Connect your app to a running instance of IBG or TWS
ib.connect(host='127.0.0.1', port=port, clientId=client_id)

# Make sure you're connected -- stay in this while loop until ib.isConnected() is True.
while not ib.isConnected():
    sleep(.01)

# If connected, script exits the while loop and prints a success message
print('Connection Successful!')

if 'currency_pair.txt' in listdir():
    # Code goes here...
    with open('currency_pair.txt', 'r') as f:
        curr = f.read()
    #remove('currency_pair.txt')
    contract = Forex(curr)
    bars = ib.reqHistoricalData(
        contract,  # <<- pass in your contract object here
        endDateTime='', durationStr='30 D', barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)
    df = util.df(bars)
    #print(df)
    df.to_csv('currency_pair_history.csv')

# Request current time
current_time = ib.reqCurrentTime()

# Print current time
print('Current time is: {}'.format(current_time))

# Close IB connection
ib.disconnect()
