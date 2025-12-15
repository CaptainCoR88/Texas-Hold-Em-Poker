import csv
from random import choice

class Deck:
    def __init__(self):
        self.__suits = []
        self._cards = []

    def shuffle_cards(self):
        array1=[]
        array2=[]
        for x in range(self.count_cards()):
            if x%2 == 0:
                array1.append(self.get_cards()[x])
            else:
                array2.append(self.get_cards()[x])
        self._cards=[]
        for x in range(26):
            card=choice(array1)
            array1.remove(card)
            self.add_card(card)
            card=choice(array2)
            array2.remove(card)
            self.add_card(card)

    def add_card(self,card):
        self._cards.append(card)

    def add_suit(self,suit):
        self.__suits.append(suit)
        for card in suit.get_cards():
            self.add_card(card)

    def reset_deck(self):
        self._cards=[]
        for suit in self.__suits:
            for card in suit.get_cards():
                self.add_card(card)

    def deal_card(self):
        card=self._cards[0]
        self._cards.remove(card)
        return card

    def count_cards(self):
        return len(self._cards)

    def get_cards(self):
        return self._cards

    def __repr__(self):
        string=''
        for card in self._cards:
            string+=str(card.value)+' of '+card.suit+', '
        return string

class Suit(Deck):
    super(Deck)
    def __init__(self, suit):
        super().__init__()
        self.name=suit

class Card:
    def __init__(self,suit,value):
        self.suit=suit
        self.value=value

    def get_numeric(self):
        if self.value in ['J','Q','K']:
            num=10
        elif self.value == 'A':
            num=11
        else:
            num = int(self.value)
        return num

    def __repr__(self):
        string=str(self.value),'of',self.suit
        return string

