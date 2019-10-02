#This is a class made for the NAND 2 Tetris Project Chapter 7, VM Translator
#This is the main file that uses the VM_Parser_Module to go through all of the 
#files and translate them. 

import VM_Parser_Module

def main():
    #All of the input file paths 
    inputFiles = ["/home/sebastian/Desktop/nand2tetris/projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm",
                  "/home/sebastian/Desktop/nand2tetris/projects/07/StackArithmetic/StackTest/StackTest.vm",
                  "/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/BasicTest/BasicTest.vm",
                  "/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/PointerTest/PointerTest.vm",
                  "/home/sebastian/Desktop/nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm"
                ]
    #Look at each file one by one
    for file in inputFiles:
        p = VM_Parser_Module.VM_Parser(file)    #Create the parser object
        while(p.hasMoreCommands()):             #While there are lines translate
            p.advance()                         #Go to next line
        p.closeFiles()                          #Close the files to safely save them
        
main()