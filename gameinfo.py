from enum import Enum

class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class Mark(Enum):
    HIKARI = 1
    TANN = 2
    TANE = 3
    KASU = 4

class Yaku(Enum):
    KASU = 1
    TANN = 2
    TANE = 3
    HANAMI = 4
    TSUKIMI = 5
    AOTAN = 6
    AKATAN = 7
    INOSHIKA = 8
    SANKO = 9
    AMESHIKO = 10
    SHIKO = 11
    GOKO = 12
    BOOK = 13
    TESHI = 14
    KUTTSUKI = 15
    NOMI = 16

class TannYaku(Enum):
    AKATAN = set([Month.JANUARY,Month.FEBRUARY,Month.MARCH])
    AOTAN = set([Month.JUNE, Month.SEPTEMBER,Month.OCTOBER])

class TANEYaku(Enum):
    INOSHIKACHO = set([Month.JUNE,Month.JULY,Month.OCTOBER])

class Card:
    def __init__(self, month:Month, mark:Mark):
        self.month = month  # 月（1-12）
        self.mark = mark    # 種類

    def to_str(self):
        sp = ""
        if self.mark == Mark.TANE and self.month in TANEYaku.INOSHIKACHO.value:
            sp = "(i)"
        if self.mark == Mark.TANE and self.month == Month.SEPTEMBER:
            sp = "(k)"
        if self.mark == Mark.TANN and self.month in TannYaku.AKATAN.value:
            sp = "(r)"            
        if self.mark == Mark.TANN and self.month in TannYaku.AOTAN.value:
            sp = "(b)"
        if self.mark == Mark.HIKARI and self.month == Month.NOVEMBER:
            sp = "(n)"
        return f"{self.month.value}/{self.mark.name}{sp}"