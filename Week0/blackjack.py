#WATCH OUT FOR RECURSION... put stuff in loops and use return

from deck import Deck, Card
from player import Player

class BlackJack(object):
    def __init__(self, ante=2):
        self.player = self.create_player("Player")
        self.computer = self.create_player("Computer")
        self.ante = ante

        #self.human = human

    def create_player(self, title):
        #if self.human:
        name = raw_input("Enter %s name: " % title)
        #else:
        #    name = title
        return Player(name)


    def play_game(self):

        if self.player.wallet >= self.ante:

            deck = Deck()
            deck.shuffle()
            self.create_hands(deck)

            print "NEW GAME!"
            print "Available Funds: {}".format(self.player.wallet)

            self.display_hands()

            score_player, score_computer = self.calculate_value()

            if score_player == 21:
                print "\n*****************\n   BLACKJACK 3:2 PAYOUTS!\n*****************"
                raw_input("Press ENTER to continue...")
                self.player.wallet += self.ante*1.5
                if not self.play_game():
                    return False

            self.player_hit(deck, score_player)

            print "\n\n"

            self.display_hands(computer_turn=True)

            print "\n\n"

            while score_computer < 17:
                raw_input("Press ENTER to continue...")
                print "\n\n"

                self.computer.hand.append(deck.draw_card())
                self.display_hands(computer_turn=True)
                __, score_computer = self.calculate_value()
                print "\n\n"

            self.win_condition(score_player, score_computer)

        else:
            print "Insufficient Funds!"
            print "Balance: {}".format(self.player.wallet)
            return False





    def display_hands(self, computer_turn=False):
        if not computer_turn:
            print "{}:\t{} XX".format(self.computer.name, self.computer.hand[0])
        else:
            print "{}:\t{}".format(self.computer.name, " ".join(map(str, self.computer.hand)))
        print "{}:\t{}".format(self.player.name, " ".join(map(str, self.player.hand)))

    def call_prompt(self):
        print ""
        choice = ""
        chosen = False
        while chosen==False:
            choice = raw_input("Do you want to (H)it or (S)tay?")
            if choice in "HhSs":
                chosen=True
        return choice

    def calculate_value(self):
        score_player, score_computer = 0, 0
        values_dict = Card(13,4).value_dict
        player_ace_count, computer_ace_count = 0, 0

        for card in self.player.hand:
            card_str = str(card)
            if values_dict[card_str[:-1]]==11:
                player_ace_count+=1
            score_player += values_dict[card_str[:-1]]

        while player_ace_count > 0 and score_player > 21:
            player_ace_count -= 1
            score_player -= 10

        for card in self.computer.hand:
            card_str = str(card)
            if values_dict[card_str[:-1]]==11:
                computer_ace_count+=1
            score_computer += values_dict[card_str[:-1]]

        while computer_ace_count > 0 and score_computer > 21:
            computer_ace_count -= 1
            score_computer -= 10

        print "P-score: {} / C-score: {}".format(score_player, score_computer)
        return score_player, score_computer

    def player_hit(self, deck, score_player):
        player_choice = self.call_prompt()

        while player_choice not in 'Ss' and score_player is not 21:
            print "\n\n"
            if player_choice in 'Hh':
                self.player.hand.append(deck.draw_card())
                self.display_hands()
                score_player, __ = self.calculate_value()

            if score_player > 21:
                print "\n*****************\n   You BUSTED!\n*****************"
                raw_input("Press ENTER to continue...")

                self.player.wallet -= self.ante
                self.play_game()
            if score_player == 21:
                break

            player_choice = self.call_prompt()

    def win_condition(self, score_player, score_computer):
        if score_computer > 21 or score_computer < score_player:
            print "\n*****************\n   You WON!!!\n*****************"
            raw_input("Press ENTER to continue...")

            self.player.wallet += self.ante
            self.play_game()

        elif score_computer > score_player:
            print "\n*****************\n   You Lost :-(\n*****************"
            raw_input("Press ENTER to continue...")

            self.player.wallet -= self.ante
            self.play_game()

        elif score_computer == score_player:
            print "\n*****************\n   Draw :-/\n*****************"
            raw_input("Press ENTER to continue...")

            self.play_game()


    def create_hands(self, deck):
        self.player.hand = []
        self.computer.hand = []

        for i in xrange(2):
            self.player.hand.append(deck.draw_card())
            self.computer.hand.append(deck.draw_card())



if __name__ == '__main__':
    game = BlackJack()
    game.play_game()
