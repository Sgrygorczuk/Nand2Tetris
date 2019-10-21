#This is a class made for the NAND 2 Tetris Project Chapter 8, VM Translator
#The goal of this class to go through each line of the .vm code and detrime 
#what is its asm equivalent. It uses only this module which reads the inputed file.
#Creates a new one and writes the transatlion line by line of the VM file. 
#It's an upgraded version of the VM Translator from chapter 7

import os 
import fnmatch

class VM_Parser:
    def __init__(self, inputPath):
        self.nextStack = 0
        self.staticPointer = 0
        self.staticStack = {}
        #File Managment
        self.lines = []
        self.outputFilePath = ""
        self.fileReader(inputPath)
        self.outputFile = open(self.outputFilePath, 'w')
        self.lineCount = len(self.lines)
        #Variables to keep track of
        self.staticCount = 0
        self.currentLine = 0
        self.jumpCount = 0         #Incrmented number to have unique jump labels 
        self.functionName = "Sys.init"
        self.functionNumber = 0
        
        #Symbol Table 
        #It's broken into 3 parts, the Key, the function operation code, 
        #0 Refering to addSubAndOr, 1 refering to notNeg and so on.
        #Then last is register code that correstonds or address 
        #When in function (0) addSubAndOr depdning on key diffrent register code is required
        #When in function (4) popLclArgThisThatTempStatic diffrent address is required 
        #And some functions like (3) push don't require any addtional information 
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
                "poptemp"       : [7,"5"],
                "label"         : [10, ""],
                "goto"          : [11, ""],
                "if-goto"       : [12, ""],
                "function"      : [13, ""],
                "call"          : [14, ""],
                "return"        : [15, ""]
                }
        
        
    #fileReader takes in the input path, checks for if it is a dictonary or a vm file
    #if its just a vm file it performs reading normal. If the dictonary is provided 
    #it scanns for any .vm files then combines all of their read out into one list 
    def fileReader(self, inputPath):
        if os.path.isdir(inputPath):          #Checks if the path is a direcotry 
            #Input File Flowis a collection which is unordered, changeable and indexed. No duplicate members.
            files = self.findFiles('*.vm', inputPath)           #Looks for all of the vm flies that are stored in the dictornary 
            for file in files:                                  #For each file found read it
                self.inputFile = open(file, 'r')                #Opens the file
                info = self.inputFile.readlines()               #Save the lines from the file into a list
                self.staticStackSetUp(info, file)               #Creates pointers for static stacks of diffrent functions from diffrent files
                self.lines = self.lines + info                  #Merge that list with the global one
                self.inputFile.close()                          #Close the currently open file
            #Output File Flow
            found = inputPath.rfind('/')        #Search for the first "/" from the end, that gives us the name of the folder
            self.outputFilePath  = inputPath + "/" + inputPath[found+1:]+ ".asm"
        elif os.path.isfile(inputPath):        #Checks if the path given is a vm file 
            self.inputFile = open(inputPath, 'r')            #Opens the file 
            self.lines = self.inputFile.readlines()            #Reads all of the lines into a list
            self.outputFilePath = inputPath[:len(inputPath)-2]+"asm"   #Create an outputfile path
            self.inputFile.close()            #Close the inputfile 
        
    #Takes the input path of a dictornary and the patter we are searching for 
    #and returns a list of files that match 
    def findFiles(self,pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result
    
        
    #Checks if there is more lines in the file to translate 
    def hasMoreCommands(self):
        if self.currentLine == self.lineCount:
            return False
        else:
            return True 
            
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
        self.lines[self.currentLine] = self.lines[self.currentLine].replace("\n", "")
        index = self.lines[self.currentLine].find("//")
        if index != -1:
            self.lines[self.currentLine] = self.lines[self.currentLine][:index]
        
        #Addition to the comment remvoer that looks for function and call symbols 
        #As they are out of format for the other types having 2 variables to find rather than 1
        line = self.lines[self.currentLine]         #Creates a temorary line that can be tweaked
        found = line.find("function")               #Looks for "function" substring
        foundTwo = line.find("call")                #Looks for "call" substring 
        if found == 0 or foundTwo == 0:             #If Either is found at 0 procced
            if found == 0:                          #If "functinon" is found
                line = line.strip("function ")      #Remvoe function
            if foundTwo == 0:                       #If "call" is found
                line = line.strip("call ")          #Remove call
            index = line.find(" ")                  #Look for where the space occurs between the function name and the k inputs
            self.functionName = line[:index]        #Save the name
            for function in self.staticStack:       #looks through Static Stack
                found = self.functionName.find(function)    #Looks to see which function we are in right now
                if found == 0:                              #If the function matches on in stack dictonary
                    self.staticPointer = self.staticStack[function]     #Save the starting static point
                #print("Function: " + self.functionName + " " + str(found) + " " + function + " " + str(self.staticStack[function]))
            self.functionNumber = int(line[index+1:])   #Saves number of inputs
    
        self.lines[self.currentLine] = self.lines[self.currentLine].replace(" ", "")
    
    #For each line looks through the table to see if it finds any matches "], "popthis"    
    #If it does it sends the information over to chooseTranslation()
    def findSymbol(self):
        for symbol in self.table:
            found = self.lines[self.currentLine].find(symbol)
            if found == 0:
                self.chooseTranslation(symbol)
        
    #Takes in the filePath and all the info that was stored in that file 
    #looks for the name of the class and all instnaces of push static 
    def staticStackSetUp(self, info, filePath):
        counter = 0
        found = filePath.rfind('/')                 #Finds '/' from back to estbalish name of function
        for line in info:                           #Look for all instnaces of pop static
            if line.find("pop static")  != -1:      #if pop static is found 
                counter = counter + 1               #Increase counter 
        if filePath[found+1:-3] != "Sys":           #While not Sys file 
            self.staticStack[filePath[found+1:-3]] = self.nextStack #Add info to dictonary 
            self.nextStack = self.nextStack + counter               #Updated what next pointer should start at
        elif filePath[found+1:-3] == "Sys":         #If it Sys
            self.staticStack["Sys"] = 0             #Static always starts at 0
        
        
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
        elif choice[0] == 10:
            self.label(symbol)
        elif choice[0] == 11:
            self.goto(symbol)
        elif choice[0] == 12:
            self.gotoIf(symbol)
        elif choice[0] == 13:
            self.function()
        elif choice[0] == 14:
            self.call(0)
        elif choice[0] == 15:
            self.returnCall()

    #Bootstrap create the generic stack organziation with the SP being set to 256
    #The other pointers beinging set to 0 for indeifcation that they have not been set yet
    #And initates the call for Sys.init function 
    def bootstrap(self):                                                 
        self.outputFile.write("//Bootstrap\n")   #Comment to inspect 
        self.outputFile.write("@256\n")          #Looks at 256
        self.outputFile.write("D=A\n")           #Saves the number 256 to register D
        self.outputFile.write("@0\n")            #Looks at SP 
        self.outputFile.write("M=D\n")           #Saves 256 to SP
        self.outputFile.write("@1\n")            #Looks at LCL 
        self.outputFile.write("M=0\n")          #Saves -1 to LCL
        self.outputFile.write("@2\n")            #Looks at ARG
        self.outputFile.write("M=0\n")           #Saves -1 to ARG
        self.outputFile.write("@3\n")            #Looks at THIS
        self.outputFile.write("M=0\n")          #Saves -1 to THIS
        self.outputFile.write("@4\n")            #Looks at THAT
        self.outputFile.write("M=0\n")          #Saves -1 to THAT
        self.call(1)                             #Calls Sys.init 
    
    #The addSubAndOr takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform add, sub, and, or functions 
    def addSubAndOr(self,line):                                 #Example Add, SP = 258
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@0\n")                           #Look at SP = 258
        self.outputFile.write("A=M-1\n")                        #Move to SP-1= 257
        self.outputFile.write("D=M\n")                          #Save that value to D
        self.outputFile.write("@0\n")                           #Look at SP = 258
        self.outputFile.write("A=M-1\n")                        #Move SP-1 = 257
        self.outputFile.write("A=A-1\n")                        #Move SP-1 = 256
        self.outputFile.write(line)                             #Grab the line from table,
                                         #for add it's M=D+M, so we add the value of D with 
                                         #value of current memory and save it to that address
        self.updateSP(1)                  #Updates the current place of SP 
    
    
    #The notNeg takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform  not and neg functions 
    def notNeg(self,line):                                   #Example NEG, SP = 258
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@0\n")                        #Look at SP
        self.outputFile.write("A=M-1\n")                     #Move SP-1
        self.outputFile.write(line)                          #Grab the line from table 
                                        #for neg M=-M, so we negate the value the memoery is looking at
        
    #The eqGtLt takes an input of a string assembly that the VM code
    #corresponds to, it has no return. It writes to the outputFile
    #the actions necessary to perform comparison eq, gt and lt functions 
    #Will save 0 for False and -1 for True 
    def eqGtLt(self,line):                 
        #First we need to compare two values so we perform sub
                                                                        #Example Sub, SP = 258
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n") #Comment to inspect 
        self.outputFile.write("@0\n")                                   #Looks at SP = 258
        self.outputFile.write("A=M-1\n")                                #Goes to SP-1 = 257
        self.outputFile.write("D=M\n")                                  #Save that value to D
        self.outputFile.write("@0\n")                                   #Look at SP = 258
        self.outputFile.write("A=M-1\n")                                #Goes to SP-1 = 257
        self.outputFile.write("A=A-1\n")                                #Goes to A-1 = 256
        self.outputFile.write("D=M-D\n")                                #Perfom sub, save result to D
        
        #Here is wehere we start doing the comparison                   #Example EQ
        self.outputFile.write("@JUMP" + str(self.jumpCount) + "\n")     #Create a condital jump
        self.outputFile.write(line)                                     #Based on table we choose the condition for eq
                                                                        #its D;JEQ
        self.outputFile.write("@0\n")                                   #Look at SP = 258
        self.outputFile.write("A=M-1\n")                                #Goes to SP-1 = 257
        self.outputFile.write("A=A-1\n")                                #Goes to A-1 = 256
        self.outputFile.write("M=0\n")                                  #Saves 0 for False
        self.outputFile.write("@EXIT" + str(self.jumpCount) + "\n")     #Sets up EXIT jump over the other choice
        self.outputFile.write("0;JMP\n")                                #Jumps to EXIT 
        self.outputFile.write("(JUMP" + str(self.jumpCount) + ")\n")    #If true JUMP to this part
        self.outputFile.write("@0\n")                                   #Look at SP = 258
        self.outputFile.write("A=M-1\n")                                #Goes to SP-1 = 257
        self.outputFile.write("A=A-1\n")                                #Goes to A-1 = 256
        self.outputFile.write("M=-1\n")                                 #Store -1 in it if True
        self.outputFile.write("(EXIT" + str(self.jumpCount) + ")\n")    #EXIT for False output                               
        self.jumpCount = self.jumpCount + 1                             #Increase jumpCount for unique names for future jumps
        self.updateSP(1)                                                #Updates current SP
        
    #The push takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, it has no return. 
    #It writes to the outputFile the current input into the stack 
    def push(self,line, lineLen):                                                   #Example push constant 7, SP = 256
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")           #Comment to inspect 
        self.outputFile.write("@" + self.lines[self.currentLine][lineLen:] + "\n")  #Gets the address of the index = 7
        self.outputFile.write("D=A\n")                                              #Saves value of 7 to D
        self.outputFile.write("@0\n")                                               #Look at SP
        self.outputFile.write("A=M\n")                                              #Goes to SP 
        self.outputFile.write("M=D\n")                                              #Saves index to current address
        self.updateSP(0)                                                            #Updates SP
    
    #The popLclArgThisThatTempStatic takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, and the corresponding type of action 
    #it has no return. Based on input it provides the address and distance from address 
    #As to where to place the input, with main diffenrce only occuring when Temp or Static is called
    #As temp does not read the address of its orignal location but just starts at that address
    
    def popLclArgThisThatTempStatic(self,line, lineLen, choice):            #Example pop local 2     
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@0\n")                  #Looks at last input of stack SP = 256
        self.outputFile.write("A=M-1\n")  
        self.outputFile.write("D=M\n")                                      #Saves whats in the memory
        self.outputFile.write("@" + line + "\n")                            #Goes to local @1
        if choice == 4:                                                     #If not Temp or Static read the set address to that of the memory at @1
            self.outputFile.write("A=M\n")                                  #LCL points to A 
        if choice == 7:
            for i in range(self.staticPointer):                                #Based on index (2) increment A that number of times
                self.outputFile.write("A=A+1\n")  
        for i in range(int(self.lines[self.currentLine][lineLen:])):      #Based on index (2) increment A that number of times
            self.outputFile.write("A=A+1\n")                                #Move A till we reach Mem[LCL] + 2
        self.outputFile.write("M=D\n")                                      #Save the value into that memory
        self.updateSP(1)                                                    #Update Stack
        
    #The pushLclArgThisThatTempStatic takes an input of a string assembly that the VM code
    #corresponds to and the lenght of the given symbol, and the corresponding type of action 
    #it has no return. Based on input it provides the address and distance from address 
    #As to where to place the were take the memory from tostatic, with main diffenrce only occuring when Temp or Static is called
    #As temp does not read the address of its orignal location but just starts at that address
        
    def pushLclArgThisThatTempStatic(self,line, lineLen, choice):           #Example push static 5
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@" + line + "\n")                            #Look at the address @16
        if choice == 5:                                                     #Static skip
            self.outputFile.write("A=M\n") 
        if choice == 6:
            #print("Function: " + self.functionName + str(self.staticPointer))
            for i in range(self.staticPointer):                                #Based on index (2) increment A that number of times
                self.outputFile.write("A=A+1\n")                                  #Static skip
        for i in (range(int(self.lines[self.currentLine][lineLen:]))):      #For index (5) increment address
            self.outputFile.write("A=A+1\n")                                #Oncea @21 stops
        self.outputFile.write("D=M\n")                                      #Saves whats stored on @21 to D
        self.outputFile.write("@0\n")                                       #Looks at SP
        self.outputFile.write("A=M\n")                                      #Goes to SP 
        self.outputFile.write("M=D\n")                                      #Saves D onto stack                                             
        self.updateSP(0)                                                    #Update stack
    
    #The popPointer takes the lenght of the given symbol, it has no return. 
    #It updates the This and That pointer values, index chooses which one we look at 
    def popPointer(self, lineLen):                             #Example pop pointer 0
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@0\n")                          #Looks at SP
        self.outputFile.write("A=M-1\n")                       #Goes to SP-1  
        self.outputFile.write("D=M\n")                         #Save  data from SP
        if self.lines[self.currentLine][lineLen:] == "0":      #True index == 0
            self.outputFile.write("@3\n")                      #Look at @3 
        elif self.lines[self.currentLine][lineLen:] == "1":    #False index != 1
            self.outputFile.write("@4\n")                      #Skip
        self.outputFile.write("M=D\n")                         #Save that to This pointer
        self.updateSP(1)                                       #Update SP
        
    #The popPointer takes the lenght of the given symbol, it has no return. 
    #Takes the This and That pointer values and puts it on stack, 
    #index chooses which one we look at 
    def pushPointer(self, lineLen):                         #Example push pointer 1
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        if self.lines[self.currentLine][lineLen:] == "0":   #False index != 0
           self.outputFile.write("@3\n")                    #Skip
        elif self.lines[self.currentLine][lineLen:] == "1": #True index == 1
            self.outputFile.write("@4\n")                   #Look at @4
        self.outputFile.write("D=M\n")                      #Save data from address
        self.outputFile.write("@0\n")                       #Look at SP
        self.outputFile.write("A=M\n")                      #Go to SP
        self.outputFile.write("M=D\n")                      #Save data to SP
        self.updateSP(0)                                    #Update SP
    
    #Label takes in a symbol which is used as a jumping point in an goto action, it works under a functionName$LabelName systmer
    def label(self, symbol):
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("(" + self.functionName + "$" + self.lines[self.currentLine][len(symbol):] + ")\n")#Writes label 
    
    #Goto performs a jump and works in conjunction with label as it's desitaition. Uses the same name scheme so that it can reach it's destination 
    def goto(self,symbol):
        self.outputFile.write("//" + self.functionName + "$" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("@" + self.functionName + "$" + self.lines[self.currentLine][len(symbol):] + "\n")#Gets the address of the jump point
        self.outputFile.write("0;JMP\n")#Jumps 
    
    #GotoIf is a conditial jump based on if the top of the stack is equal to 0
    #Used for creating loops 
    def gotoIf(self,symbol):               
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        
        self.outputFile.write("D=0\n")             #Save 0 to D
        self.outputFile.write("@0\n")              #Looks at SP 
        self.outputFile.write("A=M-1\n")           #Goes to SP-1 (Top of Stack)
        self.outputFile.write("D=M-D\n")           #Perfom sub, save result to D
                                                  
        self.updateSP(1)                           #Pops top of stack 
        
        #Here is wehere we start doing the comparison                   #Example EQ
        self.outputFile.write("@" + self.functionName + "$EXIT" + str(self.jumpCount) + "\n") #Gets the exit desitation 
        self.outputFile.write("D;JEQ\n") #If Top of Stack was 0 exit the loop  

                                  
        self.outputFile.write("@" + self.functionName + "$" + self.lines[self.currentLine][len(symbol):] + "\n") #Gets address of the start of the loop   
        self.outputFile.write("0;JMP\n")  #If top of stack was not 0 perform loop   
        self.outputFile.write("(" + self.functionName + "$EXIT" + str(self.jumpCount) + ")\n")    #EXIT for False output 
        self.jumpCount = self.jumpCount + 1     #Increase jumpCount for unique names for future jumps
    
    #Defines a function that can later be called
    def function(self): 
        self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
        self.outputFile.write("(" + self.functionName + ")\n")              #Create a jump to label
        self.outputFile.write("D=0\n")                                      #Saves 0 to D
        for indexI in range(self.functionNumber):                           #For given number n push to LCL
            self.outputFile.write("@1\n")                                       #Look at LCL 
            self.outputFile.write("A=M\n")                                      #Go to LCL Pointer
            #If functionNumber = 3 for loop #2 performs addtion and address increntation appropratlely
            #indexI = 0, no incrment saves to LCL 
            #indexI = 1, saves to LCL + 1
            #indexI = 2, saves to LCL + 2 and so on
            for indexJ in range(indexI):                                    #For loop #2  
                self.outputFile.write("A=A+1\n")                            #Goes to LCL + indexI
            self.outputFile.write("M=D\n")                                  #Adds 0 to LCL stack 
            self.updateSP(0)                                                #Increases SP
            
    #The call function saves all of the infromation of the current function 
    #onto the stack so that the return function can retrive it later 
    #It takes in on input and it's to determin if to write the comment that distinguishes it as a 
    #regualr call of call from bootstrap 
    def call(self, bootstrap):
        if bootstrap == 0:          #If not bootstrap print out comment 
            self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect 
       
        #Push Return Address - THis changes each time in the VM simualtion 
        self.outputFile.write("@" + self.functionName + "_RETURN" + str(self.jumpCount) + "\n")  #Looks at address of return function
        self.outputFile.write("D=A\n")              #Saves address to D
        self.outputFile.write("@0\n")               #Looks at SP
        self.outputFile.write("A=M\n")              #Goes to SP
        self.outputFile.write("M=D\n")              #Push RET onto Stack
        self.updateSP(0)                            #Increase SP
        
        #Push LCL
        self.outputFile.write("@1\n")               #Looks at LCL 
        self.outputFile.write("D=M\n")              #Saves LCL
        self.outputFile.write("@0\n")               #Looks at SP
        self.outputFile.write("A=M\n")              #Goes to SP
        self.outputFile.write("M=D\n")              #Saves LCL to stack             
        self.updateSP(0)                            #Increase SP
        
        #Push ARG
        self.outputFile.write("@2\n")               #Looks at ARG
        self.outputFile.write("D=M\n")              #Saves ARG      
        self.outputFile.write("@0\n")               #Looks at SP
        self.outputFile.write("A=M\n")              #Goes to SP
        self.outputFile.write("M=D\n")              #Saves ARG to top of stack   
        self.updateSP(0)                            #Increase SP
        
        #Push This
        self.outputFile.write("@3\n")               #Looks at THIS
        self.outputFile.write("D=M\n")              #Saves THIS          
        self.outputFile.write("@0\n")               #Looks at SP
        self.outputFile.write("A=M\n")              #Goes to SP
        self.outputFile.write("M=D\n")              #Save THIS to top of stack                    
        self.updateSP(0)                            #Increase SP
        
        #Push That
        self.outputFile.write("@4\n")               #Look at THAT
        self.outputFile.write("D=M\n")              #Saves THAT           
        self.outputFile.write("@0\n")               #Look at SP 
        self.outputFile.write("A=M\n")              #Goes to SP
        self.outputFile.write("M=D\n")              #Save THAT to to of stack                     
        self.updateSP(0)                            #Increase SP
        
        #ARG = SP-n-5       
        self.outputFile.write("@0\n")               #Look at SP
        self.outputFile.write("D=M\n")              #Save SP to D                 
        for indexI in range(5+self.functionNumber): #Do it 5 times plus number of args
             self.outputFile.write("D=D-1\n")       #D-1
        self.outputFile.write("@2\n")               #Look at ARG 
        self.outputFile.write("M=D\n")              #Save new address 
        
        #LCL = SP
        self.outputFile.write("@0\n")               #Look at SP 
        self.outputFile.write("D=M\n")              #Save SP             
        self.outputFile.write("@1\n")               #Look at LCL  
        self.outputFile.write("M=D\n")              #Save SP to LCL 
        
        #goto f         
        self.outputFile.write("@" + self.functionName + "\n")  #Get address of function label 
        self.outputFile.write("0;JMP\n")                       #Go to label  
        
        #return address
        self.outputFile.write("(" + self.functionName + "_RETURN" + str(self.jumpCount) + ")\n")  #Creates a return label 
        self.jumpCount = self.jumpCount + 1
        
    #the returnCall or just Return takes all the infromation from a function call and brings it back such
    #that we go back to the orignal function from which the call was made from 
    def returnCall(self):
         self.outputFile.write("//" + self.lines[self.currentLine] + "\n")   #Comment to inspect
         #FRAME = LCL - Sets the LCL to Temp @13
         self.outputFile.write("@1\n")              #Looks at current LCL
         self.outputFile.write("D=M\n")             #Saves Address it points to 
         self.outputFile.write("@13\n")             #Looks at Temp @13
         self.outputFile.write("M=D\n")             #Saves current LCL to @13 now it's FRAME
         
         #RET = *(FRAME-5) - Saves the Return address to Temp @14
                                                    #Address FRAME is pointing to is still stored in D
         for indexI in range(5):                    #Calcaute FRAME - 5 
             self.outputFile.write("D=D-1\n")       #Move FRAME - 1 
         self.outputFile.write("A=D\n")             #Go to FRAME - 5 
         self.outputFile.write("D=M\n")             #Save the RET to  D
         self.outputFile.write("@14\n")             #Looks @14
         self.outputFile.write("M=D\n")             #Stores RET at @14
         
         #ARG* = pop() - Takes the argument from SP and moves it to current ARG stack 
         self.outputFile.write("@0\n")              #Looks at SP 
         self.outputFile.write("A=M-1\n")           #Moves SP-1 
         self.outputFile.write("D=M\n")             #Saves whatever is on top of the stack
         self.outputFile.write("@2\n")              #Looks at ARG
         self.outputFile.write("A=M\n")             #Goes to ARG 
         self.outputFile.write("M=D\n")             #Saves top of stack to current ARG
         
         #SP = ARG+1 - Sets SP to be current ARG + 1 
         self.outputFile.write("@2\n")              #Look at ARG
         self.outputFile.write("D=M+1\n")           #Saves ARG+1
         self.outputFile.write("@0\n")              #Look at SP
         self.outputFile.write("M=D\n")             #Save SP = ARG + 1
        
         #THAT = *(FRAME-1) - Replaces current THAT with pervious function THAT
         self.outputFile.write("@13\n")             #Look at FRAME
         self.outputFile.write("A=M-1\n")           #Go to FRAME - 1
         self.outputFile.write("D=M\n")             #Saves old THAT
         self.outputFile.write("@4\n")              #Look at THAT
         self.outputFile.write("M=D\n")             #Replace current THAT with old THAT
         
         #THAT = *(FRAME-2) - Replaces current THIS with pervious function THIS
         self.outputFile.write("@13\n")             #Look at FRAME
         self.outputFile.write("A=M-1\n")           #Go to FRAME-1
         self.outputFile.write("A=A-1\n")           #Go to A-1
         self.outputFile.write("D=M\n")             #Save old THIS
         self.outputFile.write("@3\n")              #Look at THIS
         self.outputFile.write("M=D\n")             #Replace current THIS with old THIS
         
         #ARG = *(FRAME-3) - Replaces current ARG with pervious function ARG
         self.outputFile.write("@13\n")             #Look at FRAME
         self.outputFile.write("A=M-1\n")           #Go to FRAME-1
         for indexI in range(2):                    #Repeate 2 times
             self.outputFile.write("A=A-1\n")       #Go to A-1
         self.outputFile.write("D=M\n")             #Save old ARG
         self.outputFile.write("@2\n")              #Look at ARG
         self.outputFile.write("M=D\n")             #Replace current ARG with old ARG         
         
         #LCL = *(FRAME-4) - Replaces current LCL with pervious function LCL
         self.outputFile.write("@13\n")             #Look at FRAME
         self.outputFile.write("A=M-1\n")           #Go to FRAME-1
         for indexI in range(3):                    #Repeate 3 times
             self.outputFile.write("A=A-1\n")       #Go to A-1
         self.outputFile.write("D=M\n")             #Save old LCL
         self.outputFile.write("@1\n")              #Look at LCL
         self.outputFile.write("M=D\n")             #Replace current LCL with old LCL   
         
         #GoTo Ret
         self.outputFile.write("@14\n")             #Look at RET
         self.outputFile.write("A=M\n")             #Go to RET
         self.outputFile.write("0;JMP\n")           #Jumps to RET label 
         
    #The updateSP takes in one input which detrimes if the stack is increased or decraesed, 
    #it has no return. It writes to the outputFile the current postion of the stack pointer 
    def updateSP(self, addOrSub):                         
        self.outputFile.write("@0\n")                           #Look at address of SP
        if addOrSub == 0:
            self.outputFile.write("M=M+1\n")                          #Save current value of SP to adress of SP
        else:
            self.outputFile.write("M=M-1\n") 
            
    #Closese the output file 
    def closeFiles(self):
        self.outputFile.close() 


    