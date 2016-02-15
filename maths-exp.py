# Necessary imports
import json


##############################################################
# Data structure for holding variables, expressions and values
##############################################################

class Tree:
	
    def __init__(self, key, operator, children = []):
        
        # Every tree has a key, an operator and a list of children
        # Any of the three may be None or empty respectively
        # depending on what is being stored
        
        self.key = key
        self.operator = operator
        self.children = children


    def addChild(self,child):
	    # Append new child to the parent's array of children
        self.children.append(child)
         
         
    def getVariableValue(self, targetVariable, tree, index):
            
        # Gather the variables (the RHS) in a list
        # We don't use the list of root's children directly to avoid affecting the structure
        variableList = [self.children[x] for x in range(index)]
        
        # Reverse the list for searching (to return the most recent value)
        variableList.reverse()
        
        # Check our target variable exists; search the list of variables
        for variableFromList in variableList:
        
            # Search match
            if targetVariable == variableFromList.key:
            
                # Reverse the original list of variables
                # So we can obtain the correct index for getValue()
                variableList.reverse()
                
                # Return the variable's value
                return variableFromList.getValue(tree, variableList.index(variableFromList))
    
    
    def getValue(self,tree,index):
		
        if self.operator == "integer":
            # Integer
            
            return self.children[0]
            
        elif self.operator == "variable":
            # Variable
            
            # We need to traverse the tree to find the variable's value
            
            targetVariable = self.children[0]
            
            return root.getVariableValue(targetVariable, tree, index)
                                
        elif self.operator == "tuple":
            # Tuple
            
            # Return the pair by using (a, b) format
            return (self.children[0].getValue(tree,index), self.children[1].getValue(tree,index))
            
        elif self.operator == "set":
            # Set
            
            # We"ll use a list to represent the set
            # To avoid future complications (as advised in emails)
            
            # Build (and return) a new list of the children's values
            return [child.getValue(tree,index) for child in self.children]
            
        elif self.operator == "equal":
            # Equality test
            
            # Get value of both sides; left hand side & right hand side
            lhs = self.children[0].getValue(tree,index)
            rhs = self.children[1].getValue(tree,index)
            
            # Boolean that checks if the LHS and RHS are both sets (lists in this implementation)
            bothSet = isinstance(lhs, list) and isinstance(rhs, list)
            
            # Check if they are both sets
            if bothSet:
            
                # Check all elements of LHS in RHS & all elements of RHS in LHS
                # This allows us to account for possibly duplicate members
                if all(l in lhs for l in rhs) and all(l in rhs for l in lhs):
                    return 1
                else:
                    return 0
                    
            else:
            
                # Check if they are equal or not (and return appropriate boolean)
                return 1 if lhs == rhs else 0
                
        elif self.operator == "member":
            # Membership test
            
            # First, get the values
            lhs = self.children[0].getValue(tree, index)
            rhs = self.children[1].getValue(tree, index)
            
            # Check the RHS is a set (list in this implementation)
            if isinstance(rhs, list):
            
                # Check whether the LHS is a "member of" the RHS
                # And return appropriate true/false boolean value
                return 1 if lhs in rhs else 0
                    
            else:
                
                # Not a set, so it's not possible
                # To check whether the LHS is a "member of" the RHS
                return 0
                
        else:
            # We don"t have a definition for this operator
            return "undefined!"


    def insertChild(self, key, value):
	    
        # First, check if the value is an int
        if isinstance(value, int):
        
            # If so, store a subtree within the root tree
            # with "integer" as the operator and the integer as a child
            self.addChild(Tree(key, "integer", [value]))
            
        elif isinstance(value, dict):
            # If the value is a dictionary, consider whether it
            # has "operator" as a key OR "variable" as a key
            
            if "operator" in value:
            
                # We have an operator to store, along with arguments
                operator = value["operator"]
                arguments = value["arguments"]
                
                # Construct the subtree with the key, operator and (for now) an empty set of children
                subTree = Tree(key, operator, [])
                
                # For each nested argument
                for arg in arguments:
                    # Store the argument in the subtree
                    subTree.insertChild(None, arg)
                
                # Add the subtree to the parent tree
                self.addChild(subTree)
                
            else:
                # Add variable subtree
                self.addChild(Tree(key, "variable", value.values()))
        
            
    def writeToFile(self):
    
        # Enumerate the list (ie attach an index to each child)
        # And loop through
        for index, child in enumerate(self.children):
            
            # Beginning of the expression
            file.write("let "),
            file.write(str(child.key)),
            file.write(" be "),
            
            # For each variable, find the value
            value = child.getValue(self, index)
            
            # Now write the value to the file
            writeValue(value)
            
            # End the expression and start a new line
            file.write(";\n")
            
##############################################################

##############################################################
# Printing function
##############################################################
    
def writeValue(value):
    
    if isinstance(value, int):
    
        # Simply write the int value
        file.write(str(value))
        
    elif isinstance(value, list):
    
        # Open set
        file.write("{"),
        
        for pos, member in enumerate(value, start=1):
            
            # Recursive call on each member of the set
            writeValue(member)
        
            # Only include a comma if it is not the last member
            if pos < len(value):
                file.write(", ")
            
        # Close the set
        file.write("}")
        
    elif isinstance(value, tuple):
        
        # Open tuple
        file.write("("),
        
        # Recursive call on LHS of tuple
        writeValue(value[0])
        
        # Seperate items of tuple
        file.write(", ")
        
        # Recursive call on RHS of tuple
        writeValue(value[1])
            
        # Close tuple
        file.write(")")   
        
    else:
        
        # Some kind of error/notice; probably "undefined!"
        file.write(str(value))         
    
##############################################################



##############################################################
# Store the declarations
##############################################################

root = Tree(1, None, []) # The root tree node

def storeDeclarations(data):
    
    # For every declaration on the top level of the JSON input file
    for declaration in data["declaration-list"]:
    
        # The variable and value of the declaration
        variable = declaration["declared-variable"]
        value = declaration["value"]
        
        # Insert the variable and its value, which itself will be a tree of subtrees
        # These subtrees will be used to determine the variable's true value
        root.insertChild(variable, value)

##############################################################



##############################################################
# Run the program's sequence of events
##############################################################

# Load the JSON input test case file
with open("input.json") as input:
    
    # Open the output file in writable mode
    file =  open("output.txt", "w")
    
    # Store the input loaded from JSON
    storeDeclarations(json.load(input))

# Write the evaluated expressions to the output file
# by recursively traversing through the entire structure
# beginning from the root
root.writeToFile()

##############################################################
