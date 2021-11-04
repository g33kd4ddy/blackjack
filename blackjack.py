import random
#######################
# Script: blackjack.py
# Author: Brian Buchan
# Date:  4/18/2020
#######################
'''
Single deck black jack with one player
'''
import random
from IPython.display import clear_output 
class Card():
    def __init__(self,mycard=['0','0'], visible=True):
        self.mycard = mycard
        self.visible = visible
        self.cardnum = mycard[0]
        self.cardsuit = mycard[1]
    
    def __str__(self):
        outstr = ''
        x = [] 
        x = self.mycard
        for i in x:
            outstr += str(i)
        if self.visible:
            return outstr
        else:
            return 'XX'
    
    def value(self):
        card_val = 0
        try:
            card_val = int(self.mycard[0])
        except:
            if self.mycard[0] == 'A':
                card_val = 11
            else:
                card_val = 10
        return card_val
    
    def hide(self):
        self.visible = False
        
    def show(self):
        self.visible = True

### Deck Class ###
class Deck:
    def __init__(self):
        card = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
        suit = ('H','D','C','S')
        self.cardlist = []
        for c in card:
            for s in suit:
                self.cardlist.append([c,s])
        
    def __str__(self):
        outstr = ''
        x = [] 
        x = self.cardlist
        for i in x:
            outstr += str(i)
        return outstr
        
    def shuffle(self):
        random.shuffle(self.cardlist)
        print('Shuffling...')

    def cnt(self):
        return (len(self.cardlist))
        
    def deal(self):
        if self.cnt() == 0:
            print("Deck is out of cards...")
        else:
            card = self.cardlist.pop(0)
            return card
        
### Bankroll Class          
class Bankroll():
    def __init__(self, owner='house', balance=0.0):
        self.owner = owner
        self.balance = balance

    def __str__(self):
       return self.owner + "'s balance: " + str(self.balance)
        
    def bet(self, amount):
        self.balance -= amount
    
    def win(self, amount):
        self.balance += amount

### Hand Class
class Hand():
    def __init__(self): 
        self.cards = []
        self.hand_value = 0
        self.cnt = 0
        self.ace_cnt = 0
    
    def __str__(self):
        hstring = ''
        showem = True
        for i in self.cards:
            hstring += '|' + str(i)
            if not i.visible:
                showem = False
        if showem:
            hstring += '|  count:' + str(self.hand_value)
        else:
            hstring += '|'
        return hstring

    def receive(self, card):
        self.cards.append(card)
        self.hand_value += card.value()
        if card.cardnum == 'A':
            self.ace_cnt += 1
        if self.hand_value > 21 and self.ace_cnt > 0:
            self.hand_value -= 10
            self.ace_cnt -= 1
        
        self.cnt += 1
        
    def show(self):
        for i in self.cards:
            i.show()

if __name__ == '__main__':  
    # ######################
    ### Start Game
    # ######################

    # Initialize
    deck = Deck()
    deck.shuffle()  

    # Set player name and bankroll...
    name = input("Enter name: ")
    while True:
        try:
            val = int(input("What is your bankroll?: "))
            break
        except:
            print("Looks like you did not enter an integer!")

    player_bank = Bankroll(name, val )
    house_bank = Bankroll('House', 10000)

    game_on = True
    player_bet = 0

    # Start new round
    while game_on:
        clear_output()
        print('_________________________________________________________________')
        print(player_bank)
        print(house_bank)
        if deck.cnt() < 12:
            deck = Deck()
            deck.shuffle()
        if player_bank.balance == 0:
            print("You are broke..take a hike!")
            game_on = False
            break
        if house_bank.balance == 0:
            print("Congrats.. you broke the house!")
            game_on = False
            break
        while True:
            try:
                player_bet = int(input("Amount to bet? "))
                if player_bet <= player_bank.balance:
                    break
                else:
                    print('Insufficient funds... bet again')
            except:
                print("Looks like you did not enter an integer!")    
        # Deal new hands... 
        player_bank.bet(player_bet)
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.receive(Card(deck.deal()))
        # Dealer first card is down...
        dealer_hand.receive(Card(deck.deal(),False))
        player_hand.receive(Card(deck.deal()))
        dealer_hand.receive(Card(deck.deal()))
        print('Dealer: ' + str(dealer_hand))
        print('Player: ' + str(player_hand))
        player_turn = True
        game_over = False
      
        ### Start game play...
        # Check dealer blackjack...
        if dealer_hand.hand_value == 21 and player_hand.hand_value < 21:
            print('House Has Blackjack')
            dealer_hand.show()
            print('Dealer: ' + str(dealer_hand))
            house_bank.win(player_bet)
            game_over = True
            player_turn = False
        
        # Checker player blackjack...
        if player_hand.hand_value == 21:
            print('Black Jack!!!')
            player_bank.win(player_bet + (player_bet * 1.5))
            house_bank.bet(player_bet * 1.5)
            game_over = True 
            player_turn = False

        ### Player turn
        while player_turn:
            while True:
                move = input('Hit or Stay? < h or s >')
                if move.lower() in ['h', 's']:
                    break
                else:
                    print('Enter "h" to hit or "s" to stay.')
                
            if move.lower() == 's':
                player_turn = False
            else:
                player_hand.receive(Card(deck.deal()))
                print('Player: ' + str(player_hand))
                if player_hand.hand_value > 21:
                    print('Player busts!')
                    house_bank.win(player_bet)
                    game_over = True
                    player_turn = False
                    
        ### Dealer's turn
        ### Flip down card
        dealer_hand.show()

        while not game_over:
            print('Dealer: ' + str(dealer_hand))
            if dealer_hand.hand_value < 17:
                dealer_hand.receive(Card(deck.deal()))
                if dealer_hand.hand_value > 21:
                    print('Dealer: ' + str(dealer_hand))
                    print('Dealer busts!')
                    player_bank.win(player_bet + player_bet)
                    house_bank.bet(player_bet)            
                    game_over = True
            elif dealer_hand.hand_value == player_hand.hand_value:
                print('Push')
                player_bank.win(player_bet)
                game_over = True
            elif dealer_hand.hand_value < player_hand.hand_value:
                if player_hand.hand_value == 21:
                    if player_hand.cnt == 2:
                        print('Black Jack!!!')
                        player_bank.win(player_bet + (player_bet * 1.5))
                        house_bank.bet(player_bet * 1.5)
                        game_over = True 
                    else:
                        print('Player Wins!')
                        player_bank.win(player_bet + player_bet)
                        house_bank.bet(player_bet)
                        game_over = True              
                else:
                    print('Player Wins!')
                    player_bank.win(player_bet + player_bet)
                    house_bank.bet(player_bet)
                    game_over = True
            else:
                print('House Wins')
                house_bank.win(player_bet)
                game_over = True
        
        another_game = input('Play again? (Y/N)')
        if another_game.upper() == 'N':
            game_on = False