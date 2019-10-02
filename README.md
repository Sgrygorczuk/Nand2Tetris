# Nand2Tetris

This project is based on the Nand2Tetris project from the https://www.nand2tetris.org/, 
Folders 01-05 deal with the creation of a sixteen-bit CPU using HDL, 06-12 deal with utilizing the CPU and building to a more user-friendly interaction with it through the creation of Assembler, VM Translator, Compiler using Python

01 Logic Components: 
       Creates bit and sixteen-bit components such as AND, OR, NOR, XOR and MUX to build more complex units in the later chapters 
       
02 ALU:
       Creates arithmetic units that build up to an ALU which will perform all the computation a CPU has to 
       
03 Memory:
       Creates memory units that build up the RAM and PC which will store all the pointer and data the CPU uses
       
04 Assembly:
       To understand how the CPU function the chapter focuses on using assembly to perform two functions, one that multiples two inputs and another that changes the color of the screen from white to black and vice versa. 
       
05 CPU:
      Putting together the ALU, Memory and Logic Components to make a functioning Computer 
      
06 Assembler:
      Reads the input ASM files and translates them to HACK files so that the CPU can read them. 
      
07 VM Part I Arithmetic and Memory:
      Reads the input VM files and translates them to ASM files, only dealing with basic arithmetic and memory calls 
      
08 VM Part II Protocols:
