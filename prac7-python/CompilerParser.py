from ParseTree import *

class CompilerParser:

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.currentTokenIndex = 0

    

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        parse_tree = ParseTree("program")
        while self.currentTokenIndex <len(self.tokens):
            parse_tree.addChild(self.compileClass()) 
        return parse_tree 
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        parse_tree = ParseTree("class")
        parse_tree.addChild(self.mustBe("keyword","class"))
        parse_tree.addChild(self.mustBe("identifier",None))
        parse_tree.addChild(self.mustBe("symbol","{"))
        
        while self.have("keyword",["static","field"]):
            parse_tree.addChild(self.compileClassVarDec())
        
        parse_tree.addChild(self.mustBe("symbol","}"))
        
        return parse_tree 
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        parse_tree = ParseTree("classVarDec")
        parse_tree.addChild(self.mustBe("keyword",["static","field"]))
        parse_tree.addChild(self.compileType())
        parse_tree.addChild(self.mustBe("identifier",None))

        while self.have("symbol",","):
            parse_tree.addChild(self.mustBe("symbol",","))
            parse_tree.addChild(self.mustBe("identifier",None))

        parse_tree.addChild(self.mustBe("symbol",";"))
        return parse_tree 
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        return None 
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        return None 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        return None 
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        return None 
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        parse_tree = ParseTree("statements")

        while self.have("KEYWORD", ["let", "do", "if", "while", "return"]):
            if self.have("KEYWORD", "let"):
                parse_tree.children.append(self.compileLet())
            elif self.have("KEYWORD", "do"):
                parse_tree.children.append(self.compileDo())
            elif self.have("KEYWORD", "if"):
                parse_tree.children.append(self.compileIf())
            elif self.have("KEYWORD", "while"):
                parse_tree.children.append(self.compileWhile())
            elif self.have("KEYWORD", "return"):
                parse_tree.children.append(self.compileReturn())

        return parse_tree
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        parse_tree = ParseTree("letStatement")
        parse_tree.children.append(self.mustBe("KEYWORD", "let"))
        parse_tree.children.append(self.mustBe("IDENTIFIER"))  # varName
        parse_tree.children.append(self.mustBe("SYMBOL", "="))

        # Partial implementation of compileExpression
        parse_tree.children.append(self.compileExpression())

        parse_tree.children.append(self.mustBe("SYMBOL", ";"))
        return parse_tree


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        parse_tree = ParseTree("ifStatement")
        parse_tree.children.append(self.mustBe("KEYWORD", "if"))
        parse_tree.children.append(self.mustBe("SYMBOL", "("))

        # Partial implementation of compileExpression
        parse_tree.children.append(self.compileExpression())

        parse_tree.children.append(self.mustBe("SYMBOL", ")"))
        parse_tree.children.append(self.mustBe("SYMBOL", "{"))

        # Partial implementation of compileStatements
        parse_tree.children.append(self.compileStatements())

        parse_tree.children.append(self.mustBe("SYMBOL", "}"))

        if self.have("KEYWORD", "else"):
            parse_tree.children.append(self.mustBe("KEYWORD", "else"))
            parse_tree.children.append(self.mustBe("SYMBOL", "{"))

            # Partial implementation of compileStatements
            parse_tree.children.append(self.compileStatements())

            parse_tree.children.append(self.mustBe("SYMBOL", "}"))

        return parse_tree

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        parse_tree = ParseTree("whileStatement")
        parse_tree.children.append(self.mustBe("KEYWORD", "while"))
        parse_tree.children.append(self.mustBe("SYMBOL", "("))

        # Partial implementation of compileExpression
        parse_tree.children.append(self.compileExpression())

        parse_tree.children.append(self.mustBe("SYMBOL", ")"))
        parse_tree.children.append(self.mustBe("SYMBOL", "{"))

        # Partial implementation of compileStatements
        parse_tree.children.append(self.compileStatements())

        parse_tree.children.append(self.mustBe("SYMBOL", "}"))
        return parse_tree


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        return None 


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 


    def next(self):
        """
        Advance to the next token
        """
        if self.currentTokenIndex < len(self.tokens):
            self.currentTokenIndex += 1
        else:
            raise ParseException("No more tokens")


    def current(self):
        """
        Return the current token
        @return the token
        """
        return self.tokens[self.currentTokenIndex]


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        currentToken = self.current()
        if currentToken.type == expectedType:
            if expectedValue == None:
                return True
            elif currentToken.value == expectedValue:
                return True
        return False


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        if self.have(expectedType,expectedValue):
            currentToken = self.current()
            self.next()
            return currentToken
        else:
            raise ParseException("Expected token not found")
        
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","MyClass"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")


