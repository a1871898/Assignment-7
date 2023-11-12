class CompilerParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    # ... (other methods)

    def compileProgram(self):
        parse_tree = ParseTree("program")
        while self.current_token_index < len(self.tokens):
            parse_tree.children.append(self.compileClass())
        return parse_tree

    def compileClass(self):
        parse_tree = ParseTree("class")
        parse_tree.children.append(self.mustBe("KEYWORD", "class"))
        parse_tree.children.append(self.mustBe("IDENTIFIER"))
        parse_tree.children.append(self.mustBe("SYMBOL", "{"))

        while self.have("KEYWORD", ["static", "field"]):
            parse_tree.children.append(self.compileClassVarDec())

        parse_tree.children.append(self.mustBe("SYMBOL", "}"))
        return parse_tree

    def compileClassVarDec(self):
        parse_tree = ParseTree("classVarDec")
        parse_tree.children.append(self.mustBe("KEYWORD", ["static", "field"]))
        parse_tree.children.append(self.mustBe(["KEYWORD", "IDENTIFIER"]))  # Type
        parse_tree.children.append(self.mustBe("IDENTIFIER"))  # VarName

        while self.have("SYMBOL", ","):
            parse_tree.children.append(self.mustBe("SYMBOL", ","))
            parse_tree.children.append(self.mustBe("IDENTIFIER"))  # VarName

        parse_tree.children.append(self.mustBe("SYMBOL", ";"))
        return parse_tree

    # Implement other methods as per the given structure

    def next(self):
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
        else:
            raise ParseException("Cannot advance further, end of input reached")

    def current(self):
        return self.tokens[self.current_token_index]

    def have(self, token_type, expected_values=None):
        current_token = self.current()
        if current_token.token_type == token_type:
            if expected_values is None or current_token.value in expected_values:
                return True
        return False

    def mustBe(self, token_type, expected_values=None):
        if self.have(token_type, expected_values):
            current_token = self.current()
            self.next()
            return current_token
        else:
            raise ParseException(f"Expected token type: {token_type}, value: {expected_values}, but found {self.current().token_type}, value: {self.current().value}")


if __name__ == "__main__":
    # ... (other code)

    tokens = [
        Token("KEYWORD", "class"),
        Token("IDENTIFIER", "MyClass"),
        Token("SYMBOL", "{"),
        Token("SYMBOL", "}"),
    ]

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
