from util import INSTRUCTIONS


class Node:
    def __init__(self, nodeType) -> None:
        self.nodeType = nodeType
        self.children = []

    def addChild(self, child) -> None:
        self.children.append(child)

    def addChildren(self, children) -> None:
        self.children.extend(children)


class Parser:
    def __init__(self, tokenStream: list) -> None:
        self.tokenStream = tokenStream
        self.index = 0

        self.ast = Node

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

        if self.getCurrentToken()[0] == '.text':
            node.addChild(self.textField())
        
        return node
    
    def textField(self) -> Node:
        node = Node('.text')

        if self.getCurrentToken()[0] == '.text':
            self.advance()
            node.addChildren(self.labelInstList())
        else:
            raise Exception('Unexpected token. Expected .text. Got ' + self.getCurrentToken()[0])
        
        return node
    
    def labelInstList(self) -> Node:
        children = []
        
        children.append(self.labelOrInst())

        if (tempChildrenList := self.labelInstList()) is not None:
            children.extend(tempChildrenList)
        
        
        return None if children == [] else children
    
    def labelOrInst(self) -> Node:
        if self.getCurrentToken()[0] in INSTRUCTIONS:
            self.advance()
            return self.instruction()
        
        elif self.getCurrentToken()[0] == 'label':
            self.advance()
            return self.label()
        
        else:
            raise Exception('Syntactical Error - Unexpected token. Expected instruction or label. Got ' + self.getCurrentToken()[0])

