#%%
import random
from gameinfo import Month, Mark, TANEYaku, TannYaku, Yaku, Card
from decisionmake import DecisionMake, UserInterface

class Deck:
    def __init__(self,seed = 0):
        self.cards = self.addAll()
        self.shuffle(seed)
        self.seed = seed

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

    def shuffle(self,seed):
        random.seed(seed)
        random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()

    def to_str(self):
        ret = ""
        for card in self.cards:
            ret += card.to_str() +" "
        return ret


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

    def sortCards(self):
        self.cards.sort(key=lambda card: (card.month.value, card.mark.value ))

    def addCard(self,card):
        self.cards.append(card)
        self.sortCards()       

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
        self.sortCards()
        return candidates

    def removeCard(self,card:Card):
        self.cards.remove(card)
    
    def to_str(self):
        ret = ""
        for idx, card in enumerate(self.cards):
            ret += card.to_str() + " "
        return ret

class Player:
    def __init__(self,playerName:str = "",isAuto:bool = True):
        self.playerName = playerName
        self.isAuto = isAuto
        self.hand = []
        self.kasu = []
        self.tane = []
        self.tann = []
        self.hikari = []
        self.yaku = {}
        self.DecisionMaiking = None
        if not isAuto:
            self.DecisionMaiking = UserInterface()
        else:
            self.DecisionMaiking = DecisionMake()

    def isEmpty(self):
        return len(self.hand)==0

    def addCardToHand(self,card:Card):
        self.hand.append(card)
        self.hand.sort(key=lambda card: (card.month.value, card.mark.value ))
    
    def playCard(self, card:Card):
        self.hand.remove(card)
        return card
    
    def addCardFromField(self, cards:list):
        for card in cards:
            targetlist = []
            if card.mark == Mark.HIKARI:
                targetlist = self.hikari
            if card.mark == Mark.TANE:
                targetlist = self.tane
            if card.mark == Mark.TANN:
                targetlist = self.tann
            if card.mark == Mark.KASU:
                targetlist = self.kasu
            targetlist.append(card)
            targetlist.sort(key=lambda card: (card.month.value, card.mark.value ))
   
    def validCards(self, field:Field):
        candidates = set([])
        for fcard in field.cards:
            for card in self.hand:
                if fcard.month==card.month:
                    candidates.add(card)
        return list(candidates)
    
    def selectCardFromList(self, cardList:list):
        selectedCard = None
        print(f"{self.playerName} select")
        selectedCard = self.DecisionMaiking.selectCardFromList(cardList)
        print(f"selected {selectedCard.to_str()}")
        return selectedCard
    
    def selectKoikoi(self,yakus:dict):
        isKoikoi = False
        if len(self.hand)==0:
            return isKoikoi
        isKoikoi = self.DecisionMaiking.selectKoikoi()

        if isKoikoi:
            self.yaku = yakus
        return isKoikoi

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