class Player:
    def __init__(self):
        self.order={'2':0,
                    '3':1,
                    '4':2,
                    '5':3,
                    '6':4,
                    '7':5,
                    '8':6,
                    '9':7,
                    '10':8,
                    'J':9,
                    'Q':10,
                    'K':11,
                    'A':12}
        self.scores={
        'high card':1,
        'pair':2,
        'two pair':3,
        'three of a kind':4,
        'straight':5,
        'flush':6,
        'full house':7,
        'four of a kind':8,
        'straight flush':9,
        'royal flush':10
        }
        self.cards=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.score=0
        self.hand=[]
        self.suit=[]
        self.value=[]

    def give_card(self,card):
        self.hand.append(card)
        self.sort_hand()
        self.suit = []
        self.value = []
        for y in range(self.card_count()):
            self.suit.append(self.hand[y].suit)
            self.value.append(self.hand[y].value)

    def reset_player(self):
        self.hand=[]
        self.suit=[]
        self.value=[]
        self.cards=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.score=0

    def sort_hand(self):
        num1 = self.card_count()
        count = 1
        swap = 1
        while swap > 0:
            swap = 0
            num = num1 - count
            for x in range(num):
                if self.order[self.hand[x].value] > self.order[self.hand[x+1].value]:
                    temp = self.hand[x]
                    self.hand[x] = self.hand[(x + 1)]
                    self.hand[(x + 1)] = temp
                    swap += 1
            count += 1

    def card_count(self):
        return len(self.hand)

    def display_hand(self):
        string=''
        for card in self.hand:
            string+=str(card.value)+' of '+card.suit+', '
        return string

    def hand_type(self):
        count=0
        hand='high card'
        num=self.card_count()-1
        valid=True
        for x in self.cards:
            if x > 0:
                valid=False
        if valid:
            for x in range(num+1):
                self.cards[self.order[self.value[x]]]+=1
        for value in self.cards:
            if value == 2:
                count+=1
        if count == 1:
            hand='pair'
        if count >= 2:
            hand='two pair'
        count=0
        for value in self.cards:
            if value == 3:
                count+=1
        if count == 1:
            hand='three of a kind'
        count=0
        count1=0
        for value in self.cards:
            if value == 2:
                count+=1
            elif value == 3:
                count1+=1
        if count >= 1 and count1 >= 1:
            hand='full house'
        elif count1 == 2:
            hand='full house'
        count=0
        for value in self.cards:
            if value == 4:
                count+=1
        if count == 1:
            hand='four of a kind'
        temperhand=''
        Hearts=0
        Diamonds=0
        Clubs=0
        Spades=0
        for suit in self.suit:
            if suit == 'Hearts':
                Hearts+=1
            elif suit == 'Diamonds':
                Diamonds+=1
            elif suit == 'Clubs':
                Clubs+=1
            else:
                Spades+=1
        if Hearts == 5 or Diamonds == 5 or Clubs == 5 or Spades == 5:
            temperhand='flush'
        valid=False
        temphand=''
        for x in range(num-3):
            count=0
            for y in range(4):
                if self.order[self.value[x+y]] == self.order[self.value[x+y+1]] - 1:
                    count+=1
            if count == 4:
                valid=True
                length=x
        if valid:
            temphand='straight'
            suits=self.suit[length:5+length]
            values=self.value[length:5+length]
        if temphand == 'straight':
            Hearts = 0
            Diamonds = 0
            Clubs = 0
            Spades = 0
            for suit in suits:
                if suit == 'Hearts':
                    Hearts += 1
                elif suit == 'Diamonds':
                    Diamonds += 1
                elif suit == 'Clubs':
                    Clubs += 1
                else:
                    Spades += 1
            if Hearts == 5 or Diamonds == 5 or Clubs == 5 or Spades == 5:
                hand='straight flush'
            if hand == 'straight flush' and values[4] == 'A':
                hand='royal flush'
        if hand not in ['four of a kind','straight flush','royal flush']:
            if temperhand == 'flush':
                hand='flush'
            elif temphand == 'straight':
                hand='straight'

        return hand

    def set_score(self):
        self.score=self.scores[self.hand_type()]

    def hand_score(self):
        hand=self.hand_type()
        score=0
        if hand == 'high card':
            score = self.order[self.value[self.card_count()-1]]
        if hand == 'pair':
            for x in range(13):
                if self.cards[x] == 2:
                    score=x
        if hand == 'two pair':
            for x in range(13):
                if self.cards[x] == 2:
                    score=x
        if hand == 'three of a kind':
            for x in range(13):
                if self.cards[x] == 3:
                    score=x
        if hand == 'full house':
            temp=[]
            for x in range(13):
                if self.cards[12-x] == 3:
                    temp.append(12-x)
            if len(temp) == 2:
                if temp[0] > temp[1]:
                    score=temp[0]
                else:
                    score=temp[1]
                length=2
            else:
                score=temp[0]
                length=2
            if length == 2:
                count=0
                for x in range(13):
                    if self.cards[12-x] == 3:
                        if count == 0:
                            count+=1
                        else:
                            score+=12-x
            else:
                for x in range(13):
                    if 3 > self.cards[12-x] > 0:
                        score+=12-x
        if hand == 'four of a kind':
            for x in range(13):
                if self.cards[x] == 4:
                    score=x
        if hand == 'flush':
            score = self.order[self.value[self.card_count() - 1]]
        if hand == 'straight':
            score = self.order[self.value[self.card_count()-1]]
        if hand == 'straight flush' or hand == 'royal flush':
            score = self.order[self.value[self.card_count() - 1]]
        return score

    def tie_breaker(self,num):
        hand=self.hand_type()
        if hand == 'high card':
            if num > self.card_count()-1:
                score=None
            else:
                score = self.order[self.value[self.card_count()-num-1]]
        if hand == 'pair':
            temp=[]
            if num > self.card_count()-2:
                score=None
            else:
                for x in range(13):
                    if self.cards[12-x] == 1:
                        temp.append(12-x)
                score=temp[num-1]
        if hand == 'two pair':
            count=0
            if num == 1:
                count1=0
                for x in range(13):
                    if self.cards[12-x] == 2:
                        if count == 0:
                            if count1 == 0:
                                count1+=1
                            else:
                                score=12-x
                                count+=1
            else:
                if num > self.card_count()-4:
                    score=None
                else:
                    length=0
                    for x in self.cards:
                        if x == 2:
                            length+=1
                    if length == 3:
                        for x in range(13):
                            if self.cards[12-x] == 2:
                                score=10*(12-x)
                    else:
                        temp=[]
                        for x in range(13):
                            if self.cards[12 - x] == 1:
                                temp.append(12-x)
                        score = temp[num-2]

        if hand == 'three of a kind':
            temp=[]
            if num > self.card_count()-3:
                score=None
            else:
                for x in range(13):
                    if self.cards[12-x] == 1:
                        temp.append(12-x)
                score=temp[num-1]
        if hand in ['straight']:
            score=None
        if hand == 'flush':
            if num > self.card_count()-1:
                score=None
            else:
                score = self.order[self.value[self.card_count()-num-1]]
        if hand == 'full house':
            if num > 3:
                score=None
            else:
                length=0
                for x in range(13):
                    if self.cards[12-x] == 3:
                        length+=1
                if length == 2:
                    temp=[]
                    for x in range(13):
                        if self.cards[12-x] == 3:
                            temp.append(12-x)
                    score=temp[0]+temp[1]
                if length == 1:
                    length=0
                    for x in range(13):
                        if self.cards[12-x] == 3:
                            score=(12-x)
                    for x in range(13):
                        if self.cards[12-x] == 2:
                            length += 1
                    if length == 2:
                        temp=[]
                        for x in range(13):
                            if self.cards[12-x] == 2:
                                temp.append(12-x)
                        if num == 1:
                            score+=temp[0]
                        else:
                            score+=temp[1]
                    if length == 1:
                        for x in range(13):
                            if self.cards[12-x] == 2:
                                score+=(12-x)
                if num > 1 and length == 1:
                    for x in range(13):
                        if self.cards[12-x] == 1:
                            score+=12-x
        if hand == 'four of a kind':
            temp=[]
            if num > self.card_count()-4:
                score=None
            else:
                for x in range(13):
                    if self.cards[12-x] == 3:
                        for y in range(3):
                            temp.append((12-x)*self.cards[12-x])
                for x in range(13):
                    if self.cards[12-x] == 2:
                        for y in range(2):
                            temp.append((12-x) * self.cards[12-x])
                for x in range(13):
                    if self.cards[12-x] == 1:
                        temp.append(12-x)
                score=temp[num-1]
        if hand == 'straight flush':
            score=None
        if hand == 'royal flush':
            score=None
        return score

