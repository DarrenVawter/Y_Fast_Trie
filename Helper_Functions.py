# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:25:51 2022

@author: Darren
"""

def Check_Int(value, domain=("-inf","inf"), value_name="value"):
        
    # Check that variable name is a string
    if(type(value_name) != str):
        raise(TypeError("The name of the value to check must be a string."));
        
    # Validate domain
    if(type(domain) != tuple):
        raise(TypeError("The domain of ["+value_name+"] must be a tuple."));
    if( (type(domain[0]) != int and domain[0] != "-inf" and domain[0] != "inf") or (type(domain[1]) != int and domain[1] != "-inf" and domain[1] != "inf") ):
        raise(TypeError("The bounds of [domain] must be integers, -inf, or inf."));
    if( type(domain[0]) == int and type(domain[1]) == int and domain[1] <= domain[0] or domain[0] == "inf" or domain[1] == "-inf"):
        raise(ValueError("The bounds of [domain] must be ascending."));

    # Validate that it is an int being checked        
    if(type(value) != int):
        raise(TypeError("["+value_name+"] must be an integer."));
        
    # Check that int is within bounds
    if(domain[0] != "-inf" and domain[1] != "inf"):            
        # Both bounds are finite, check both
        if(value <= domain[0] or value >= domain[1]):
            raise(ValueError("["+value_name+"] must be in the integer range ("+str(domain[0])+","+str(domain[1])+")."));     
    if(domain[0] == "-inf"):            
        # Lower bound is infinite, only check upper bound
        if(value >= domain[1]):
            raise(ValueError("["+value_name+"] must be in the integer range ("+str(domain[0])+","+str(domain[1])+").")); 
    elif(domain[1] == "inf"):            
        # Upper bound is infinite, only check lower bound
        if(value <= domain[0]):
            raise(ValueError("["+value_name+"] must be in the integer range ("+str(domain[0])+","+str(domain[1])+")."));            
    else:
        # Both bounds are infinite, no need to check
        pass;