class YakuManager:         
    def __init__(self,field:Field=None,deck:Deck=None):
        self.field = field
        self.deck = deck
        self.YakuPointDict = {
            Yaku.KASU : 1,
            Yaku.TANN : 1,
            Yaku.TANE : 1,
            Yaku.HANAMI : 5,
            Yaku.TSUKIMI : 5,
            Yaku.AOTAN : 6,
            Yaku.AKATAN : 6,
            Yaku.INOSHIKA : 6,
            Yaku.SANKO : 5,
            Yaku.AMESHIKO : 7,
            Yaku.SHIKO : 8,
            Yaku.GOKO : 10,
            Yaku.BOOK : 12,
            Yaku.TESHI : 6,
            Yaku.KUTTSUKI : 6,
            Yaku.NOMI : 10,
        }

    def getCardsList(self,player:Player, isBlind:bool = True):
        ret = []
        if not isBlind:
            for card in player.hand:
                ret.append(card)
        for card in player.kasu:
            ret.append(card)
        for card in player.tane:
            ret.append(card)            
        for card in player.tane:
            ret.append(card)  
        return ret

    def yakuProb(self,player:Player,enemy:Player,isBlind:bool = True):
        kasuTotal = 24
        tanTotal = 10
        taneTotal = 10
        playerYaku, playerYakuMax = self.getCurYakuCards(player)
        enemyYaku, enemyYakuMax = self.getCurYakuCards(enemy)
        reqDict = {}
        for yaku in playerYaku:
            val = 0
            val = -enemyYaku[yaku] - playerYaku[yaku]
            if yaku is Yaku.KASU:
                val += kasuTotal
            elif yaku is Yaku.TANN:
                val += tanTotal
            elif yaku is Yaku.TANE:
                val += taneTotal
            else:
                val += playerYakuMax[yaku]
            

            reqDict[yaku] = val
        return reqDict



    def getCurYakuCards(self,player:Player):
        aotn = 0
        aktn = 0
        for card in player.tann:
            if card.month in TannYaku.AOTAN.value:
                aotn+=1
            if card.month in TannYaku.AKATAN.value:
                aktn+=1    
        inoshika = 0
        kiku = 0
        for card in player.tane:
            if card.month in TANEYaku.INOSHIKACHO.value:
                inoshika +=1
            if card.month is Month.SEPTEMBER:
                kiku = 1
        hikari11 = 0
        sakura = 0
        tsuki = 0
        for card in player.hikari:
            if card.month == Month.NOVEMBER:
                hikari11 = 1
            if card.month == Month.MARCH:
                sakura = 1
            if card.month == Month.AUGUST:
                tsuki = 1
        hikari = len(player.hikari)-hikari11

        kasu = len(player.kasu)
        tann = len(player.tann)
        tane = len(player.tane)


        yakuNum =  {
                    Yaku.KASU : min(24, max(kasu+1,10)),
                    Yaku.TANN : min(10, max(tann+1,5)),
                    Yaku.TANE : min(10,max(tane+1,5)),
                    Yaku.AOTAN : 3,
                    Yaku.AKATAN : 3,
                    Yaku.BOOK : 6,
                    Yaku.INOSHIKA : 3,
                    Yaku.SANKO : 3,
                    Yaku.AMESHIKO : 4,
                    Yaku.SHIKO : 4,
                    Yaku.GOKO : 5,
                    Yaku.HANAMI : 2,
                    Yaku.TSUKIMI : 2,
                    Yaku.NOMI : 3,
                }

        myDict = {
                    Yaku.KASU : min(kasu,yakuNum[Yaku.KASU]),
                    Yaku.TANN : min(tann,yakuNum[Yaku.TANN]),
                    Yaku.TANE : min(tane,yakuNum[Yaku.TANE]),
                    Yaku.AOTAN : aotn,
                    Yaku.AKATAN : aktn,
                    Yaku.BOOK : aotn+aktn,
                    Yaku.INOSHIKA : inoshika,
                    Yaku.SANKO : min(3,hikari),
                    Yaku.AMESHIKO : min(hikari,3)+hikari11,
                    Yaku.SHIKO : min(hikari,4),
                    Yaku.GOKO : hikari+hikari11,
                    Yaku.HANAMI : kiku+sakura,
                    Yaku.TSUKIMI : kiku+tsuki,
                    Yaku.NOMI : kiku+tsuki+sakura,
            }
        
        return  myDict,yakuNum
        

        


        

    


    def isInitialYaku(self,player:Player):
        di = {}
        for card in player.hand:
            if card.month not in di:
                di[card.month]=0
            di[card.month] +=1
            if di[card.month]==4:
                return Yaku.TESHI
        for month in di:
            if di[month]!=2:
                return None
        return Yaku.KUTTSUKI
    
    def isNewYaku(self,newYakus:dict,player:Player):
        if len(player.yaku)==0 and len(newYakus)==0:
            return False
        if len(player.yaku)==0:
            return True
        for yaku in player.yaku:
            if yaku in newYakus and player.yaku[yaku]!=newYakus[yaku]:
                return True
        if Yaku.SANKO in player.yaku:
            if Yaku.SHIKO in newYakus or Yaku.AMESHIKO in newYakus:
                return True
        if Yaku.SHIKO in player.yaku or Yaku.AMESHIKO in player.yaku:
            if Yaku.GOKO in newYakus:
                return True
        if (Yaku.HANAMI in player.yaku or Yaku.TSUKIMI in player.yaku) and Yaku.NOMI in newYakus:
            return True
        return False

    def isYaku(self,player:Player):
        yakus = {}
        isKiku = False
        if len(player.kasu)>=10:
            yakus[Yaku.KASU] = len(player.kasu)-9
        if len(player.tann)>=5:
            yakus[Yaku.TANN] = len(player.tann)-4
        if len(player.tann)>=3:
            akaCount = 0
            aoCount = 0
            for card in player.tann:
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
            elif len(player.tann)>=5:
                yakus[Yaku.TANN] = len(player.tann)-4
        if len(player.tane)>=5:
            yakus[Yaku.TANE] = len(player.tane)-4
        if len(player.tane)>=1:
            inoCount = 0
            for card in player.tane:
                if card.month == Month.SEPTEMBER:
                    isKiku = True
                if card.month in TANEYaku.INOSHIKACHO.value:
                    inoCount+=1
            if inoCount==3:
                yakus[Yaku.INOSHIKA] = 1
 
        if len(player.hikari)==5:
            yakus[Yaku.GOKO] = 1
            if Yaku.SHIKO in yakus:
                yakus.pop(Yaku.SHIKO)
            if Yaku.AMESHIKO in yakus:
                yakus.pop(Yaku.AMESHIKO)

        if len(player.hikari)==4:
            isNov = False
            for card in player.hikari:
                if card.month==Month.NOVEMBER:
                    isNov = True
            if isNov:
                yakus[Yaku.AMESHIKO] = 1
            else:
                yakus[Yaku.SHIKO] = 1
            if Yaku.SANKO in yakus:
                yakus.pop(Yaku.SANKO)

        if len(player.hikari)==3:
            isNov = False
            for card in player.hikari:
                if card.month==Month.NOVEMBER:
                    isNov = True
            if not isNov:
                yakus[Yaku.SANKO] = 1
        
        if isKiku and len(player.hikari)>0:
            for card in player.hikari:
                if card.month == Month.AUGUST:
                    yakus[Yaku.TSUKIMI] = 1
                if card.month == Month.MARCH:
                    yakus[Yaku.HANAMI] = 1
            if Yaku.HANAMI in yakus and Yaku.TSUKIMI in yakus:
                yakus[Yaku.NOMI] = 1
                yakus.pop(Yaku.HANAMI)
                yakus.pop(Yaku.TSUKIMI)      
        return yakus            






# %%
