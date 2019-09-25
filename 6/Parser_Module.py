#This is a class made for the NAND 2 Tetris Project Chapter 6, Assembler 
#The goal of this class to go through each line of the .asm code and detrime 
#what is its binary equivalent. It uses two other classes Code_Module and 
#Symbol_Table_Module to keep track of the predefined and user defined symbols 
#This class is also responosible for all of the I/O interactions such as opening
#writing and closing files. 

import Code_Module
import Symbol_Table_Module

class Parser:
    def __init__(self, inputFile):
        self.inputFile = open(inputFile, 'r')
        self.outputFile = open(inputFile[:len(inputFile)-3]+"hack", 'w')
        self.currentLine = 0
        self.addressCounter = 0;
        self.lines = self.inputFile.readlines();
        self.lineCount = len(self.lines);
        #Command Types. 0 = A, 1 = L, 2 = C, 3 = Ignore 
        self.commandType = 0
        self.symbolTable = Symbol_Table_Module.symbolTable()
        self.labelTabel = {                  #Address
        "SP"    : "0000000000000000",        #0
        "LCL"   : "0000000000000001",        #1
        "ARG"   : "0000000000000010",        #2
        "THIS"  : "0000000000000011",        #3
        "THAT"  : "0000000000000100",        #4
        "R0"    : "0000000000000000",        #0
        "R1"    : "0000000000000001",        #1
        "R2"    : "0000000000000010",        #2
        "R3"    : "0000000000000011",        #3
        "R4"    : "0000000000000100",        #4
        "R5"    : "0000000000000101",        #5
        "R6"    : "0000000000000110",        #6
        "R7"    : "0000000000000111",        #7
        "R8"    : "0000000000001000",        #8
        "R9"    : "0000000000001001",        #9
        "R10"   : "0000000000001010",        #10
        "R11"   : "0000000000001011",        #11
        "R12"   : "0000000000001100",        #12
        "R13"   : "0000000000001101",        #13
        "R14"   : "0000000000001110",        #14
        "R15"   : "0000000000001111",        #15
        "SCREEN": "0100000000000000",        #16384
        "KBD"   : "0110000000000000",        #24576
        }
    
    #Checks if there is more lines in the file to translate 
    def hasMoreCommands(self):
        if self.currentLine == self.lineCount:
            return False
        else:
            return True 
    
    #Sets the current line back to zero for when we do the second pass of the 
    #file 
    def resetCurrentLine(self):
        self.currentLine = 0
    
    #If there are more lines then we procceed to the next tine 
    def advance(self):
        if self.hasMoreCommands():
            self.currentLine = self.currentLine + 1
    
    #Cleans us the line so its easier to translate
    #First removes all of the empty spaces 
    #Second looks for comments and removes them either from the beginning or 
    #after an instruction 
    def commentRemover(self):
        self.lines[self.currentLine] = self.lines[self.currentLine].replace(" ", "")
        self.lines[self.currentLine] = self.lines[self.currentLine].replace("\n", "")
        index = self.lines[self.currentLine].find("//")
        if index != -1:
            self.lines[self.currentLine] = self.lines[self.currentLine][:index]
    
    #Checks for what kind of insturction we are looking at
    #If the instruction contains '@' then it's A type meaning that it's an address
    #If the instruion contains a '=' or a ';' then is an arithmetic or jump insturction 
    #which is C Type
    #If it's neither, an empty line which used to be a commment it gets type 3 which we ignore 
    def commandTypes(self):
        self.commentRemover()
        if self.lines[self.currentLine].find("@") != -1:
            self.commandType = 0
        elif self.lines[self.currentLine].find("=") != -1 or self.lines[self.currentLine].find(";") != -1:
            self.commandType = 2
        else:
            self.commandType = 3
    
    #Checks if it is a undefined symbol and adds it to the Symbols tables 
    #Gets rind of the excess parts of the symbol like the @ and () 
    #Based on if its is a @ or () it will label it as a variables which starts at adress 16
    #or it will label it as an address to jump to saving the current address 
    def symbolCheck(self):
        self.commentRemover()
        afterAt = ""
        jumpToLabel = 0
        if self.lines[self.currentLine].find("@") != -1 and self.lines[self.currentLine].islower():
            afterAt = self.lines[self.currentLine][1:len(self.lines[self.currentLine])]
        elif self.lines[self.currentLine].find("(") != -1:
            afterAt = self.lines[self.currentLine][1:len(self.lines[self.currentLine])-1]
            jumpToLabel = 1
        confrirm = self.labelTabel.get(afterAt)
        if afterAt != "" and confrirm == None and afterAt.isdigit() == False:
            self.symbolTable.addEntry(afterAt, self.addressCounter, jumpToLabel)
        if self.lines[self.currentLine] != "" and self.lines[self.currentLine].find("(") == -1:
            self.addressCounter = self.addressCounter + 1
            
    #Returns the current state of commandType variable to the user
    def returnCommandType(self):
        return self.commandType
    
   #The return A will create a 16 bit output string 
   #It will interpret if it is looking at symbol or number 
   #If it is symbol it needs to check if it is pre programed or user symbol 
    def returnA(self):
       #First checks if this is indeed a A Type Instruction 
       if self.commandType == 0:
           #in @123 or @SP the afterAt refers to 123 or SP
           afterAt = self.lines[self.currentLine]
           #Removes the @ and the /n from the string
           afterAt = afterAt[1:len(afterAt)]
           #Since not all numbers translate to 16 bit addresses extend is there to extend it
           #So that 101 turns to 0000000000000101
           extend = "0000000000000000"
           symbol = self.isSymbol(afterAt)
           if afterAt.isdigit():
               #lenght is there to figure out how much to cut from the end of the empty string
               lenght = len('{0:b}'.format(int(afterAt)))
               #Here we short the end of the extend and then attach the binary version
               #of the number that we were given 
               return extend[:16-lenght] + '{0:b}'.format(int(afterAt))
           #Check if its a vaiable symbol then choose what kind and reads from that table 
           elif symbol == 0 or symbol == 1:
               if symbol == 0:
                   return self.labelTabel[afterAt]
               elif symbol == 1:
                   return self.symbolTable.getAddress(afterAt)
    
    #Check for if the given string is a symbol that exits in either 
    #predefined tables or a user defined symbol
    def isSymbol(self, symbol):
        symbol = symbol
        confrirm = self.labelTabel.get(symbol)
        if confrirm != None:
            return 0
        confrirm = self.symbolTable.contains(symbol)
        if confrirm != None:
            return 1
        return 2
    
    #The return C will create a 16 bit output string 
    #It will interpret if this is an arithmetic or jump C Type instuction 
    #How an insturction is broken down 
    #line is AM=A+M/n
    #Indexs  0123456
    #line.find('=') = 2 
    #line[0:equal] = AM only indexes 01 
    #line[equal+1:lien(line)-1] = A+M moves one from '=' and remvoes '/n' 
    def returnC(self):
        #Make sure that this is in fact C Type instruction before exectuing 
        line = self.lines[self.currentLine]
        if self.commandType == 2:
            #Create an Empty Code Module which will help us determin the bits for dest, comp, and jump
            commandC = Code_Module.Code()
            equal = line.find("=")
            semicolon = line.find(";")
            #If the C type is arithmetic then there will be a '=' which means that the jump is set to 'null'
            if equal != -1:
                commandC.updateData(line[0:equal], line[equal+1:len(line)] , "null")
            #If the C type is a jump then there will be a ';' which means that the dest is set to 'null'
            elif semicolon != -1:
                commandC.updateData("null", line[0:semicolon], line[semicolon+1:len(line)])
            return "111" + commandC.compFunction() + commandC.destFunction() + commandC.jumpFunction()
    
    #Writes the input to the outputFile and adds a jump to next line
    def writeLine(self, inputLine):
        self.outputFile.write(inputLine + "\n")
        
    #Closes the files so that they can be saved properly 
    def closeFiles(self):
        self.inputFile.close
        self.outputFile.close 
            
    #Allows the user to view the access of the table 
    def returnTable(self):
        return self.symbolTable.returnTable()

