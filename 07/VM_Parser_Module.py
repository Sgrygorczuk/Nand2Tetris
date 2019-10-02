#This is a class made for the NAND 2 Tetris Project Chapter 7, VM Translator
#The goal of this class to go through each line of the .vm code and detrime 
#what is its asm equivalent. It uses only this module which reads the inputed file.
#Creates a new one and writes the transatlion line by line of the VM file. 

class VM_Parser:
    def __init__(self, inputFile):
        self.inputFile = open(inputFile, 'r')
        self.outputFile = open(inputFile[:len(inputFile)-2]+"asm", 'w')
        self.currentLine = 0
        self.SP = 256
        self.index = 0
        self.currentLine = 0
        self.jumpCount = 0
        self.lines = self.inputFile.readlines()
        self.lineCount = len(self.lines)
        self.table = {
                "add"           : [0,"M=D+M\n"], 
                "sub"           : [0,"M=M-D\n"],
                "neg"           : [1,"M=-M\n"],
                "eq"            : [2,"D;JEQ\n"], 
                "gt"            : [2,"D;JGT\n"],
                "lt"            : [2,"D;JLT\n"],
                "and"           : [0,"M=M&D\n"], 
                "or"            : [0,"M=M|D\n"], 
                "not"           : [1,"M=!M\n"],
                "pushconstant"  : [3,""],           #Follows SP
                "pushargument"  : [5,"2"],          #Pointer Address to ARG stored @2
                "pushlocal"     : [5,"1"],          #Pointer Address to LCL is stored @1
                "pushstatic"    : [6, "16"],        #Static Stack starts @16
                "pushthis"      : [5,"3"],          #Pointer Address to THIS stored @3
                "pushthat"      : [5,"4"],          #Pointer Address to THAT stored @4
                "pushpointer"   : [9,""],           #Controlled by index 
                "pushtemp"      : [6,"5"],          #Temp Stack starts @5
                "popargument"   : [4,"2"], 
                "poplocal"      : [4,"1"],
                "popstatic"     : [7,"16"],
                "popthis"       : [4,"3"],
                "popthat"       : [4,"4"],
                "poppointer"    : [8,""], 
                "poptemp"       : [7,"5"]
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
            self.commentRemover()
            self.findSymbol()
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
    
    #For each line looks through the table to see if it finds any matches 
    #If it does it sends the information over to chooseTranslation()
    def findSymbol(self):
        for symbol in self.table:
            found = self.lines[self.currentLine].find(symbol)
            if found == 0:
                self.chooseTranslation(symbol)
   
    #Takes in one input of the current symbol based on the table it 
    #chooses which translation function it has to initate 
    def chooseTranslation(self, symbol):
        choice = self.table[symbol]
        if choice[0] == 0:
            self.addSubAndOr(choice[1])
        elif choice[0] == 1:
            self.notNeg(choice[1])
        elif choice[0] == 2:
            self.eqGtLt(choice[1])
        elif choice[0] == 3:
            self.push(choice[1], len(symbol))
        elif choice[0] == 4 or choice[0] == 7:
            self.popLclArgThisThatTempStatic(choice[1], len(symbol),choice[0])
        elif choice[0] == 5 or choice[0] == 6:
            self.pushLclArgThisThatTempStatic(choice[1], len(symbol),choice[0])
        elif choice[0] == 8:
            self.popPointer(len(symbol))
        elif choice[0] == 9:
            self.pushPointer(len(symbol))

    #The addSubAndOr takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform add, sub, and, or functions 
    def addSubAndOr(self,line):                                 #Example Add, SP = 258
        self.outputFile.write("@" + str(self.SP-1) + "\n")      #Grab the value from SP = 257
        self.outputFile.write("D=M\n")                          #Save that value to D
        self.outputFile.write("@" + str(self.SP-2) + "\n")      #Grab the value from SP = 256
        self.outputFile.write(line)                             #Grab the line from table,
                                         #for add it's M=D+M, so we add the value of D with 
                                         #value of current memory and save it to that address
        self.SP = self.SP - 1            #Move the SP back one space
        self.updateSP(1)                  #Updates the current place of SP 
    
    
    #The notNeg takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform  not and neg functions 
    def notNeg(self,line):                                   #Example NEG, SP = 258
        self.outputFile.write("@" + str(self.SP-1) + "\n")   #Grab the value from SP = 257
        self.outputFile.write(line)                          #Grab the line from table 
                                        #for neg M=-M, so we negate the value the memoery is looking at
        
    #The eqGtLt takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform comparison eq, gt and lt functions 
    #Will save 0 for False and -1 for True 
    def eqGtLt(self,line):                 
        #First we need to compare two values so we perform sub
                                                                        #Example Sub, SP = 258
        self.outputFile.write("@" + str(self.SP-1) + "\n")              #Grab the value from SP = 257
        self.outputFile.write("D=M\n")                                  #Save that value to D
        self.outputFile.write("@" + str(self.SP-2) + "\n")              #Grab the value from SP = 256
        self.outputFile.write("D=M-D\n")                                #Perfom sub, save result to D
        
        #Here is wehere we start doing the comparison                   #Example EQ
        self.outputFile.write("@JUMP" + str(self.jumpCount) + "\n")     #Create a condital jump
        self.outputFile.write(line)                                     #Based on table we choose the condition for eq
                                                                        #its D;JEQ
        self.outputFile.write("@" + str(self.SP-2) + "\n")              #Sets the address where to save
        self.outputFile.write("M=0\n")                                  #Saves 0 for False
        self.outputFile.write("@EXIT" + str(self.jumpCount) + "\n")     #Sets up EXIT jump over the other choice
        self.outputFile.write("0;JMP\n")                                #Jumps to EXIT 
        self.outputFile.write("(JUMP" + str(self.jumpCount) + ")\n")    #If true JUMP to this part
        self.outputFile.write("@" + str(self.SP-2) + "\n")              #Set up address we're saving to
        self.outputFile.write("M=-1\n")                                 #Store -1 in it if True
        self.outputFile.write("(EXIT" + str(self.jumpCount) + ")\n")    #EXIT for False output
        self.SP = self.SP - 1                                           #Decrease SP
        self.jumpCount = self.jumpCount + 1                             #Increase jumpCount for unique names for future jumps
        self.updateSP(1)                                                 #Updates current SP
        
    #The push takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, it has no return. 
    #It writes to the outputFile the current input into the stack 
    def push(self,line, lineLen):                                                   #Example push constant 7, SP = 256
        self.outputFile.write("@" + self.lines[self.currentLine][lineLen:] + "\n")  #Gets the address of the index = 7
        self.outputFile.write("D=A\n")                                              #Saves value of 7 to D
        self.outputFile.write("@" + str(self.SP) + "\n")                            #Looks at current SP 
        self.outputFile.write("M=D\n")                                              #Saves index to current address
        self.SP = self.SP + 1                                                       #Increases SP
        self.updateSP(0)                                                             #Updates SP
    
    #The popLclArgThisThatTempStatic takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, and the corresponding type of action 
    #it has no return. Based on input it provides the address and distance from address 
    #As to where to place the input, with main diffenrce only occuring when Temp or Static is called
    #As temp does not read the address of its orignal location but just starts at that address
    
    def popLclArgThisThatTempStatic(self,line, lineLen, choice):            #Example pop local 2     
        self.outputFile.write("@" + str(self.SP-1) + "\n")                  #Looks at last input of stack SP = 256
        self.outputFile.write("D=M\n")                                      #Saves whats in the memory
        self.outputFile.write("@" + line + "\n")                            #Goes to local @1
        if choice == 4:                                                     #If not Temp or Static read the set address to that of the memory at @1
            self.outputFile.write("A=M\n")                                  #LCL points to A 
        for i in (range(int(self.lines[self.currentLine][lineLen:]))):      #Based on index (2) increment A that number of times
            self.outputFile.write("A=A+1\n")                                #Move A till we reach Mem[LCL] + 2
        self.outputFile.write("M=D\n")                                      #Save the value into that memory
        self.SP = self.SP - 1                                               #Decrease SP
        self.updateSP(1)                                                    #Update Stack
        
    #The pushLclArgThisThatTempStatic takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, and the corresponding type of action 
    #it has no return. Based on input it provides the address and distance from address 
    #As to where to place the were take the memory from tostatic, with main diffenrce only occuring when Temp or Static is called
    #As temp does not read the address of its orignal location but just starts at that address
        
    def pushLclArgThisThatTempStatic(self,line, lineLen, choice):           #Example push static 5
        self.outputFile.write("@" + line + "\n")                            #Look at the address @16
        if choice == 5:                                                     #Static skip
            self.outputFile.write("A=M\n")                                  #Static skip
        for i in (range(int(self.lines[self.currentLine][lineLen:]))):      #For index (5) increment address
            self.outputFile.write("A=A+1\n")                                #Oncea @21 stops
        self.outputFile.write("D=M\n")                                      #Saves whats stored on @21 to D
        self.outputFile.write("@" + str(self.SP) + "\n")                    #Goes to SP
        self.outputFile.write("M=D\n")                                      #Saves D onto stack
        self.SP = self.SP + 1                                               #Increment stack
        self.updateSP(0)                                                    #Update stack
    
    
    #The popPointer takes the lenght of the given symbol, it has no return. 
    #It updates the This and That pointer values, index chooses which one we look at 
    def popPointer(self, lineLen):                             #Example pop pointer 0
        self.outputFile.write("@" + str(self.SP-1) + "\n")     #Look at last SP address
        self.outputFile.write("D=M\n")                         #Save  data from SP
        if self.lines[self.currentLine][lineLen:] == "0":      #True index == 0
            self.outputFile.write("@3\n")                      #Look at @3 
        elif self.lines[self.currentLine][lineLen:] == "1":    #False index != 1
            self.outputFile.write("@4\n")                      #Skip
        self.outputFile.write("M=D\n")                         #Save that to This pointer
        self.SP = self.SP - 1                                  #Decrement SP
        self.updateSP(1)                                       #Update SP
        
    #The popPointer takes the lenght of the given symbol, it has no return. 
    #Takes the This and That pointer values and puts it on stack, 
    #index chooses which one we look at 
    def pushPointer(self, lineLen):                         #Example push pointer 1
        if self.lines[self.currentLine][lineLen:] == "0":   #False index != 0
           self.outputFile.write("@3\n")                    #Skip
        elif self.lines[self.currentLine][lineLen:] == "1": #True index == 1
            self.outputFile.write("@4\n")                   #Look at @4
        self.outputFile.write("D=M\n")                      #Save data from address
        self.outputFile.write("@" + str(self.SP) + "\n")    #Look at SP
        self.outputFile.write("M=D\n")                      #Save data to SP
        self.SP = self.SP + 1                               #Incrment SP
        self.updateSP(0)                                    #Update SP
    
    #The updateSP takes in one input which detrimes if the stack is increased or decraesed, 
    #it has no return. It writes to the outputFile the current postion of the stack pointer 
    def updateSP(self, addOrSub):                         
        self.outputFile.write("@0\n")                           #Look at address of SP
        if addOrSub == 0:
            self.outputFile.write("M=M+1\n")                          #Save current value of SP to adress of SP
        else:
            self.outputFile.write("M=M-1\n") 
    
    #Closese the input and output files
    def closeFiles(self):
        self.inputFile.close()
        self.outputFile.close() 


    