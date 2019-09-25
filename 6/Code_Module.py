#This is a class made for the NAND 2 Tetris Project Chapter 6, Assembler 
#The goal of this class is to take the C Type Instruction break it down
#and obtain the desired binary equvialent of the symbolic representation 

#The class contains 3 string variables
#dest which translates the symbolic destation to the binary 
#jump which translates the symbolic jump instruction to the binary 
#comp which translates the symbolic computation to the binary 
#It also holds the three tables which Hack assembler recongizes 
class Code:
    def __init__(self, dest = "null", comp = "0", jump = "null"):
        self.dest = dest
        self.comp = comp
        self.jump = jump
        
        self.destTable = {
                "null":"000", 
                "M"   :"001",
                "D"   :"010",
                "MD"  :"011",
                "A"   :"100",
                "AM"  :"101",
                "AD"  :"110",
                "AMD" :"111"
        }
        #A and M comp are mostly the same with only diffrence being A starts with
        #0 and M starts with 1
        self.compTable = {
                "0"    :"0101010", 
                "1"    :"0111111",
                "-1"   :"0111010",
                "D"    :"0001100",
                "A"    :"0110000",
                "!D"   :"0001101",
                "!A"   :"0110001",
                "-D"   :"0001111",
                "-A"   :"0110011", 
                "D+1"  :"0011111",
                "A+1"  :"0110111",
                "D-1"  :"0001110",
                "A-1"  :"0110010",
                "D+A"  :"0000010",
                "D-A"  :"0010011",
                "A-D"  :"0000111",
                "D&A"  :"0000000",
                "D|A"  :"0010101",
                "M"    :"1110000",
                "!M"   :"1110001",
                "-M"   :"1110011",
                "M+1"  :"1110111",
                "M-1"  :"1110010",
                "D+M"  :"1000010",
                "D-M"  :"1010011",
                "M-D"  :"1000111",
                "D&M"  :"1000000", 
                "D|M"  :"1010101"
        }
        
        self.jumpTable = {
                "null":"000", 
                "JGT" :"001",
                "JEQ" :"010",
                "JGE" :"011",
                "JLT" :"100",
                "JNE" :"101",
                "JLE" :"110",
                "JMP" :"111"
        }
    
    #Allows for change of the dest, comp and jump variables 
    def updateData(self, dest, comp, jump):
        self.dest = dest
        self.comp = comp
        self.jump = jump
    #Returns the value of the dest as per the destTable 
    def destFunction(self):
        return self.destTable[self.dest]
        
    #Returns the value of the comp as per the compTable 
    def compFunction(self):
        return self.compTable[self.comp]
    
    #Returns the value of the jump as per the jumpTable 
    def jumpFunction(self):
        return self.jumpTable[self.jump]