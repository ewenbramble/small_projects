# Simple blackjack text game, single player vs computer dealer
# Written by Ewen Bramble in 2020 as an OOP exercise

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}

class Card:
    """Class representing a playing card object"""
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    """Class representing a deck of card object"""
    
    def __init__(self):
        
        self.all_cards = []

        # Generate a deck, each suit contains all ranks
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
                
    def shuffle(self):
        """Method shuffles deck"""
        random.shuffle(self.all_cards)
        
    def deal_card(self):
        """Method deals a single card"""
        return self.all_cards.pop()

class Hand:
    """Class representing a player hand"""
    
    def __init__(self, name):
        self.name = name
        self.hand = [] # Player hand empty initially
        
    def add_card(self, new_card):
        """Method to add a card to player hand"""
        self.hand.append(new_card)
    
    def __str__(self):
        return self.name

# GAME FUNCTIONS
def starting_balance():
    """Function to set initial balance"""
    global balance
    while True: 
        balance = input("How much $ have you brought to the table? $")
        # Check if numeric
        if balance.isnumeric() == False:
            print("Must be a number!")
        else:
            break
    balance = int(balance)
    return balance
    
def show_balance():
    """Function to show balance during game"""
    print("You have ${} to bet".format(balance))

def bet():
    """Functon to set bet amount"""
    global bet_amount
    while True:        
        bet_amount = input("How much would you like to bet on this game? $")
        # Check if numeric
        if bet_amount.isnumeric == False:
            print("Must be a number!")
        elif int(bet_amount) > balance:
            print("Sorry, you don't have that much left")
        else:
            print("You are betting ${}".format(bet_amount))
            break
    bet_amount = int(bet_amount)
    return bet_amount
    
def win(amount):
    """Function to add win to balance"""
    global balance
    balance += 2*amount

def lose(amount):
    """Function to subtract loss from balance"""
    global balance
    balance -= amount
    
def balance_check():
    """Function to check if balance is not zero"""
    if balance > 0:
        return True
    else:
        return False

def deal_two(player_name):
    """Function to deal two cards to each player"""
    for i in range(2):
        player_name.hand.append(deck.deal_card())
        
def hand_value(player_name):
    """Function that returns the value of a players hand"""
    value = 0
    # add the value of all cards except any aces to value in first loop
    for i in range(len(player_name.hand)):
        if player_name.hand[i].rank != 'Ace':
            value += player_name.hand[i].value
        else:
            pass
    # add value of any aces - 1 or 11 depending on total without aces
    for i in range(len(player_name.hand)):
        if player_name.hand[i].rank == 'Ace':
            if value <= 10:
                value += 11
            else:
                value += 1
    return value

def hit_question():
    """ Asks if player wants to hit, checks if valid response """
    while True:
        question = input('Would you like to hit? (Y/N): ')
        if question.upper() not in ['Y', 'N']:
            print("Invalid response")
        else:
                break
    if question.upper() == 'Y':
        return True
    else:
        return False
    

def hit(player_name):
    """ Deals a card for deck class instance to player instance, prints new card and value """
    player_name.hand.append(deck.deal_card())
    print("New card for {}: {}".format(player_name, player_name.hand[-1]))
    print("{}'s current hand value: {}".format(player_name, hand_value(player_name)))
    
def play_again():
    """ Asks if play again, returns True if player wants to play again """
    # ask, check response is valid
    while True:
        play_again = input("Would you like to play again? (Y/N)")
        if play_again.upper() not in ['Y', 'N']:
            print("Invalid response")
        else:
                break
    if play_again.upper() == 'Y':
        return True
    else:
        return False
    
def reset_hands():
    """ Function to clear each hand before dealing in each round """
    player.hand = []
    dealer.hand = []

# GAMEPLAY
# Initialise Game
from IPython.display import clear_output
deck = Deck()
dealer = Hand('Dealer')
player = Hand('Player')
game_on = True


print("Welcome to Blackjack!")

starting_balance() # Initial amount

while game_on:
    clear_output()
    show_balance()
    player_turn = True
    dealer_turn = True

    # Set up game
    # Shuffle Deck
    deck.shuffle()
    
    # Empty hands for both players
    reset_hands()

    # Deal two cards to each player
    deal_two(dealer)
    deal_two(player)
    
    # Take bet (returns bet_amount)
    bet()
    
    # Show one of dealer's cards, both player's cards
    print("\nDealer's hand: {} and *******".format(dealer.hand[0]))
    print("Your hand: {} and {}\n".format(player.hand[0], player.hand[1]))
    
    # Player's turn
    while player_turn:
        # ask if hit, if no end turn
        if hit_question() == False:
            print("Player stands")
            print("Player's final hand value: {}".format(hand_value(player)))
            player_turn = False
            break
        # hit
        hit(player)
        # check hand value
        if hand_value(player) > 21:
            lose(bet_amount)
            print("Bust! Dealer wins")
            player_turn = False
            dealer_turn = False
        else:
            pass
        
    # Dealer's turn
    if dealer_turn:    
        print("\nDealer's turn!")
        print("Dealer's hand: {} and {}\n".format(dealer.hand[0], dealer.hand[1]))
    while dealer_turn:
        # hit if hand_value 16 or under
        if hand_value(dealer) <= 16:
            hit(dealer)
            # check hand value
            if hand_value(dealer) > 21:
                print("Dealer bust! You win!")
                win(bet_amount)
                dealer_turn = False
            else:
                pass
        else:
            print("Dealer stands")
            print("Dealer's final hand value: {}".format(hand_value(dealer)))
            dealer_turn = False
            
    # If both turns complete without bust, game still on, check winner
    if hand_value(player) <= 21 and hand_value(dealer) <=21:
        if hand_value(player) > hand_value(dealer):
            print("\nYou win! ${} added to balance".format(bet_amount*2))
            win(bet_amount)
        elif hand_value(player) < hand_value(dealer):
            lose(bet_amount)
            print("\nDealer wins. New balance ${}".format(balance))
        else:
            print("Draw!")
    
    # Check if player has remaining funds after round
    if balance_check():
        if play_again() == False:
            print("\nThanks for playing!")
            game_on = False
        else:
            pass
    else:
        print("\nYou are out of cash! Game over")
        game_on = False
