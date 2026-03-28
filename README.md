# First Strike # 
*A strategic game about energy management and survivability against a programmed bot.* 

### Gameplay ###
First Strike is a simultaneous, text-based, combat game where players try to defeat an opponent, a moveset shadowing theirs. Why is it called "First Strike"? Because whoever gets the (literal) first strike wins the game.
The game is written in python and your saves are stored in a `.json` file. To play, please download both files and run them in the same folder!

### Required Libraries ###
- time
- random
- os
- json
- requests
- fastapi
- datetime

### Moveset ###
As of 9/3/2026, there are five legal moves:

1. \[Misc\] Charge - gain 1 energy
2. \[Misc\] Shield - Block Basic Attacks, cost 0
3. \[Basic Attack\] Fireball - costs 1 energy, destroys Charge
4. \[Basic Attack\] Sword - costs 2 energy, destroys Charge and Fireball
6. \[Attack+\] Mountain - costs 7 energy, destroys everything else

### Beta Moves ###
*As of 11/3/2026, these moves are still in beta testing and are not combat legal yet:*

1. \[Attack\] Taser - cost 1 energy, destroy chield and sword
2. \[Attack+\] Shadow Ball - costs 4 energy, destroys everything but mountain and fireball
3. \[Attack\] Bow and Arrow - costs 2 energy, destroys charge, sword and taser (if added)

Do take a while to get used to keeping track of both yours and your opponent's energy, as there is no counter and part of the gameplay is to actively track the energy levels!

Inspired by the popular Singaporean childhood game "Charge". Can't find any other refrences except this [reddit post](https://www.reddit.com/r/askSingapore/comments/11b8iyq/anyone_remembers_the_childhood_game_charge/). 

## Changelog ##

**28/3/2026**

*v1.1.2c*

Major shop changes. However, no effects have been implemented yet.


**27/3/2026**

*v1.1.2b*

Testing online shop API *\[Beta Optional Update\]*


**21/3/2026**

*v1.1.2a*

Testing online shop API *\[Beta Optional Update\]*



**12/3/2026**

*v1.1.2*

Testing online shop API *\[Beta Optional Update\]*



**10/3/2026**

*v1.1.1*

Added win ratio in the main menu

Testing beta move `Bow and Arrow`

Updated bot algorithm



**9/3/2026**

*v1.1.0*

Added main menu and move swapping

Testing beta moves `Taser` and `Shadow Ball`

Added player game saving



**7/3/2026**

*v1.0.0*

Initial push to Github

---
*Aidan Ng 2026*
