import gemNumFuncs as gnf
import getwordsfromdbs as gwdb


class Word:
  def __init__(self, value):
    self.value = value
    self.children = {}
    self.words = []
    return

class NineRootedTree:

    def __init__(self, words, cipher):
      self.roots = [None, None, None, None, None, None, None, None, None, None]
      if words:
        for i in words:
          self.addWord(i, cipher)        
      self.numList = []

      return

    def addWord(self, word, cipher):
      route = gnf.getParentList(gnf.getGematria(word, cipher))
      route.reverse()
      parent = self.roots[route[0]]
      if parent is None:
        self.roots[route[0]] = Word(route[0])
        parent = self.roots[route[0]]
      for digit in route[1:]: 
        next = parent.children.get(digit)
        if next is None:
          next = Word(digit)
          parent.children[digit] = next
        parent=next  
      if not word in parent.words:
        parent.words+=[word]
      return word

    def removeNode(self, node):
      if node.children:
        return
      parent = self.roots[gnf.getRootNumber(node.value)]
      route = gnf.getParentList(node.value)[1:]
      for digit in route:
        next = parent.children.get(digit)
        if next is None:
          return
        if next == node:
          parent.children.pop(digit)
          return
        parent=next
      return
    
    def getWords(self):
      words=[]
      for i in self.getNumbers():
        words+=self.findWords(i)
      return words


    def findWords(self, value):
      if value == 0:
        return []
        
      route = gnf.getParentList(value)
      route.reverse()

      node = self.roots[route[0]]
      if value == node.value:
        return node.words

      for i in route[1:]:
        node = node.children.get(i)
        if node != None:
          if i == value:
            return node.words
      return []

    def deleteWordsByValue(self, value):
      if value == 0:
        return []
        
      route = gnf.getParentList(value)
      route.reverse()

      node = self.roots[route[0]]
      if value == node.value:
        node.words = []
        return

      for i in route[1:]:
        node = node.children.get(i)
        if node != None:
          if i == value:
            node.words = []
            return

      if node.words == []:
        node = None

      return


    def route_to_root(self, word, cipher):
        return gnf.getParentList(gnf.getGematria(word, cipher))
                               
    def __str__(self):
        tree_str = ''
        for root in self.roots:
            if root is not None:
                tree_str += self.print_tree(root, '')
        return tree_str

    def print_tree(self, word, prefix):
        tree_str = prefix + str(word.value) + '\n' + prefix + str(word.words) + '\n'
        for child in word.children.values():
            tree_str += self.print_tree(child, prefix + '  ')
        return tree_str

    def iterChildren_getNumbers(self, word):
        self.numList += [word.value]
        for child in word.children.values():
            self.iterChildren_getNumbers(child)
        return

    def getNumbers(self):
        for r in self.roots:
            if r is not None:
                self.iterChildren_getNumbers(r)
        ret = self.numList.copy()
        self.numList = []
        return ret
 
    def generateNestedList(self, ue):
        result = "<ul>"
        for root in self.roots:
          if root is not None:
            result+=self.generateListItems(root, ue)
        result+="</ul>"
        return result

    def generateListItems(self, word, ue):
      result = ""

      result += "<li><button class='numberInTree' id='number"+ str(word.value)+"'>" + str(word.value) + "</button><br>"
      result+="<div class='wordies'>"
      lap=0
      for w in word.words:
        lap+=1
        if w in ue:
          result += "<button class='wordInTree_UE' id='WORD"+w+"'>"+str(w)+"&nbsp"+"</button>"

        if w not in ue:
          result += "<button class='wordInTree' id='WORD"+w+"'>"+str(w)+"&nbsp"+"</button>"

        if lap%5==0:
          result += "<br>"

      result+="</div>"
      result += "</li>"

      if word.children:
          result += "<ul>"
          for child in word.children.values():
              result += self.generateListItems(child, ue)
          result += "</ul>"
      
      return result


def wordList_to_NineRootedTree(words, cipher):
  tree = NineRootedTree(words, cipher)
  return tree

