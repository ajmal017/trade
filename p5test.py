import pandas as pd
import numpy as np
import requests
import io
from bs4 import BeautifulSoup
import time
import json
from p5 import *
##############################################################################
def get_stock_data(symbol):
    link_front = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol="
    link_end = "&illiquid=0&smeFlag=0&itpFlag=0"
    url = link_front + symbol + link_end
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup=BeautifulSoup(r.content,"lxml")
    resdic = json.loads(str(soup.find("div",{"id":"responseDiv"}).contents[0].strip()))
    ltp = float(resdic["data"][0]["lastPrice"].replace(",",""))
    day_open = float(resdic["data"][0]["open"].replace(",",""))
    day_high = float(resdic["data"][0]["dayHigh"].replace(",",""))
    day_low = float(resdic["data"][0]["dayLow"].replace(",",""))
    low_52 = float(resdic["data"][0]["low52"].replace(",",""))
    high_52 = float(resdic["data"][0]["high52"].replace(",",""))
    bq1 = 0 if resdic["data"][0]["buyQuantity1"] == "-" else int(resdic["data"][0]["buyQuantity1"].replace(",",""))
    bq2 = 0 if resdic["data"][0]["buyQuantity2"] == "-" else int(resdic["data"][0]["buyQuantity2"].replace(",",""))
    bq3 = 0 if resdic["data"][0]["buyQuantity3"] == "-" else int(resdic["data"][0]["buyQuantity3"].replace(",",""))
    bq4 = 0 if resdic["data"][0]["buyQuantity4"] == "-" else int(resdic["data"][0]["buyQuantity4"].replace(",",""))
    bq5 = 0 if resdic["data"][0]["buyQuantity5"] == "-" else int(resdic["data"][0]["buyQuantity5"].replace(",",""))
    bq = [bq1, bq2, bq3, bq4, bq5]
    sq1 = 0 if resdic["data"][0]["sellQuantity1"] == "-" else int(resdic["data"][0]["sellQuantity1"].replace(",",""))
    sq2 = 0 if resdic["data"][0]["sellQuantity2"] == "-" else int(resdic["data"][0]["sellQuantity2"].replace(",",""))
    sq3 = 0 if resdic["data"][0]["sellQuantity3"] == "-" else int(resdic["data"][0]["sellQuantity3"].replace(",",""))
    sq4 = 0 if resdic["data"][0]["sellQuantity4"] == "-" else int(resdic["data"][0]["sellQuantity4"].replace(",",""))
    sq5 = 0 if resdic["data"][0]["sellQuantity5"] == "-" else int(resdic["data"][0]["sellQuantity5"].replace(",",""))
    sq = [sq1, sq2, sq3, sq4, sq5]
    bp1 = 0 if resdic["data"][0]["buyPrice1"] == "-" else float(resdic["data"][0]["buyPrice1"].replace(",",""))
    bp2 = 0 if resdic["data"][0]["buyPrice2"] == "-" else float(resdic["data"][0]["buyPrice2"].replace(",",""))
    bp3 = 0 if resdic["data"][0]["buyPrice3"] == "-" else float(resdic["data"][0]["buyPrice3"].replace(",",""))
    bp4 = 0 if resdic["data"][0]["buyPrice4"] == "-" else float(resdic["data"][0]["buyPrice4"].replace(",",""))
    bp5 = 0 if resdic["data"][0]["buyPrice5"] == "-" else float(resdic["data"][0]["buyPrice5"].replace(",",""))
    bp = np.array([bp1, bp2, bp3, bp4, bp5])
    sp1 = 0 if resdic["data"][0]["sellPrice1"] == "-" else float(resdic["data"][0]["sellPrice1"].replace(",",""))
    sp2 = 0 if resdic["data"][0]["sellPrice2"] == "-" else float(resdic["data"][0]["sellPrice2"].replace(",",""))
    sp3 = 0 if resdic["data"][0]["sellPrice3"] == "-" else float(resdic["data"][0]["sellPrice3"].replace(",",""))
    sp4 = 0 if resdic["data"][0]["sellPrice4"] == "-" else float(resdic["data"][0]["sellPrice4"].replace(",",""))
    sp5 = 0 if resdic["data"][0]["sellPrice5"] == "-" else float(resdic["data"][0]["sellPrice5"].replace(",",""))
    sp = np.array([sp1, sp2, sp3, sp4, sp5])
    updatetime = pd.to_datetime(resdic["lastUpdateTime"])
    retrieve_time = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S"))
    name = resdic["data"][0]["companyName"]
    tdic = {
        "TIME":retrieve_time,"STOCK":symbol.upper(),"LTP":ltp,
        "OPEN":day_open,"HIGH":day_high,"LOW":day_low,
        "LOW52":low_52,"HIGH52":high_52,
        "OQ1":sq1,"OQ2":sq2,"OQ3":sq3,"OQ4":sq4,"OQ5":sq5,
        "OP1":sp1,"OP2":sp2,"OP3":sp3,"OP4":sp4,"OP5":sp5,
        "BP1":bp1,"BP2":bp2,"BP3":bp3,"BP4":bp4,"BP5":bp5,
        "BQ1":bq1,"BQ2":bq2,"BQ3":bq3,"BQ4":bq4,"BQ5":bq5,
    }
    print(resdic)
    return(tdic)
################################################################################
class Candle:
    def __init__(self, o, h, l, c, low52, high52):
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        if c >= o:
            self.can_col =  [0,102,51]
            self.rec_x1 = np.interp(c, xp =[l-25,h+25], fp=[600,100] )
            self.can_height = np.interp(o, xp =[l-25,h+25], fp=[600,100] ) - np.interp(c, xp =[l-25,h+25], fp=[600,100] )
        else:
            self.can_col =  [153,0,0]
            self.rec_x1 = np.interp(o, xp =[l-25,h+25], fp=[600,100] )
            self.can_height = np.interp(c, xp =[l-25,h+25], fp=[600,100] ) - np.interp(o, xp =[l-25,h+25], fp=[600,100] )
        self.us_t = np.interp(h, xp =[l-25,h+25], fp=[600,100] )
        self.us_b = self.rec_x1
        self.ls_t = self.rec_x1 + self.can_height
        self.ls_b = np.interp(l, xp =[l-25,h+25], fp=[600,100] )



def setup():
    size(700,700)
    no_stroke()

def draw():
    for i in range(10):
        f = get_stock_data("INFY")
        c1 = Candle(f["OPEN"],f["HIGH"],f["LOW"],f["LTP"],f["LOW52"],f["HIGH52"])
        ccol = c1.can_col
        rec_x1 = c1.rec_x1
        can_height = c1.can_height
        us_t = c1.us_t
        us_b = c1.us_b
        ls_t = c1.ls_t
        ls_b = c1.ls_b
        background(204,229,255)
        no_stroke()
        fill(ccol[0],ccol[1],ccol[2])
        rect((100,rec_x1),15,can_height)
        stroke(ccol[0],ccol[1],ccol[2])
        line((108, us_t), (108, us_b))
        line((108, ls_t), (108, ls_b))
        time.sleep(1)

if __name__ == '__main__':
    run()
