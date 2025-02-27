import numpy as np
import random as rand
from test import ai_model
import time

# each player in the game
class Player:

    guess = -1
    lives = 5
    name = "[insert]"
    alive = True

    # constructor
    def __init__(self, name, strat=None):
        self.name = name
        self.strat = ai_model(strat)

    def guess_a_number(self, previous_results="GAME START"):
        response = ""
        if self.strat:
            response = self.strat.sendMessage(previous_results)
        else:
            response = input("Choose your number: ")
        return int(response)




# take in a list of players, return a list of guesses from all AI players and the user
def collectGuesses(player_list):
    guesses = []
    for person in player_list[1:]:
        if person.alive:
            person.guess = person.guess_a_number(str(final_guesses))
            guesses.append(person.guess)
    if player_list[0].alive:
        player_list[0].guess = int(input("num 0-100: "))
        guesses.insert(0, player_list[0].guess)
    return guesses

# takes in a list of players and a target number, returns the player object with the closest guess to 0.8 * target number
def findClosestPlayer(player_list, num):
    closest_guy = [player_list[0]]
    for guy in player_list:
        if abs(num - guy.guess) < abs(num - closest_guy[0].guess):
            closest_guy = [guy]
        elif abs(num - guy.guess) == abs(num - closest_guy[0].guess) and guy is not closest_guy[0]:
            closest_guy.append(guy)
    return closest_guy

def findDupes(ppl):
    cooked = []
    for i in range(5):
        for j in range(i + 1, 5):
            if ppl[i].guess == ppl[j].guess and ppl[i].guess > -1:
                if ppl[i] not in cooked:
                    cooked.append(ppl[i])
                if ppl[j] not in cooked:
                    cooked.append(ppl[j])
    return cooked

# runs an iteration of the game
def run_iteration(ppl):
    global final_guesses
    sum_of_guesses = 0
    final_guesses = collectGuesses(ppl)
    for guy in ppl:
        if guy.alive:
            print(guy.name + " has selected " + str(guy.guess))
            time.sleep(1)
    if rule_one_invoked:
        dupes = findDupes(ppl)
        for cooked in dupes:
            print(cooked.name + " guessed the same number as somebody else and is thus disqualified.")
            final_guesses.remove(cooked.guess)
            cooked.guess = -999
    closest_players = []
    if len(final_guesses) > 0:
        sum_of_guesses = sum(final_guesses)
        average_of_guesses = float("{:.2f}".format(np.mean(final_guesses)))
        target = float("{:.2f}".format(average_of_guesses * 0.8))
        closest_players = findClosestPlayer(ppl, target)
        print("All guesses add up to " + str(sum_of_guesses) + ". The average is " + str(average_of_guesses) + ". The target number is " + str(target) + ".")
        time.sleep(1)
        for person in closest_players:
            print(person.name + " is closest!")
        time.sleep(1)
    print("All losing players will now lose a point.")
    time.sleep(1)
    for guy in ppl:
        if guy not in closest_players:
            guy.lives -= 1
    people = 0
    print("The current points are as follows:")
    for guy in ppl:
        if guy.alive:
            print(guy.name + ": " + str(guy.lives) + " points")
            time.sleep(1)
    for guy in ppl:
        check_lose(guy)
        if guy.alive:
            people += 1
    if people == 1:
        triggerWin(closest_players[0])
        return True
    if sum_of_guesses == 0 and not rule_one_invoked:
        invokeRule(1)


def triggerWin(guy):
    print(guy.name + " has won from being the last player standing!")

# check if a player has lost
def check_lose(player):
    global remaining
    if player.lives <= 0 and player.alive:
        print(player.name + " has been eliminated from losing all of their points.")
        time.sleep(1)
        player.alive = False
        player.guess = -999
        remaining -= 1
        if not rule_one_invoked:
            invokeRule(1)
        if remaining == 3:
            invokeRule(2)
        if remaining == 2:
            invokeRule(3)

def invokeRule(rule):
    global rule_one_invoked
    global rule_two_invoked
    global rule_three_invoked
    global list_of_players
    if rule == 1:
        time.sleep(1)
        print("Rule one has been invoked either because 1 player has been eliminated, or because all players have guessed 0.")
        print("Rule one: If two or more players choose the same number, the number is invalid and all players who selected the number automatically lose a point.")
        time.sleep(1)
        rule_one_invoked = True
        for guy in list_of_players:
            guy.guess_a_number("**New Rule:** If two or more players guess the same number in a round, all those players automatically lose the round. In such cases, do not choose a number that others might choose. Make sure your guess is unique to avoid elimination.")
    elif rule == 2:
        time.sleep(1)
        print("Rule two has been invoked because 2 players have been eliminated.")
        print("If a player chooses the exact correct number, they win the round and all other players lose two points.")
        time.sleep(1)
        rule_two_invoked = True
    elif rule == 3:
        time.sleep(1)
        print("Rule three has been invoked because 3 players have been eliminated.")
        print("If someone chooses 0, a player who chooses 100 automatically wins the round.")
        time.sleep(1)
        rule_three_invoked = True

    

def main():
    global final_guesses
    global rule_one_invoked
    global rule_two_invoked
    global rule_three_invoked
    global remaining
    global list_of_players
    rule_one_invoked = False
    rule_two_invoked = False
    rule_three_invoked = False
    final_guesses = "GAME START"
    game_continue = True
    list_of_players = [Player("me"), Player("Betty", "logician"), Player("Calvin", "follower"), Player("Dana", "risk_taker"), Player("Emelia", "troll")]
    remaining = len(list_of_players)

    while game_continue:
        terminate = run_iteration(list_of_players)
        if terminate:
            break


    
if __name__ == "__main__":
    global final_guesses
    global rule_one_invoked
    global rule_two_invoked
    global rule_three_invoked
    global remaining
    main()