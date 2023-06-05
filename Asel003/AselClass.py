#a class for stacks, but modified especially for Asel.

class lastTalkedStack:
    def __init__(self,maxSize=None):
        self.items = []
        self.maxSize = None
        if maxSize:
            self.maxSize = maxSize-1
    
    def pop(self):
        return self.items.pop()
    
    def isEmpty(self): #boolean return
            return len(self.items) == 0
    
    def top(self):
        temp = self.items.pop()
        self.items.append(temp)
        return temp

    def popBottom(self):
        temp = self.items[::-1][len(self.items)-1]
        self.items = self.items[::-1]
        self.items.pop()
        self.items = self.items[::-1]
        return temp

    def topBottom(self):
        temp = self.items[::-1][len(self.items)-1]
        return temp
    
    def getList(self):
        return self.items[::-1]
    
    def printStack(self):
        for i in self.items[::-1]:
            print(f"[{i}]")

    def push(self,item):
        if self.maxSize and len(self.items) > self.maxSize:
            self.popBottom()
        if item in self.items:
            self.items.remove(item)
            #self.push(",")
        return self.items.append(item)
    
