
#importing the libraris
import ta
from BinanceFuturesPy.futurespy import Client
import pandas as pd
from BinanceFuturesPy.futurespy import MarketData
from binance.client import Client as ClientReal

#Here put your api and secret key that you have created in Binance
api_key=" "
secret_key=" "

#select the symbol to make exchange
SYMBOL = "BTCUSDT"




class Bot:

    def __init__(self,qnt):
        self.open_position=False
        self.quantity =qnt
        
#This function returns a dataframe with all the necessary informations about klines
    def get_data(self):
        df= pd.DataFrame(Data.candles_data())
        df = df.iloc[:,:6]
        df.columns=['Time','Open','High','Low','Close','Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index,unit='ms')
        df = df.astype(float)   
        return df

#Function that place an order
    def make_an_order(self):
        buy_an_order = client.new_order(symbol=SYMBOL,side='BUY',orderType='MARKET',quantity=self.quantity)
        print(buy_an_order)
        ID= int(buy_an_order.get('orderId'))
        return ID

#Function that sell an order
    def delete_an_order(self):
        cancel_an_order=client.new_order(symbol=SYMBOL,side='SELL',orderType='MARKET',quantity=self.quantity)
        print(cancel_an_order)
        return cancel_an_order

#Implementig the strategy using the ta library
    def trading_strategy(self):
        while True:
            df = self.get_data()
            if self.open_position == False:
                if ta.trend.macd_diff(df.Close).iloc[-1] > 0 and  ta.trend.macd_diff(df.Close).iloc[-2] < 0:
                    print("SELL-SELL-SELL")
                    self.make_an_order()
                    self.open_position = True
                    break
        if self.open_position == True:
            while True:
                df= self.get_data()
                if ta.trend.macd_diff(df.Close).iloc[-1] < 0 and  ta.trend.macd_diff(df.Close).iloc[-2] > 0:
                    print("BUY--BUY--BUY")
                    buy=self.delete_an_order()
                    self.open_position = False
                    break



if __name__ == '__main__':

    #Check if you want to trade in the binancetestnet enviroment 
    Is_Testnet_Or_No = input("Do you want to trade is BinanceTestnet environment Y-N?\n")
    if Is_Testnet_Or_No == 'Y' or Is_Testnet_Or_No =='y':
        testnetenvironment= True
    elif Is_Testnet_Or_No == 'N' or Is_Testnet_Or_No =='n':
        testnetenvironment =False
    else:
        print("Wrong Try Again!")
        testnetenvironment =None

    #Taking the quantity to make the trade
    Quantity = input("Please enter the quantity!")

    #Initialize the API Client
    client = Client(api_key, secret_key, testnet=testnetenvironment)

    #Initialize the Data 
    Data = MarketData(api_key,testnet=testnetenvironment,symbol=SYMBOL,interval="1m")

    bot = Bot(Quantity)
    while True:
       bot.trading_strategy()
 