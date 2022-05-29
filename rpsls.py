# .\rpsls.py
# A Python version of the game Rock, Paper, Scissors, Lizard, Spock as
# invented by Sam Kass and Karen Bryla
#
# This program was ported from my c#.NET version of the game. I will
# eventually put this up on GitHub with the c# version.
# Granted the game is pretty simple and a bit silly, but it is a
# great program for learning or honing your knowledge of a language.
#
#  RPSLS, a Python implementation of Rock, Paper, Scissors, Lizard, Spock
#  Copyright © 2020 Dan Rhea
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from random import randint
from colorama import init, Fore, Back
import os
import sys
import platform

def clearScreen():
    """clearScreen(): Clear screen based on the OS we are running"""
    sysIs = platform.system()
    if sysIs == "Windows":
        os.system("cls")
    elif sysIs == "Linux":
        os.system("clear")

def showFile(filePath, pageSize=24):
    """showFile(FilePath): Display paginated text from the file in FilePath"""
    page = 1
    clearScreen()
    print(Fore.LIGHTBLUE_EX+Back.BLACK)
    row = 0
    with open(filePath) as FileStream:
        try:
            for line in FileStream:
                sys.stdout.write(line)
                row = row + 1
                if row > pageSize:
                    row = 0
                    c = input(Fore.YELLOW+"Page: "+str(page)+" "+Fore.BLUE+"Enter \"Q\" to quit: "+Fore.LIGHTBLUE_EX)
                    clearScreen()
                    page = page + 1
                    if c.upper() == "Q":
                        break
        except:
            print("Error in: "+filePath+" is "+ sys.exc_info()[0])
            pass
        finally:
            FileStream.flush()
            FileStream.close()
    clearScreen()
    print(Fore.WHITE+Back.BLACK)

pageSize = os.get_terminal_size()

proxys = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]

results_list = [                    # Result matrix
    0,  -1,    1,       1,    -1,   # Rock
    1,   0,   -1,      -1,     1,   # Paper
    -1,  1,    0,       1,    -1,   # Scissors
    -1,  1,   -1,       0,     1,   # Lizard
    1,  -1,    1,      -1,     0    # Spock
] # Rock Paper Scissors Lizard Spock - Used to resolve combat
# 1: Win -1: Lose 0: Draw

#    Rock             Paper              Scissors             Lizard            Spock
verbs_list = [
    "matches",       "is covered by",   "smashes",           "crushes",        "is vaporized by", # Rock
    "covers",        "matches",         "is cut by",         "is eaten by",    "disproves",       # Paper
    "are broken by", "cuts",            "matches",           "decapatate",     "are smashed by",  # Scissors
    "is crushed by", "eats",            "is decapitated by", "matches",        "poisons",         # Lizard
    "vaporizes",     "is disproved by", "smashes",           "is poisoned by", "matches"          # Spock
] # Horizontal player proxy versus vertical computer proxy... this is used to build results text

debug = False
player_score = 0
computer_score = 0
tie_score = 0
match_count = 0
result = ""
cl = Fore.WHITE
prompt = "RPSLS> "

# Greet the player
print(Fore.YELLOW+
    "RPSLS 1.0, a Rock Paper Scissors Lizard Spock game\n" +
    "as invented by Sam Kass and Karen Bryla\n"+
    "programmed by Dan Rhea © 2020\n"+
    "under the GPL3 license (enter \"License\" to view)\n"+
    Fore.WHITE)

# Get the player proxy or command
player_input = input(prompt).capitalize()

while player_input not in("Q", "X", "Quit", "Exit"):
    computer_guess = randint(0,4)   # Get the computer guess (actually an index into proxys)
    try:
        # Get the player proxy index
        player_guess = int(proxys.index(player_input))
    except:
        # Not a proxy so it may be a command
        if player_input == "License":
            # Show the GNU 3 License text
            showFile("./gnu_gpl3.txt", pageSize.lines-2)
            clearScreen()
        elif player_input == "Debug":
            if debug:
                debug = False
                print("Debug mode toggled off")
            else:
                debug = True
                print("Debug mode toggled on")
        else:
            print(Fore.LIGHTBLUE_EX+
                "I don't understand \"" + player_input + "\"!"+
                "\nEnter \"Rock\", \"Paper\", \"Scissors\", \"Lizard\" or \"Spock\"."+
                "\nEnter \"License\" to view the license."+
                "\nEnter \"Quit\" or \"Exit\" to exit."+
                Fore.WHITE)
    else:
        # Process the player guess
        match_count = match_count + 1
        # Compute the index into the results and verb lists
        result_index = (player_guess * 5) + computer_guess

        if debug:
            print("Debug: Plyr: "+str(player_guess)+" Comp:"+str(computer_guess))
            print("Debug: Rslt: "+str(result_index)+" = (Plyr*5)+Comp")

        # Process the result
        if results_list[result_index] == 1:
            cl = Fore.GREEN
            result_string = "Player wins over Computer!"
            player_score = player_score + 1
        elif results_list[result_index] == -1:
            cl = Fore.RED
            result_string = "Player loses to Computer!"
            computer_score = computer_score + 1
        elif results_list[result_index] == 0:
            cl = Fore.YELLOW
            result_string = "Player ties with Computer!"
            tie_score = tie_score + 1
        else:
            cl = Fore.MAGENTA
            result_string = "Combat error! Program rides the failboat."

        # Display the results of the match
        print(cl+
            "{0} {1} {2}! {3} Player: {4} Computer: {5}".format(
            proxys[player_guess], verbs_list[result_index], proxys[computer_guess],
            result_string, str(player_score), str(computer_score))+Fore.WHITE)
    finally:
        pass

    # Get the player proxy for the next match
    player_input = input(prompt).capitalize()

if match_count > 0:
    if player_score > computer_score:
        if match_count == 1:
            print(Fore.GREEN+
                "In "+str(match_count)+" match, you defeated the computer "+
                str(player_score)+" to "+str(computer_score)+"!")
        else:
            print(Fore.GREEN+
                "In "+str(match_count)+" matches, you defeated the computer "+
                str(player_score)+" to "+str(computer_score)+"!")
    elif computer_score > player_score:
        if match_count == 1:
            print(Fore.RED+
                "In "+str(match_count)+" match, the computer defeated you "+
                str(computer_score)+" to "+str(player_score)+"!")
        else:
            print(Fore.RED+
                "In "+str(match_count)+" matches, the computer defeated you "+
                str(computer_score)+" to "+str(player_score)+"!")
    else:
        if match_count == 1:
            print(Fore.YELLOW+
                "In "+str(match_count)+" match, you won "+str(player_score)+ 
                ", the computer won "+str(computer_score)+"!") 
        else:
            print(Fore.YELLOW+
                "In "+str(match_count)+" matches, you won "+str(player_score)+ 
                ", the computer won "+str(computer_score)+"!")
    if tie_score == 1:
        print(Fore.LIGHTBLUE_EX+
            str(tie_score)+" tie match."+Fore.WHITE)
    else:
        print(Fore.LIGHTBLUE_EX+
            str(tie_score)+" tie matchs."+Fore.WHITE)
else:
    print(Fore.GREEN+
        "You don't appear to have played any matches. Good bye!"+
         Fore.WHITE)
    print(Fore.RESET+Back.RESET)