def create_cards():
    deck=Deck()
    Hearts=Suit('Hearts')
    Diamonds=Suit('Diamonds')
    Clubs=Suit('Clubs')
    Spades=Suit('Spades')
    for x in ['Hearts','Diamonds','Clubs','Spades']:
        for y in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
            if x == 'Hearts':
                tempcard=Card(x,y)
                Hearts.add_card(tempcard)
            if x == 'Diamonds':
                tempcard=Card(x,y)
                Diamonds.add_card(tempcard)
            if x == 'Clubs':
                tempcard=Card(x,y)
                Clubs.add_card(tempcard)
            if x == 'Spades':
                tempcard=Card(x,y)
                Spades.add_card(tempcard)
    deck.add_suit(Hearts)
    deck.add_suit(Diamonds)
    deck.add_suit(Clubs)
    deck.add_suit(Spades)
    return deck

ifile=open('Poker.csv', 'w')
csv_writer=csv.writer(ifile)
probability={
        'high card':0,
        'pair':0,
        'two pair':0,
        'three of a kind':0,
        'straight':0,
        'flush':0,
        'full house':0,
        'four of a kind':0,
        'straight flush':0,
        'royal flush':0
        }
p1=Player()
p2=Player()
deck=create_cards()
deck.shuffle_cards()
rounds=0
game_over=False
while not game_over:
    cards_on_table=[]
    p1.reset_player()
    p2.reset_player()
    if rounds%6 == 0:
        deck.shuffle_cards()
    for x in range(2):
        card = deck.deal_card()
        p1.give_card(card)
        cards_on_table.append(card)
    for x in range(2):
        card = deck.deal_card()
        p2.give_card(card)
        cards_on_table.append(card)
    for x in range(5):
        card=deck.deal_card()
        p1.give_card(card)
        p2.give_card(card)
        cards_on_table.append(card)
    p1.sort_hand()
    if p1.hand_type() == 'straight':
        string=[p1.display_hand(),p1.hand_type()]
        csv_writer.writerow(string)
    p2.sort_hand()
    print(p1.display_hand())
    print(p2.display_hand())
    print(p1.hand_type())
    print(p2.hand_type())
    probability[p1.hand_type()]+=1
    probability[p2.hand_type()]+=1
    p1.set_score()
    p2.set_score()
    if p1.score > p2.score:
        print('Player 1 wins!')
    elif p1.score < p2.score:
        print('Player 2 wins!')
    else:
        if p1.hand_score() > p2.hand_score():
            print('Player 1 wins!')
        elif p1.hand_score() < p2.hand_score():
            print('Player 2 wins!')
        else:
            done=False
            count=1
            while not done:
                print(p1.tie_breaker(count))
                print(p2.tie_breaker(count))
                if p1.tie_breaker(count) is None:
                    print('It\'s a draw!')
                    done = True
                elif p1.tie_breaker(count) > p2.tie_breaker(count):
                    print('Player 1 wins!')
                    done = True
                elif p1.tie_breaker(count) < p2.tie_breaker(count):
                    print('Player 2 wins!')
                    done=True
                count+=1
    for card in cards_on_table:
        deck.add_card(card)
    rounds+=1
    if rounds == 500000:
        game_over=True
for key, value in probability.items():
    print(key,'-',str(value))

ifile.close()