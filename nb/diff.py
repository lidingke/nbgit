import difflib
from difflib import Differ
from nb.node import Node, NodeDB, Branch
# from .branch import Branch
from nb.config import BranchError
from difflib import ndiff
# import pdb; pdb.set_trace()


def insert(a, a0, a1, seq):
    for s in seq:
        a.insert(a1, s)
    return a


def delete(a, a0, a1, seq):
    for i in range(a0, a1):
        a.pop(i)
    return a


def equal(a, a0, a1, seq):
    return a


def replace(a, a0, a1, seq):
    for i, v in zip(range(a0, a1), seq):
        a[i] = v
    return a


op_fun = {
    'insert': insert,
    'delete': delete,
    'equal': equal,
    'replace': replace
}

op_fun_back = {
    'insert': delete,
    'delete': insert,
    'equal': equal,
    'replace': replace
}


def get_reversed_opecodes(seq0, seq1):
    matcher = difflib.SequenceMatcher(None, seq0, seq1)
    _ = [(tag, i0, i1, seq1[j0:j1])
         for tag, i0, i1, j0, j1 in reversed(matcher.get_opcodes())]
    return _


def constructer(seq, opcodes):
    for tag, i0, i1, seq1 in opcodes:
        assert tag in op_fun.keys()
        seq = op_fun[tag](seq, i0, i1, seq1)

    return seq


class Merger(object):

    def __init__(self, db):
        self._db = db
        self.nodedb = NodeDB(db)
        self.current = Branch(db)

    def diff(self, index0, index1):

        n0, n1 = self.nodedb.get_node(index0), self.nodedb.get_node(index1)
        ng = ndiff(n0.lines, n1.lines)
        for n in ng:
            print(n)

    def auto_merge(self, other):
        # assert isinstance(current,str)
        assert isinstance(other, str)
        c_index = self.current.index
        o_index = self.current.get_ref(other)
        ancestor = self.find_ancestor(c_index, o_index)
        # diff_ret_c = self.diff_result(c_index,ancestor)
        # diff_ret_o = self.diff_result(o_index,ancestor)
        c_lines = self.nodedb.get_node(c_index)
        o_lines = self.nodedb.get_node(o_index)
        a_lines = self.nodedb.get_node(ancestor)
        res = []
        for a, c, o in zip(a_lines, c_lines, o_lines):
            if a == c == o:
                res.append(a)
            elif a == c and a != o:
                res.append(o)
            elif a != c and a != o:
                res.append(c)
            else:
                res.append('conflict')

    def diff_result(self, index0, index1):
        n0, n1 = self.nodedb.get_node(index0), self.nodedb.get_node(index1)
        ng = ndiff(n0.lines, n1.lines)
        return ng

    def find_ancestor(self, current, other):
        croot = self.trace_root([current])
        oroot = self.trace_root([other])
        if croot[-1] != 'root':
            raise BranchError('currnt node can\'t traceback to root node.')
        if oroot[-1] != 'root':
            raise BranchError('other node can\'t traceback to root node.')
        last = ''
        # import pdb; pdb.set_trace()

        for i, v in zip(croot[::-1], oroot[::-1]):
            if i != v:
                return last
            last = i
        return last

        # import pdb; pdb.set_trace()
        # while True:
        # c = current.parents[0]
        # o = other.parents[0]

    def trace_root(self, nodes):
        assert isinstance(nodes, list)
        node = nodes[-1]
        if node == 'root':
            return nodes
        else:
            node = self.nodedb.get_node(node)
            parents = node.parents[0]
            nodes.append(parents)
            return self.trace_root(nodes)


# def back_constructer(seq, opcodes):
#     for tag, i0, i1, seq1 in opcodes:
#         assert tag in op_fun_back.keys()
#         seq = op_fun_back[tag](seq, i0, i1, seq1)
#
#     return seq
