from colorama import Fore, Back

from datetime import datetime

from constant.halt_reason import HaltReason

class TradeHaltRecord:
    SYMBOL = 'ndaq:issuesymbol'
    COMPANY = 'ndaq:issuename'
    REASON = 'ndaq:reasoncode'
    HALT_DATE = 'ndaq:haltdate'
    HALT_TIME = 'ndaq:halttime'
    RESUMPTION_TRADE_TIME = 'ndaq:resumptiontradetime'

    def __init__(self, symbol, company, reason, 
                halt_date, halt_time, 
                resumption_time):
        self.__symbol = symbol
        self.__company = company
        self.__reason = reason
        self.__occurrence = 0
        self.__halt_date = halt_date
        self.__halt_time = halt_time
        self.__resumption_time = resumption_time
        self.__is_highlighted = False
    
    def __members(self):
        return (self.__symbol, self.__company, self.__reason,
                self.__halt_date, self.__halt_time,
                self.__resumption_time)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TradeHaltRecord):
            return self.__members() == other.__members()

    def __hash__(self) -> int:
        return hash(self.__members())

    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol):
        self.__symbol = symbol

    @property
    def company(self):
        return self.__company
    
    @company.setter
    def company(self, company):
        self.__company = company

    @property
    def reason(self):
        return self.__reason
    
    @reason.setter
    def reason(self, reason):
        self.__reason = reason

    @property
    def occurrence(self):
        return self.__occurrence
    
    @occurrence.setter
    def occurrence(self, occurrence):
        self.__occurrence = occurrence

    @property
    def halt_date(self):
        return self.__halt_date
    
    @halt_date.setter
    def halt_date(self, halt_date):
        self.__halt_date = halt_date

    @property
    def halt_time(self):
        return self.__halt_time
    
    @halt_time.setter
    def halt_time(self, halt_time):
        self.__halt_time = halt_time

    @property
    def __resumption_time(self):
        return self.____resumption_time
    
    @__resumption_time.setter
    def __resumption_time(self, __resumption_time):
        self.____resumption_time = __resumption_time

    @property
    def is_highlighted(self):
        return self.__is_highlighted
    
    @is_highlighted.setter
    def is_highlighted(self, is_highlighted):
        self.__is_highlighted = is_highlighted

    def display(self):
        display_resumption_time = self.__resumption_time if self.__resumption_time != None else 'Unknown'
        display_halt_date = datetime.strptime(self.__halt_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        display_reason = HaltReason(self.__reason) if (HaltReason.has_key(self.__reason)) else self.__reason
        highlight_style = Fore.YELLOW + Back.GREEN
        normal_style = Fore.WHITE + Back.BLACK

        if self.__is_highlighted:
            display_msg = f'{highlight_style}{self.__company} {self.__symbol}, {display_reason}, Halt Date Time: {display_halt_date} {self.__halt_time}, Resume Trade at {display_resumption_time}'
        else:
            display_msg = f'{normal_style}{self.__company} {self.__symbol}, {display_reason}, Halt Date Time: {display_halt_date} {self.__halt_time}, Resume Trade at {display_resumption_time}'

        print(display_msg)