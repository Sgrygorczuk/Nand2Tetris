// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//The screen of this computer is made up from 256 Rows with 512 Pixels per row 

//   				512
//   		----------------->
//    256	|
//		| 
//		v

//The address where screen memory starts is RAM[16384] (0X4000)
//So we want to fill up the screen which is 8192 bytes or 8Kb 


//The Keyboard keeps track of all the key inputs through the RAM[24576] address, each key has a unique number attached to it so as long as the value at that address is larger than zero then the screen should be set to black 

//While(RAM{24576] > 0)
//{
//	RAM[16385] - RAM[24608] = 1
//}
		
@8192			//Go to Mem[8192] 8Kb 
D = A			//Save that number in D
@R2			//Go to Mem[2]
M = D			//Set Mem[2] = 8192, this is N 
(WHILE)
@R1			//Go to Mem[1]
M = 1			//Set Mem[1] = 1 = i 
@SCREEN		//Saves the address of screen into D
D = A
@R0			//Set the start address to SCREEN
	M = D	
(STEP)
	@24576		//Look at the Keyboard Address 
	D = M			//Look at the memory stored in that Address save it to Register D 
	@WHITE
	D;JEQ			//If D = 0 go to WHITE else go to BLACK
	@R1			//Go to Mem[1], i
	D = M			//Set value of D = i
	@R2			//Go to Mem[2], n 
	D = D - M		//i = i - n
	@WHILE		//
	D;JGT			//If i > n jump to WHILE 
	@R0			//Jump to Mem[0]
	A = M			//Store the current address into Register A
	M = -1		//Set the value of that address to -1
	@R1			//Jump to Mem[1]
	M = M + 1		//Increment i			
	@R0			//Jump to Mem[0]
	M = M + 1		//Increment 
	@STEP
	0;JMP	 
(WHITE)
	@R1			//Go to Mem[1], i
	D = M			//Set value of D = i
	@R2			//Go to Mem[2], n 
	D = D - M		//i = i - n
	@WHILE		//
	D;JGT			//If i > n jump to WHILE 
	@R0			//Jump to Mem[0]
	A = M			//Store the current address into Register A
	M = 0			//Set the value of that address to -1
	@R1			//Jump to Mem[1]
	M = M + 1		//Increment i			
	@R0			//Jump to Mem[0]
	M = M + 1		//Increment 
	@STEP
	0;JMP	 



