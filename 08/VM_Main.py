#This is a class made for the NAND 2 Tetris Project Chapter 8, VM Translator
#This is the main file that uses the VM_Parser_Module to go through all of the 
#files and translate them, both from Chapter 7 and Chapter 8

import VM_Parser_Module

def main():
    #All of the input file paths 
    inputFiles = ['/home/sebastian/Desktop/nand2tetris/projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/BasicTest/BasicTest.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/PointerTest/PointerTest.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm',
                  '/home/sebastian/Desktop/nand2tetris/projects/08/FunctionCalls/FibonacciElement',
                  '/home/sebastian/Desktop/nand2tetris/projects/08/FunctionCalls/StaticsTest'
                  ]
    #Look at each file one by one
    for file in inputFiles:
        p = VM_Parser_Module.VM_Parser(file)    #Create the parser object
        #Only creates boot strap for 8 and 9 other files assume bootstrap has been 
        #used or assume to be in a middle of a program 
        if file == inputFiles[8] or file == inputFiles[9]:
           p.bootstrap()
        while(p.hasMoreCommands()):             #While there are lines translate
            p.advance()     
        p.closeFiles()                          #Close the files to safely save them
        
main()