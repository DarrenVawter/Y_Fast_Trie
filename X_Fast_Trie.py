# -*- coding: utf-8 -*-
"""


@author: Darren Vawter
"""

#TODO: add description above

from math import ceil;
from Helper_Functions import Check_Int

class X_Fast_Trie:
        
    def __init__(self, max_bits=8):
        
        # Validate that the number of bits needed is in the discrete range (0,inf)
        Check_Int(max_bits,(0,"inf"),"max_bits");
        
        # Calculate the height of x-fast trie
        self.height = 1+ceil(max_bits);
        
        # Calculate the bound the maximum int in the trie
        self.max_int_bound = 2**max_bits;
        self.max_bits = max_bits;
        
        # Create a hash table for each level of the trie
        self.layers = [{} for _ in range(self.height)];
               
        # Initialize the loop link leaf to make the linked list circular
        self.loop_link = self.Leaf(None, None);
        self.loop_link.left = self.loop_link;
        self.loop_link.right = self.loop_link;
        self.loop_link.count = -1;
        
        # Initialize the root leaf to point at the loop link
        # (Note: This is just to inject the loop link into the linked list)
        self.layers[0][0] = self.Leaf(self.loop_link, self.loop_link);
                        
    def Insert(self, value):
                
        # Validate that the number of bits needed is in the discrete range (0,inf)
        Check_Int(value,(-1,self.max_int_bound),"value");
                 
        # Check if this value is already in the list
        if(value in self.layers[self.height-1]):
            
            # If so, just increment the leaf's count
            self.layers[self.height-1][value].count += 1;
            return;
        
        # Find predecessor and successor leaves
        [predecessor, successor] = self.__Find_Adjacents(value);
        
        print(predecessor.value,successor.value)
        
        # Insert the new leaf between the two in the bottom layer
        inserted_leaf = self.Leaf(predecessor, successor, value);
        self.layers[self.height-1][value] = inserted_leaf
        predecessor.right = inserted_leaf
        successor.left = inserted_leaf
        
        # Step up through the layers of the trie for which no ancestor exists
        last_leaf = inserted_leaf;
        level_traversal = value%2;
        level_value = value>>1;
        for level in reversed(range(self.height-1)):
                        
            # Check if the ancestor at this level does not yet exist
            if(level_value not in self.layers[level]):
                
                # If so, create the ancestor leaf
                ancestor = self.Leaf(None,None);
                self.layers[level][level_value] = ancestor;
                            
            else:
            
                # Otherwise, assign ancestor to the pre-existing leaf    
                ancestor = self.layers[level][level_value];
                                                          
            # Check if the inserted val is a left descendant of this ancestor
            if(level_traversal == 0):
                    
                # Point the ancestor's left pointer to the last leaf
                ancestor.left = last_leaf;
                
                # Check if this ancestor is new
                if(ancestor.right == None):
                    
                    # If so, its right-most left-descendant is the inserted leaf
                    ancestor.right = inserted_leaf;                    
                
                # Check if this ancestor has right-descendants
                elif(ancestor.right.count == 0):
                    
                    # If so, all updating is done
                    continue;       
                    
                # Check if the current left pointer is the loop link                
                #    or if the value is the left-most right-descendant of this ancestor
                elif(ancestor.right.count == -1 
                     or ancestor.right.value > value):
            
                    # If so, its right-most left-descendant is the inserted leaf
                    ancestor.right = inserted_leaf;               
                
            # Check if the inserted val is a right descendant of this ancestor
            elif(level_traversal == 1):
                    
                # Point the ancestor's right pointer to the last leaf
                ancestor.right = last_leaf;
                
                # Check if this ancestor is new
                if(ancestor.left == None):
                    
                    # If so, its left-most right-descendant is the inserted leaf
                    ancestor.left = inserted_leaf;                    
                
                # Check if this ancestor has left-descendants
                elif(ancestor.left.count == 0):
                    
                    # If so, all updating is done
                    continue;                   
                    
                # Check if the current left pointer is the loop link                
                #    or if the value is the left-most right-descendant of this ancestor
                elif(ancestor.left.count == -1 
                     or ancestor.left.value > value):
            
                    # If so, its left-most right-descendant is the inserted leaf
                    ancestor.left = inserted_leaf;       
                    
            print("Inserted",level_value,"at level",level,ancestor);
                    
            # Update for next iteration
            last_leaf = ancestor;      
            level_traversal = level_value%2;
            level_value = level_value>>1;     
        
    def Contains(self, value):
        return value in self.layers[self.height-1];
    
    def Min(self):
        return self.loop_link.right.value;
    
    def Max(self):
        return self.loop_link.left.value;
        
    def __Find_Adjacents(self, value):
                  
        # Find the lowest ancestor of this number
        [lowest_ancestor, ancestor_level] = self.__Find_Lowest_Ancestor(value);
        print(lowest_ancestor)
        
        # Check if this value is already in the list
        if(lowest_ancestor.count > 0):
            
            # If so, just grab its adjacents
            return [lowest_ancestor.left, lowest_ancestor.right];
            
        # Get the traversal bit for this value at the ancestor's level
        ancestor_traversal = (value>>(self.height-2-ancestor_level))%2;
        
        # Check if the value is a left child of the ancestor
        if(ancestor_traversal == 0):
            
            # If so, the ancestor's left pointer is its left-most right-descendant
            successor = lowest_ancestor.left;
            # That descendant's left pointer is the predecessor of the value
            predecessor = successor.left;

            return [predecessor, successor];
        
        # Check if the value is a right child of the ancestor
        if(ancestor_traversal == 1):
            
            # If so, the ancestor's right pointer is its right-most left-descendant
            predecessor = lowest_ancestor.right;
            # That descendant's left pointer is the predecessor of the value
            successor = predecessor.right;
            
            return [predecessor, successor];
        
    def __Find_Lowest_Ancestor(self, value):
        
        # Initialize bounds of binary search among levels
        min_level = 0;
        max_level = self.height;
        
        # Iterative binary search among levels to find lowest ancestor
        while(min_level != max_level):
                        
            # Find a central layer
            level = ceil((max_level-min_level)/2)+min_level;
            
            # Check if the central layer contains the prefix
            if(value>>(self.height-1-level) in self.layers[level]):
                # If this layer contains the prefix, the lowest ancestor is at least this level
                min_level = level;
            else:
                # If this layer does not contain the prefix, the lowest ancestor is at most 1 before this level
                max_level = level-1;
                
        # Both max and min level are now the level of the lowest ancestor
        level = max_level;
        
        # Return the ancestor leaf itself and its level
        return [self.layers[level][value>>(self.height-1-level)], level];
           
    class Leaf:
          
        #left -> left_most_descendant
        #right -> right_most_descendant
        def __init__(self, left, right, value=None):
            
            #TODO: if one points to self and the other doesn't that's an error
            self.left = left;
            self.right = right;
            self.value = value;
            if(value is not None):
                self.count = 1;
            else:
                self.count = 0;
            
            
            
test = X_Fast_Trie();
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            