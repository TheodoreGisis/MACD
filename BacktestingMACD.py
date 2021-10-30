import yfinance as yf
import matplotlib.pyplot as plt
import pandas 


class CalculateDmac:

    def __init__(self,dataframe):
        self.dataframe =dataframe
        self.buy=[]
        self.sell =[]

#CREATING THE LONG ,SHORT AND SIGNAL FOR THE STRADEGY
    def Dmac(self):
        self.dataframe['EMA12'] = self.dataframe.Close.ewm(span=12).mean()
        self.dataframe['EMA26'] = self.dataframe.Close.ewm(span=26).mean()
        self.dataframe['MACD'] = self.dataframe.EMA12 - df.EMA26
        self.dataframe['signal'] = self.dataframe.MACD.ewm(span=9).mean()
        return self.dataframe

#PLOTING THE MAC-SIGNAL 
    def plotDmac(self):
        df = self.Dmac()
        plt.plot(df.signal,label="SIGNAL",color="red")
        plt.plot(df.MACD, label="MACD",color="black")
        plt.legend()
        plt.show()

#PLOTING THE BUYS 
    def plot_the_buys(self):
        
        for i in range(2,len(self.dataframe)):
            if self.dataframe.MACD.iloc[i] > self.dataframe.signal.iloc[i] and self.dataframe.MACD.iloc[i-1] < self.dataframe.signal.iloc[i-1]:
                self.buy.append(i)
            if self.dataframe.MACD.iloc[i] < self.dataframe.signal.iloc[i] and self.dataframe.MACD.iloc[i-1] > self.dataframe.signal.iloc[i-1]:
                self.sell.append(i)
        plt.figure(figsize=(20,6))
        plt.scatter(self.dataframe.iloc[self.buy].index, self.dataframe.iloc[self.buy].Close,marker="^",color="green")
        plt.scatter(self.dataframe.iloc[self.sell].index ,self.dataframe.iloc[self.sell].Close,marker="v",color="red")
        plt.plot(self.dataframe.Close,label='TSL CLOSE')
        plt.legend()
        plt.show()
        return self.buy, self.sell

#WE BACKTESTING AND TAKE THE RESULT
    def BackTest(self):
        buy , sell = self.plot_the_buys()

        profits = []

        RealBuys = []
        RealSell =[]

        RealBuys =[i+1 for i in buy]
        RealSell = [i+1 for i in sell]

        BuyPrice = df.Open.iloc[RealBuys]
        SellPrice = df.Open.iloc[RealSell]

        if SellPrice.index[0] <BuyPrice.index[0]:

            SellPrice = SellPrice.drop(SellPrice.index[0])

        elif BuyPrice.index[-1] > SellPrice.index[-1]:

           BuyPrice = BuyPrice.drop(BuyPrice.index[-1])

        for i in range(len(SellPrice)):
            profits.append((SellPrice[i] - BuyPrice[i])/BuyPrice[i])
        total = sum(profits)/len(profits)
        print(total)
        
   
#MAIN
if __name__ == "__main__":
    df = yf.download("AAPL" , start ='2020-11-01')
    DMAC = CalculateDmac(df) 
    DMAC.BackTest()

