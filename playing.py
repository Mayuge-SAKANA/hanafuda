#%%

from cards_and_players import Deck,Player,Field

# initial card
deck = Deck()
field = Field()
player1 = Player()
player2 = Player()

fieldInitialNumber = 8
playerInitialNumber = 8

for i in range(fieldInitialNumber):
    card = deck.drawCard()
    field.addCard(card)

for i in range(playerInitialNumber):
    card = deck.drawCard()
    player1.addCardToHand(card)

for i in range(playerInitialNumber):
    card = deck.drawCard()
    player2.addCardToHand(card)

players = [player1,player2]

turn = 0
# start game
while not (player1.isEmpty() and player2.isEmpty()):
    for pIdx, player in enumerate(players):
        
        print(f"turn {turn}")
        print("player2: ",player2.to_str())
        print()
        print(field.to_str())
        print()
        print("player1: ",player1.to_str())
        print()
        
        turn+=1


        # here requires player selection of card
        card = player.playCard(player.hand[0])
        candidates = field.addCardFromPlayer(card)

        if len(candidates)==3 or len(candidates)==1:
            for cand in candidates:
                player.addCardFromField([card,*candidates])
        elif len(candidates)==2:
            # here requires player selection of card
            player.addCardFromField([card,candidates[0]])
            field.removeCard(candidates[1])
        yakulist = player.isYaku()
        if len(player.yaku)<=len(yakulist):
            isKoikoi = True
            if isKoikoi:
                # here requires player selection koikoi or not
                player.koikoi(yakulist)
            else:
                break

        







# %%
