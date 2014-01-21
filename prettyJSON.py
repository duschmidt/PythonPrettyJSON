def prettyJsonStr(jsonStr, newLineStr = "\n", indentStr="\t"*4):
    """This method uses a recursive descent approach to traverse a json tree and generate
       a human-readable string representation of the json structure with nice indexing
       and indentation.

       Parameters:
       jsonStr    -- A json string to be prettied
       newLineStr -- A character or string to be used to mark the end of a line such as "\n", "\r\n", "<br>"
       indentStr  -- A character or string to be used represent a single indentation such as "\t", "|...", "&nbsp&nbsp"
       """
    
    handlers = {} # A dictionary which maps types to handler methods.
                  # Populated after the handler methods are defined.

    s = [""]  # the output string nested in a list.
              # the list nesting is used to circumvent scoping issues in handler methods

    ##############################################################################################
    # BEGIN ITEM HANDLERS                                                                        #
    # Item handler methods all accept an item to be handled and an indentation level which is    #
    # incremented as recursion proceeds deeper into the tree.                                    #
    ##############################################################################################
    def handleItem(level, item):
        """This is a generic handler method which retrieves the specific handler method based on the 
           type of item and calls that handler.
        """
        handler = handlers.get(type(item), handleLeaf) # get the handler for this item, if none is specified treat it as a leaf
        return handler(level, item) # call retrieved handler and return its resul
    def handleLeaf(level, item):
        """This method handles a leaf in a json tree.  A leaf is an entity which contains no children 
           and simply needs to be appended to the output with proper indentation"""

        s[0]+= indentStr*level + unicode(item) + newLineStr #append a line for this leaf to the pretty string

    def handleList(level, items):
        """This method handles a list element from a json tree.
           The list items are iterated.  Each item is indented beneath it's index.

           ["foo", 1] 
           becomes
           0
           ...."foo" 
           1
           ....1
           """
        i = 0 #index counter
        for item in items: #iterate the items in the list
            s[0] += indentStr*level + "[" + str(i) + "]" + newLineStr # append an index line to the output
            handleItem(level+1, item) # handle the list item with incremented indentation
            i += 1 # increment the current index

    def handleDict(level, items):
        """This method handles a dict element from a json tree.
           The dictionary items are iterated.  Each item is indented beneath it's key.

           {"first":"foo", "second":1} 
           becomes
           first:
           ....foo
           second:
           ....1
           """
        for k,v in items.items(): # iterate the key value pairs in the dictionary
            s[0] += indentStr*level + "{"+ str(k) + "}" + newLineStr # append the key to the output
            handleItem(level+1, v) # handle the item value with incremented indentation
    
    ##############################################################################################
    # END ITEM HANDLERS                                                                          #
    ##############################################################################################

    # populate the handler dictionary with the new methods
    handlers = {list: handleList,
                dict: handleDict}

    if (type(jsonStr) == str):
      data = json.loads(jsonStr) # parse the input json string
    else:
      data = jsonStr
    
    handleItem(0, data) # handler the root item with no indentation to kick off traversal.

    return s[0] # return the string built during json tree traversal.

if __name__ == "__main__":
    x = {"start":["me",2, {"fish":4, "Doctor":"Who"}], "Bow Ties":["Are", "Cool"]}
    y = json.dumps(x)
    print prettyJsonStr(y, "\n", "|---")