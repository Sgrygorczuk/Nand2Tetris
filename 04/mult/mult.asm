// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


//You set i = 1 and not 0 to keep right track of iterations if i = 1 and R1 = 0 you quit while loop before doing any arithmetic 

//int i = 1;
//R2 = 0;
//While(i < R1)
//{
//	R2 += R0;
//	i++;
//} 

// Put your code here.
	@3				//Looks at Memory Address 3 = 0
	M = 1 			//i = 1
	@2				//Looks at Memory Address 2 = R2
M = 0 			//R2 = 0
(WHILE)
	@3			//Looks at Memory Address 3 = 1
	D = M			//Read Memory in Register D, D = M = i
	@1			//Looks at Memory Address 1 = R1
	D = D - M		//Subtracts D = D - M which is equal to i = i - R1, and stores the value in Register D 
	@END			//Looks at the memory Address of END 
	D;JGT			//If i - R1 > 0 goto END, ends the while loop  
 	@0			//Looks at Memory Address 0 = R0
	D = M;		//Reads Memordy and stores it into Register D, D = R0
	@2			//Looks at Memory Address 2 = R2
	M = M + D		//Updates the current sum of R2, R2 = R2 + R0, R2 += R0
	@3			//Looks at Memory Address 3 = i
	D = M			//Set D = i
	@3
	M = D + 1 		//Increment counter M[i] = D[i] + 1
	@WHILE
	0;JMP			//goto WHILE 
(END)	
	@END
	0;JMP			//goto END, Infinite loop until ticks run out
