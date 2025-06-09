import sys
import random
import time

def division(no1, no2):
    if no2 > no1:
        no1, no2 = no2, no1
    return no1 // no2

def zero(no1, no2):
    if no1 > no2:
        no1, no2 = no2, no1
    first = (no1 + 9) // 10 * 10
    last = (no2 // 10) * 10
    if first > last:
        return 0
    return ((last - first) // 10) + 1

print("Welcome to Secret Number")
print("""Pick an option:
a) Play with 11 players (piece change counted)
b) Play with custom amount of players (piece change not counted)""")
players_option = input()
playing_default = False
if players_option == "a":
    no_of_players = 11
    playing_default = True
elif players_option == "b":
    try:
        no_of_players = int(input("Please enter the number of players: "))
        if no_of_players <= 1:
            print("Please enter a positive whole number that is not 1.")
            sys.exit()
    except ValueError:
        print("Please enter a positive whole number that is not 1.")
        sys.exit()
else:
    print("Please pick a valid option.")
    sys.exit()

player_info = {}
assigned_numbers = set()

for i in range(1, no_of_players + 1):
    player_name = input(f"Enter the name for player {i}: ")
    secret_number = random.randint(1, 100)
    while secret_number in assigned_numbers:
        secret_number = random.randint(1, 100)
    assigned_numbers.add(secret_number)
    player_info[player_name] = {
        "secret_number": secret_number,
        "points": 0,
        "piece_change": 0
    }

while True:
    print("""Pick an option:
a) Use contact cards
b) End the game""")
    option = input()
    if option == "a":
        print("Players:")
        for player in player_info:
            print(player)

        player_1 = input("Enter the name of the first player: ")
        if player_1 not in player_info:
            continue

        player_2 = input("Enter the name of the second player: ")
        if player_2 not in player_info or player_1 == player_2:
            continue

        print("""Please pick a card type to use.
(a) Addition
(b) Multiplication
(c) Division
(d) Zero""")
        card_option = input()

        n1 = player_info[player_1]["secret_number"]
        n2 = player_info[player_2]["secret_number"]

        if card_option == "a":
            result = n1 + n2
            if result > 180:
                print("The result is between 180 and 199.")
            elif result < 20:
                print("The result is between 3 and 20.")
            else:
                print(f"Result of {player_1} and {player_2} using the addition card: {result}.")
        elif card_option == "b":
            result = (n1 * n2) % 10
            print(f"Result of {player_1} and {player_2} using the multiplication card: {result}.")
        elif card_option == "c":
            result = division(n1, n2)
            print(f"Result of {player_1} and {player_2} using the division card: {result}.")
        elif card_option == "d":
            result = zero(n1, n2)
            print(f"Result of {player_1} and {player_2} using the zero card: {result}.")
        else:
            print("Please pick a valid option.")
    elif option == "b":
        print("The checking of answer sheets will now begin.")
        print("Please type in nothing if there was no answer given.")

        for player_guessing in player_info:
            print(f"Checking {player_guessing}")
            for other_player in player_info:
                if other_player != player_guessing:
                    guess = input(f"What is {player_guessing}'s guess for {other_player}'s number? ")
                    if guess != "":
                        try:
                            if int(guess) == player_info[other_player]["secret_number"]:
                                player_info[player_guessing]["points"] += 1
                                player_info[other_player]["points"] -= 1
                            else:
                                player_info[player_guessing]["points"] -= 1
                        except ValueError:
                            player_info[player_guessing]["points"] -= 1
                else:
                    guess = input(f"What is {player_guessing}'s guess for their number? ")
                    if guess != "":
                        try:
                            if int(guess) == player_info[player_guessing]["secret_number"]:
                                player_info[player_guessing]["points"] += 5
                            else:
                                player_info[player_guessing]["points"] -= 5
                        except ValueError:
                            player_info[player_guessing]["points"] -= 5

            if player_info[player_guessing]["points"] == no_of_players + 4:
                player_info[player_guessing]["points"] += 5

        ranked_players = sorted(player_info.items(), key=lambda x: x[1]["points"], reverse=True)
        if playing_default:
            points_set = {info["points"] for info in player_info.values()}
            all_same = len(points_set) == 1

            if all_same:
                print("All players must return 1 piece each, as they all have the same number of points.")
                for player in player_info:
                    player_info[player]["piece_change"] -= 1
            else:
                print("Players:")
                for player in player_info:
                    print(player)

                player_picked_last = input(f"Who did {ranked_players[0][0]} pick to require returning 3 pieces? ")
                while player_picked_last not in player_info:
                    print("Please pick a valid player.")
                    player_picked_last = input(f"Who did {ranked_players[0][0]} pick to require returning 3 pieces? ")
                    
            min_points = min(info["points"] for info in player_info.values())
            lowest_players = [name for name, info in player_info.items() if info["points"] == min_points]

            for player_name, info in ranked_players:
                if info["points"] >= 16:
                    info["piece_change"] += 3
                elif info["points"] >= 11:
                    info["piece_change"] += 2
                elif info["points"] >= 6:
                    info["piece_change"] += 1
                elif player_name in lowest_players and not all_same:
                    info["piece_change"] -= 3
                elif info["points"] < 0:
                    info["piece_change"] -= 2
                else:
                    info["piece_change"] -= 1

                if info["piece_change"] < 0:
                    print(f"{player_name}: {info['points']} points (Return {abs(info['piece_change'])} pieces)")
                elif info["piece_change"] == 0:
                    print(f"{player_name}: {info['points']} points (No pieces given)")
                else:
                    print(f"{player_name}: {info['points']} points (Receive {info['piece_change']} pieces)")
        else:
            for player_name, info in ranked_players:
                print(f"{player_name}: {info['points']} points")
                
        sys.exit()
    else:
        print("Please pick a valid option.")
