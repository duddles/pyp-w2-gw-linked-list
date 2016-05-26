import copy

class AbstractLinkedList(object):
    """
    Abstract class representing the LinkedList inteface you must respect.
    
    You must not implement any of the method in this class, and this class
    must never be instantiated. It's just a "guide" of which methods
    the LinkedList class should respect.
    """

    def __str__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()

    def __add__(self, other):
        raise NotImplementedError()

    def __iadd__(self, other):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def append(self, element):
        raise NotImplementedError()

    def count(self):
        raise NotImplementedError()

    def pop(self, index=None):
        raise NotImplementedError()


class Node(object):
    """
    Node class representing each of the linked nodes in the list.
    """

    def __init__(self, elem, next=None):
        self.elem = elem
        self.next = next

    def __str__(self):
        return str(self.elem)

    def __eq__(self, other):
        if type(other) == Node: # make sure we are comparing two nodes
            return self.elem == other.elem
        return self.elem == other # in case comparing to a non-node value
        
    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self.elem)


class LinkedList(AbstractLinkedList):
    """
    Implementation of an AbstractLinkedList inteface.
    """

    def __init__(self, elements=None):
        '''
        Reads in either no parameters LinkedList()
        or a list of parameters LinkedList([1,2,3])
        '''
        # no parameter case, set start and end to None
        self.start = None
        self.end = None
        
        # if there are parameters, append them one at a time
        # append() will create the nodes and deal with the .start and .end attributes
        if elements:
            for element in elements:
                self.append(element) # append will set the start and end attributes

    def __str__(self):
        '''
        str representation of linked list for print
        Print the node.elem for each node in the list "[2, 4, 6, 8, 10]"
        This utilizes the __iter__ method of the linked list
        '''
        return '[{}]'.format(', '.join(str(i) for i in self))

    def __len__(self):
        '''
        Returns length of linked lest by calling count() method
        '''
        return self.count()

    def __iter__(self):
        '''
        Generator that traverses through the linked list
        '''
        node = self.start
        while node: # loop until node gets set to Next when reach the end node
            yield node
            node = node.next # node.next will be None for the end node
            
    def __getitem__(self, index):
        '''
        Returns the node at the particular index in the linked list
        '''
        # Check that index is within the range of the list length
        if not 0 <= index < self.count():
            raise IndexError
        for pos, node in enumerate(self):
            if pos == index:
                return node
        
    def __add__(self, other):
        '''
        Combines 2 linked lists and returns a new list
        [1,2,3,'car'] = [1,2,3] + ['car']
        '''
        # make new copies of the lists so we don't create conflicts
        left_list = copy.deepcopy(self)
        right_list = copy.deepcopy(other)
        
        # special cases where one of the two lists is empty
        # if both are empty it will return an empty list as well
        if not left_list.start:
            return right_list
        if not right_list.start:
            return left_list
        
        # both lists are non-empty, so combine them into the left_list
        left_list.end.next = right_list.start # connect the left end with right start
        left_list.end = right_list.end # set the end pointer to now point to right end
        return left_list

    def __iadd__(self, other):
        '''
        Adds the other linked list to the end of self (self is modified)
        [1,2,3] += ['car'] # self is now [1,2,3,'car']
        '''
        self = self + other
        return self

    def __eq__(self, other):
        '''
        Compares 2 linked lists, they must have the same node.elem in the same order
        to be equal
        '''
        # first check for equal lengths
        if self.count() != other.count():
            return False
            
        # use __iter__ to traverse both lists and compare nodes
        for i,j in zip(self, other):
            if i != j: # uses the node __ne__ method
                return False
        return True

    def append(self, elem):
        '''
        Creates a new node for elem
        Adds new node to the end of the linked list
        Sets list.end to point to this node
        '''
        node = Node(elem)
        if not self.start: # appending to an empty list
            self.start = node
        else: # adding to an existing list
            self.end.next = node # previous last node now points to new last node
        self.end = node # the appended node is our new end
 
    def count(self):
        '''
        Returns the length of a list by traversing from start to end node
        '''
        return sum(1 for _ in self)
        
    def pop(self, index=None):
        '''
        If no index is given, will remove and return the end node
        Else it will remove and return the node located at the index
        '''
        list_length = self.count()
        
        if index == None: # assign index in case it was None (using 0-based indexing)
            index = list_length - 1 

        # check for a valid index range
        if not 0 <= index < list_length:
            raise IndexError
            
        node_to_remove = self[index] # store the node we will remove so we can return it later

        if index == 0: # special case if removing start node
            if list_length == 1: # removed the only node in the list so list is now empty
                self.start = None
                self.end = None
            else:
                self.start = self[1] # move self.start to point to 2nd node
                
        elif index == list_length - 1: # if remove end node
            node_before = self[index-1]
            node_before.next = None
            self.end = node_before
            
        else: # removing a node somewhere in the middle
            node_before = self[index-1] # node before the one to remove
            node_after = self[index+1] # node after the one to remove
            node_before.next = node_after # connect the before and after nodes
            
        return node_to_remove
