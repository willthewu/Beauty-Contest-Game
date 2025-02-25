import numpy as np
import random as rand

# each player in the game
class Player:

    guess = -1
    lives = 10
    name = "[insert]"
    alive = True

    # constructor
    def __init__(self, name):
        self.name = name


# take in a list of players, return a list of guesses from all AI players and the user
def collectGuesses(player_list):
    guesses = []
    for person in player_list[1:]:
        if person.alive:
            person.guess = rand.randint(0, 100)
            guesses.append(person.guess)
    player_list[0].guess = int(input("num 1-100: "))
    print()
    guesses.insert(0, player_list[0].guess)
    return guesses

# takes in a list of players and a target number, returns the player object with the closest guess to 0.8 * target number
def findClosestPlayer(player_list, num):
    closest_guy = player_list[0]
    for guy in player_list:
        if abs(num - guy.guess) < abs(num - closest_guy.guess):
            closest_guy = guy
    return closest_guy

# runs an iteration of the game
def run_iteration(ppl):
    final_guesses = collectGuesses(ppl)
    sum_of_guesses = sum(final_guesses)
    average_of_guesses = float("{:.2f}".format(np.mean(final_guesses)))
    target = float("{:.2f}".format(average_of_guesses * 0.8))
    closest_player = findClosestPlayer(ppl, target)
    for guy in ppl:
        if guy.alive:
            print(guy.name + " has selected " + str(guy.guess))
    print()
    print("All guesses add up to " + str(sum_of_guesses) + ". The average is " + str(average_of_guesses) + ". The target number is " + str(target) + ".")
    print(closest_player.name + " is closest!")
    print("All losing players will now lose a point.")
    print()
    for guy in ppl:
        if guy != closest_player:
            guy.lives -= 1
            check_lose(guy)
    people = 1
    print("The current points are as follows:")
    for guy in ppl:
        if guy.alive:
            people -= 1
            print(guy.name + ": " + str(guy.lives) + " points")
    if people == 0:
        triggerWin(closest_player)
        return True
    print()

def triggerWin(guy):
    print()
    print(guy.name + " has won from being the last player standing!")

# check if a player has lost
def check_lose(player):
    if player.lives == 0:
        print(player.name + " has been eliminated from losing all of their points.")
        print()
        player.alive = False
        player.guess = -999

    

def main():
    game_continue = True
    list_of_players = [Player("me"), Player("Betty"), Player("Calvin"), Player("Dana"), Player("Emelia")]

    while game_continue:
        terminate = run_iteration(list_of_players)
        if terminate:
            break


    
if __name__ == "__main__":
    main()