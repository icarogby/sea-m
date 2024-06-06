R_TYPE_INSTRUCTIONS = ['add', 'sub']
INSTRUCTIONS = R_TYPE_INSTRUCTIONS


class Node:
    def __init__(self, type, lexeme: str = '\0') -> None:
        self.type = type
        self.lexeme: str = lexeme
        self.children: list[Node] = []

    def __repr__(self) -> str:
        return f'{self.type}({self.lexeme}) -> {self.children}'

    def addChildren(self, child) -> None:
        if type(child) is list:
            self.children.extend(child)
        else:
            self.children.append(child)


class Parser:
    def __init__(self, tokenStream: list) -> None:
        self.tokenStream = tokenStream
        self.index = 0

        self.ast = None

        self.parse()

    def getAst(self) -> Node:
        return self.ast
    
    def getCurrentToken(self) -> str:
        return self.tokenStream[self.index]
    
    def peekNextToken(self) -> str:
        return self.tokenStream[self.index + 1]
    
    def advance(self) -> None:
        self.index += 1

    def parse(self) -> None:
        self.ast = self.asmCode()

    def asmCode(self) -> Node:
        node = Node('asmCode')

        # if (currentToken := self.getCurrentToken()[0]) == '.data': # todo: create data section

        if (currentToken := self.getCurrentToken()[0]) == 'text_dir':
            node.addChildren(self.textField())
        
        return node
    
    def textField(self) -> Node:
        if self.getCurrentToken()[0] == 'text_dir':
            node = Node('Text Field')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".text". Got "' + self.getCurrentToken()[0] + '"')

        if (instList := self.instList()) is not None:
            node.addChildren(instList)
        
        return node

    def instList(self) -> Node:
        instList = []

        if self.getCurrentToken()[0] == 'mnemonic':
            instList.append(self.inst())
        
        elif self.getCurrentToken()[0] == 'label':
            instList.append(self.labelDec())

        if (self.getCurrentToken()[1] == 'mnemonic') or (self.getCurrentToken()[0] == 'label'):
            instList.extend(self.instList())

        return instList
    
    def inst(self) -> Node:
        node = Node('inst')

        if (tokenLabel := self.getCurrentToken()[0])  == 'mnemonic':
            if (tokenLexeme := self.getCurrentToken()[1]) in R_TYPE_INSTRUCTIONS:
                node.addChildren(self.rTypeInst())
                
                return node
            # todo: add more instruction types here
            else:
                raise Exception('SYNTACTICAL ERROR - Invalid mnemonic. Got "' + tokenLexeme + '"')

        else:
            raise Exception('SYNTACTICAL ERROR - Expected mnemonic. Got "' + tokenLabel + '"')

    def rTypeInst(self) -> Node:
        if (tokenlexeme := self.getCurrentToken()[1]) in R_TYPE_INSTRUCTIONS:
            node = Node('rTypeInst', tokenlexeme)
            self.advance()

            node.addChildren(self.acReg())

            if self.getCurrentToken()[0] == 'comma':
                self.advance()
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected , after AC register. Got ' + self.getCurrentToken()[0] + '"')
            
            node.addChildren(self.rfReg())

            if self.getCurrentToken()[0] == 'comma':
                self.advance()
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token.Expected , after AC register. Got ' + self.getCurrentToken()[0] + '"')
            
            node.addChildren(self.rfReg())

            return node

        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected R-Type instruction. Got ' + tokenlexeme + '"')

    def labelDec(self) -> Node:
        if (currentToken := self.getCurrentToken()[0]) == 'label':
            node = Node('labelDec', self.getCurrentToken()[1])
            self.advance()

            if self.getCurrentToken()[0] == 'colon':
                self.advance()

                node.addChildren(self.inst())
            
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected ":" after label declaration. Got "' + self.getCurrentToken()[0] + '"')
       
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected label declaration. Got "' + currentToken + '"')
        
        return node
        
    def acReg(self) -> Node:
        if (currentToken := self.getCurrentToken()[0]) == 'acReg':
            node = Node('acReg', self.getCurrentToken()[1])
            self.advance()

            return node
        
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected AC register. Got ' + currentToken + '"')
        
    def rfReg(self) -> Node:
        if (currentToken := self.getCurrentToken()[0]) == 'rfReg':
            node = Node('rfReg', self.getCurrentToken()[1])
            self.advance()

            return node
        
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected RF register. Got ' + currentToken + '"')
