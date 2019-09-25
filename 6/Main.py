#This is a class made for the NAND 2 Tetris Project Chapter 6, Assembler 
#This is the main file that uses the Parser_Module to go through all of the 
#files and translate them. It is done in two passes, first saving 
#all of the user defined symbols and second transtalating the file given
#the completed tables. 

import Parser_Module

#Paths of all the files stored in an array 
files =[
        "/home/sebastian/Desktop/nand2tetris/projects/06/add/Add.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/max/MaxL.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/pong/PongL.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/rect/RectL.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/max/Max.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/pong/Pong.asm",
        "/home/sebastian/Desktop/nand2tetris/projects/06/rect/Rect.asm"
    ]

def main():
    for file in files:
        p = Parser_Module.Parser(file)
        #First Pass where we save all the user generated symbols 
        while(p.hasMoreCommands()):
            p.symbolCheck()
            p.advance()
        #Resets to the start of the file 
        p.resetCurrentLine()
        #Second Pass where we translate it all 
        while(p.hasMoreCommands()):
            p.commandTypes()
            if p.returnCommandType() == 0:
                p.writeLine(p.returnA())
            elif p.returnCommandType() == 2:  
                p.writeLine(p.returnC())
            p.advance()
        p.closeFiles()
    
main()