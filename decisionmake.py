
class DecisionMake:
    def selectCardFromList(self, cardList:list):
        return cardList[0]
    def selectKoikoi(self):
        return False

class UserInterface(DecisionMake):
    def selectCardFromList(self, cardList:list):
        selectionDict = {}
        showStr = ""
        for i,card in enumerate(cardList):
            showStr += f"{i}: {card.to_str()}, "
            selectionDict[i] = card
        print(showStr)

        while True:
            try:
                val = input()
                val = int(val)
                selectedCard = selectionDict[val]  
            except:
                if val == "c":
                    break
                print("invalid value! (if you want to break game, press c)")
                continue
            break
           
        return selectedCard  
    
    def selectKoikoi(self):
        print(f"Koikoi?")
        print("0: koikoi, 1: end game")
        while True:
            try:
                val = input()
                isKoikoi = int(val)==0
                break
            except:
                if val == "c":
                    break                    
                print("invalid value! (if you want to break game, press c)")
                continue
        return isKoikoi
