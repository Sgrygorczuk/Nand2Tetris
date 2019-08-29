// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/mult/Mult.tst

load Mult.hack,
output-file Mult.out,
compare-to Mult.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;



set PC 0,
set RAM[0] 3,   // Set test arguments
set RAM[1] 1,
set RAM[2] -1;  // Ensure that program initialized product to 0
repeat 120 {
  ticktock;
}
set RAM[0] 3,   // Restore arguments in case program used them as loop counter
set RAM[1] 1,
output;
