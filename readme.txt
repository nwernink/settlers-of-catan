Coding Settlers of Catan!
import PIL
import cmu_112_graphics
run catan.py
keep provided image files in the same folder

The popular board game, Settlers of Catan, is beloved by millions around the world. We set out to code this board game in its entirety.

The rules of the game are as follows:
- Each of the four players compete to reach 10 points by building: 
	- settlements: 1
	- cities: 2
	- buying the most knight cards (largest army): 2
	- building the most roads (longest road): 2
	- buying VP cards: 1
- The board is randomly generated
- Each turn a player:
	- rolls die to collect resources
		- if you roll a 7, you can move the robber to a hexagon of 		your choice
			- you can then steal a random card from one of the 			players that have a settlement bordering that hexagon
			- if anyone has more than 7 cards, you lose half of 			your resource card hand
	- receives resources that their settlements/cities border
		- if 1 your settlements borders a hexagon whose number has 		just been rolled, you receive a resource card that 			corresponds to the tile (for cities, receive 2)
	- trades with other players to assemble sets of resource cards or 	trade with the bank at a 4 for 1 rate
	- builds/buys with resource cards:
		- road: 1 brick, 1 wood
		- settlement: 1 wheat, 1 wood, 1 sheep, 1 brick
		- city: 2 wheat, 3 ore
		- development card: 1 sheep, 1 wheat, 1 ore
	-the various development cards that you buy can be used for:
		- knight: allows you to move the robber to a hexagon of your 		choosing and steal a random resource from a player bordering 		the hexagon
		- monopoly: gives you all of a random resource from all other 		players
		- year of plenty: gives you 2 random resources
		- road building: gives you 2 roads to build 
		- victory point (VP): gives your one point towards victory
	- click done when you are finished building
	- click submit when you are finished with your turn
		- the next player can now roll to begin turn
- Tkinter game functionality:
	- to roll die, click roll die text
	- to play a development card, click corresponding development card 	text in your player hand
	- to trade, press t on keyboard to enter the trading interface
		- to select the player you want to trade with, click the 		corresponding rectangle on one of the four corners of the 		board
		- press c to reveal/hide your hand and select the resources 		you want to offer to trade by clicking on the corresponding 		text in player hand
		- hide your hand with c and hand your opponent the computer 
		- press o to reveal/hide your opponent's hand and select the 		resources that they want to offer to you
		- hide your opponents hand with o and once you have come to 		an agreement, press accept to execute the trade
		- if you press decline, it clears currently offered resources 		and you can continue trading or return to the current player 		interface by pressing t
		- you can continue to trade with other players or return to t		he current player interface by pressing t
		- you can also trade with the bank at a 4 for 1 rate
			- when in the trading interface, press b
			- select four of the same type of resource from your 			hand you would like to trade and select the 				resource you desire from the bank
			- click accept or decline to accept the deal or clear 			the current trade
	- to build/buy, click corresponding item
		- if you have the required resources, you can then place the 		item on the board
			- settlements: click on a vertex of the hexagon two 			spaces away from any other settlement/city
			- cities: click on your pre-existing settlement to 			upgrade to a city
			- roads: click on a vertex of the hexagon where you 			already have a road tail or settlement/city and then 			click on an adjacent vertex of the hexagon
	- to move the robber, once you have played a knight card or rolled a 	7, click on the center of the hexagon where you want to place it
		- resource production from this hexagon is blocked until the 		robber is moved

Points of Interest/Algorithmic Complexity:
	- the unique hexagonal structure of the board made us implement new 	ways to check adjacency/mouse pressed
		- road building/settlement/city placement was especially 		challenging
	- trading screen interface enabled ease of user interaction

For more information about how Catan works please refer to Game Rules & Almanac 3/4 Players at https://www.catan.com/service/game-rules# 