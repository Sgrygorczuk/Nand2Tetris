@SCREEN		//Saves the address of screen into D
D = A
@R0			//Set the start address to SCREEN
M = D
@R0
A = M		//Store the current address into Register A
M = -1		//Set the value of that address to -1
