#%%
from enum import Enum
import random

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
    KASU = 1
    TANN = 2
    TANE = 3
    HIKARI = 4

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

class TannYaku(Enum):
    AKATAN = set([Month.JANUARY,Month.FEBRUARY,Month.MARCH])
    AOTAN = set([Month.JUNE, Month.SEPTEMBER,Month.OCTOBER])

class Card:
    def __init__(self, month:Month, mark:Mark):
        self.month = month  # 月（1-12）
        self.mark = mark    # 種類
    def to_str(self):
        return f"{self.month.value}/{self.mark.name}"

class Deck:
    def __init__(self):
        self.cards = self.addAll()
        self.shuffle(self.cards)

    def isEmpty(self):
        return len(self.cards)==0
    
    def addAll(self):
        cards = []
        # カス一枚目設定
        for name, month in Month.__members__.items():  
            card = Card(month, Mark.KASU)
            cards.append(card)

        # カス二枚目設定
        for name, month in Month.__members__.items():  
            if month == Month.NOVEMBER:
                continue
            card = Card(month, Mark.KASU)
            cards.append(card)
        
        # カス三枚目設定
        cards.append(Card(Month.DECEMBER,Mark.KASU))

        # タン設定
        for name, month in Month.__members__.items():  
            if month in [Month.AUGUST,Month.DECEMBER]:
                continue
            card = Card(month, Mark.TANN)
            cards.append(card)        

        # タネ設定
        for name, month in Month.__members__.items():  
            if month in [Month.JANUARY,Month.MARCH,Month.DECEMBER]:
                continue
            card = Card(month, Mark.TANE)
            cards.append(card)       

        # 光設定
        for month in [Month.JANUARY, Month.MARCH, Month.AUGUST,Month.NOVEMBER,Month.DECEMBER]:
            card = Card(month, Mark.HIKARI)
            cards.append(card)   
        return cards

    def shuffle(self,cards):
        random.shuffle(cards)

    def drawCard(self):
        return self.cards.pop()

class Field:
    def __init__(self):
        self.cards = []
    
    def isIniFour(self):
        di = {}
        for card in self.cards:
            if card.month not in di:
                di[card.month]=0
            di[card.month] +=1
            if di[card.month]==4:
                return True
        return False

    def addCard(self,card):
        self.cards.append(card)

    def addCardFromPlayer(self,card:Card):
        candidates = []
        for fcard in self.cards:
            if fcard.month == card.month:
                candidates.append(fcard)
                continue

        if len(candidates)==0:
            self.addCard(card)
        if len(candidates)==1 or len(candidates)==3:
            for cand in candidates:
                self.removeCard(cand) 
        return candidates

    def removeCard(self,card:Card):
        self.cards.remove(card)
    
    def to_str(self):
        ret = ""
        for idx, card in enumerate(self.cards):
            ret += card.to_str() + " "
        return ret

class Player:
    def __init__(self):
        self.hand = []
        self.kasu = []
        self.tane = []
        self.tann = []
        self.hikari = []
        self.yaku = {}

    def isEmpty(self):
        return len(self.hand)==0

    def addCardToHand(self,card:Card):
        self.hand.append(card)
    
    def playCard(self, card:Card):
        self.hand.remove(card)
        return card
    
    def addCardFromField(self, cards:list):
        for card in cards:
            if card.mark == Mark.HIKARI:
                self.hikari.append(card)
            if card.mark == Mark.TANE:
                self.tane.append(card)
            if card.mark == Mark.TANN:
                self.tann.append(card)
            if card.mark == Mark.KASU:
                self.kasu.append(card)
    
    def validCards(self, field:Field):
        candidates = set([])
        for fcard in field.cards:
            for card in self.hand:
                if fcard.month==card.month:
                    candidates.add(card)
        return list(candidates)
    
    def isInitialYaku(self):
        di = {}
        for card in self.hand:
            if card.month not in di:
                di[card.month]=0
            di[card.month] +=1
            if di[card.month]==4:
                return Yaku.TESHI
        for month in di:
            if di[month]!=2:
                return None
        return Yaku.KUTTSUKI
    
    def isNewYaku(self,newYakus):
        if len(self.yaku)==0 and len(newYakus)==0:
            return False
        if len(self.yaku)==0:
            return True
        for yaku in self.yaku:
            if yaku in newYakus and self.yaku[yaku]!=newYakus[yaku]:
                return True
        if Yaku.SANKO in self.yaku:
            if Yaku.SHIKO in newYakus or Yaku.AMESHIKO in newYakus:
                return True
        if Yaku.SHIKO in self.yaku or Yaku.AMESHIKO in self.yaku:
            if Yaku.GOKO in newYakus:
                return True
        return False


    def isYaku(self):
        yakus = {}
        if len(self.kasu)>=10:
            yakus[Yaku.KASU] = len(self.kasu)
        if len(self.tann)>=5:
            yakus[Yaku.TANN] = len(self.tann)
        if len(self.tann)>=3:
            akaCount = 0
            aoCount = 0
            for card in self.tann:
                if card.month in TannYaku.AOTAN.value:
                    aoCount+=1
                if card.month in TannYaku.AKATAN.value:
                    akaCount+=1       
            if aoCount==3 and akaCount ==3:
                yakus[Yaku.BOOK] = 1
            elif aoCount==3:
                yakus[Yaku.AOTAN] = 1
            elif akaCount==3:
                yakus[Yaku.AKATAN] = 1
        if len(self.tane)>=5:
            yakus[Yaku.TANE] = len(self.tane)
        if len(self.hikari)==5:
            yakus[Yaku.GOKO] = 1
        
        if len(self.hikari)==4:
            isNov = False
            for card in self.hikari:
                if card.month==Month.NOVEMBER:
                    isNov = True
            if isNov:
                yakus[Yaku.AMESHIKO] = 1
            else:
                yakus[Yaku.SHIKO] = 1

        if len(self.hikari)==3:
            isNov = False
            for card in self.hikari:
                if card.month==Month.NOVEMBER:
                    isNov = True
            if not isNov:
                yakus[Yaku.SANKO] = 1
        return yakus
    
    def koikoi(self,yakus):
        self.yaku = yakus

    def to_str(self):
        ret = ""
        for idx, card in enumerate(self.hand):
            ret += card.to_str() + " "
        ret +="\n "
        ret +="kasu: "
        for idx, card in enumerate(self.kasu):
            ret += card.to_str() + " "
        ret +="\n "
        ret +="tann: "
        for idx, card in enumerate(self.tann):
            ret += card.to_str() + " "
        ret +="\n "
        ret +="tane: "
        for idx, card in enumerate(self.tane):
            ret += card.to_str() + " "
        ret +="\n "
        ret +="hikari: "
        for idx, card in enumerate(self.hikari):
            ret += card.to_str() + " "
        return ret


