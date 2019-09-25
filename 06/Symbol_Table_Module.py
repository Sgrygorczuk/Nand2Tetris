#This is a class made for the NAND 2 Tetris Project Chapter 6, Assembler 
#The goal of this class is create a symbol table for user defined symbols 
#It will see if the symbol exits and if it does not it adds it to defined address

class symbolTable:
    def __init__(self):
        self.currentAddress = 16
        self.symbolsTabel = {
        }
    
    #If the input does not already exist in the table we add a new one along with its address
    #We take the current address and translate it into binary
    #We use an extened string to make sure the address is 16 bit 
    #Once a new entry has been added to the tabel we increase the current address   
    #We have two address assgiments ones which go forward from the 16th address and ones
    #that are part of the jump which used given address 
    def addEntry(self,inputSymbol, address = 0, jumpToLabel = 0):
        if self.contains(inputSymbol) == False:
            extend = "0000000000000000"
            if jumpToLabel == 1: 
                lenght = len('{0:b}'.format(address))
                self.symbolsTabel.update({inputSymbol : extend[:16-lenght] + '{0:b}'.format(address)})
            elif jumpToLabel == 0:
                lenght = len('{0:b}'.format(int(self.currentAddress)))
                self.symbolsTabel.update({inputSymbol : extend[:16-lenght] + '{0:b}'.format(int(self.currentAddress))})
                self.currentAddress = self.currentAddress + 1

    
    #Checks if the symbol already exits in the table
    def contains(self, inputSymbol):
        confrirm = self.symbolsTabel.get(inputSymbol)
        if(confrirm == None):
            return False
        else:
            return True
    
    #Returns the current address 
    def getCurrentAddress(self):
        return self.currentAddress
    
    #Returns the address of given input if the input exits in the table 
    def getAddress(self, inputSymbol):
        if self.contains(inputSymbol):
            return self.symbolsTabel[inputSymbol]
    
    #Returns the table, mostly to print out and check the contents manually 
    def returnTable(self):
        return self.symbolsTabel