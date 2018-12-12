class Node:
    def __init__(self):
        self.label = None
        self.children = {}
        self.saveChildren={}
        self.isLeaf = True
        self.attribute = ''
        # you may want to add additional fields here...

    def __init__(self, attribute, children, label, isLeaf=False):
        self.attribute = attribute
        self.children = children
        self.label = label
        self.isLeaf = isLeaf


    def get_label(self):
        return self.label

    def get_children(self):
        return self.children

    def get_child(self, val):
        if self.children.get(val):
            return self.children[val]
        return None

    def get_atrribute(self):
        return self.attribute

    def checkLeaf(self):
        return self.isLeaf

    def set_to_leaf(self,label):
        self.saveChildren=self.children
        self.children={}
        self.isLeaf=True
        self.label=label

    def recoveprune(self):
        self.children = self.saveChildren
        self.saveChildren = {}
        self.isLeaf = False
        self.label = None
