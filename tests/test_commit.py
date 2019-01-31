import os
import logging


from git_objects import Commit,Commit_Tree


logger = logging.getLogger(__name__)

def test_new_commit():
    c = Commit_Tree()
    r = c.root
    n1 = c.new_commit(r,)
    n2 = c.new_commit(n1)
    n3 = c.new_commit(n2)
    n4 = c.new_commit(n2)
    assert n4 in n2.children
    assert n4 not in n3.children

def test_change_commit_to():
    c = Commit_Tree()
    r = c.root
    n1 = c.new_commit(r, )
    n2 = c.new_commit(n1)
    n3 = c.new_commit(n2)
    n4 = c.new_commit(n2)
    assert n4 in n2.children
    assert n4 not in n3.children
    c.change_commit_to(n4,n3)
    assert n4 not in n2.children
    assert n4 in n3.children
    assert n4.parent in n3.parent.children
    logger.info(c.__str__())
    # print(c)
    # print(n2)
    # print(n4)


def test_load_commit_tree():
    # print(os.getcwd())
    c = Commit_Tree('../data/datas_for_tests.json')


def test_load_commit_tree():
    # print(os.getcwd())
    c = Commit_Tree('../data/datas_for_tests.json')


