from bs4 import BeautifulSoup
import pyttsx3

from pytz import timezone
from datetime import datetime
import requests
import time
import os
from collections import Counter

from model.trade_halt_record import TradeHaltRecord
from constant.halt_reason import HaltReason

def main():
    us_timezone = timezone('US/Eastern')
    parse_date_format = '%m/%d/%Y'
    parse_time_format = '%H:%M:%S'
    default_iteration_time = 60
    start_date = datetime.now(us_timezone).date()

    text_to_speech_engine = pyttsx3.init()
    session = requests.Session()

    text_to_speech_engine.setProperty('voice', text_to_speech_engine.getProperty('voices')[1].id)
    text_to_speech_engine.setProperty('rate', 150)
    text_to_speech_engine.setProperty('volume', 1)

    full_trade_halt_list = []
    ticker_list = []

    while True:
        iteration_start_time = time.time()
        feed_response = session.get('http://www.nasdaqtrader.com/rss.aspx?feed=tradehalts')
        feed_contents = feed_response.text
        soup = BeautifulSoup(feed_contents, 'lxml')
        xml_record_list = soup.find_all('item')

        pending_notificatioin_list = []

        for xml_record in xml_record_list:
            symbol = xml_record.find(TradeHaltRecord.SYMBOL).string
            company = xml_record.find(TradeHaltRecord.COMPANY).string
            reason = xml_record.find(TradeHaltRecord.REASON).string
            halt_date = xml_record.find(TradeHaltRecord.HALT_DATE).string
            halt_time = xml_record.find(TradeHaltRecord.HALT_TIME).string
            resumption_time = xml_record.find(TradeHaltRecord.RESUMPTION_TRADE_TIME).string

            trade_halt_record = TradeHaltRecord(symbol, company, reason, halt_date, halt_time, resumption_time)

            if (datetime.strptime(halt_date, parse_date_format).date() >= start_date and (trade_halt_record not in full_trade_halt_list)):
                ticker_list.append(symbol)
                ticker_to_max_occurrence_dict = Counter(ticker_list)
                trade_halt_record.occurrence = ticker_to_max_occurrence_dict.get(symbol) + 1

                full_trade_halt_list.append(trade_halt_record)
                pending_notificatioin_list.append(trade_halt_record)
        
        if len(pending_notificatioin_list) > 0:
            os.system('cls')

            for halt_record in full_trade_halt_list:
                halt_record.display()
            
            for notification in pending_notificatioin_list:
                reason = HaltReason(notification.reason) if (HaltReason.has_key(notification.reason)) else notification.reason
                text_to_speech_engine.say(f'{notification.symbol} Get Halted at {notification.halt_time}, Occurrence: {notification.occurrence} Times, Halt Reason: {reason}')

        refresh_time = time.time() - iteration_start_time

        if refresh_time >= default_iteration_time:
            continue
        else:
            time.sleep(default_iteration_time - refresh_time)

        text_to_speech_engine.runAndWait()

main()

