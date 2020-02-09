import difflib
from difflib import Differ
from nb.node import Node, NodeDB
from difflib import ndiff
    # import pdb; pdb.set_trace()


def insert(a,a0,a1,seq):
    for s in seq:
        a.insert(a1,s)
    return a

def delete(a,a0,a1,seq):
    for i in range(a0,a1):
        a.pop(i)
    return a

def equal(a,a0,a1,seq):
    return a

def replace(a, a0, a1, seq):
    for i, v in zip(range(a0, a1), seq):
        a[i] = v
    return a


op_fun = {
    'insert':insert,
    'delete':delete,
    'equal':equal,
    'replace':replace
}

op_fun_back = {
    'insert':delete,
    'delete':insert,
    'equal':equal,
    'replace':replace
}

def get_reversed_opecodes(seq0,seq1):
    matcher = difflib.SequenceMatcher(None,seq0,seq1)
    _ = [(tag, i0,i1,seq1[j0:j1]) for tag, i0, i1, j0, j1 in reversed(matcher.get_opcodes())]
    return _

def constructer(seq,opcodes):
    for tag, i0,i1,seq1 in opcodes:
        assert tag in op_fun.keys()
        seq = op_fun[tag](seq,i0,i1,seq1)

    return seq


def Merger(object):

    def __init__(self, db):
        self._db = db
        self.nodedb = NodeDB(db)

    def diff(self, index0,index1):

        n0,n1 = self.nodedb.get_node(index0), self.nodedb.get_node(index1)
        ng = ndiff(n0.lines,n1.lines)
        for n in ng:
            print(n)

# def back_constructer(seq, opcodes):
#     for tag, i0, i1, seq1 in opcodes:
#         assert tag in op_fun_back.keys()
#         seq = op_fun_back[tag](seq, i0, i1, seq1)
#
#     return seq