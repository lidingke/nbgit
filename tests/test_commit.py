import json
import os
import logging
import shelve
from collections import UserDict
import uuid as UUID
from commit import Commit, Commit_Tree, Commits

logger = logging.getLogger(__name__)

def duck(a,b):
    return str(UUID.uuid1()),()

def test_new_commit():
    c = Commit_Tree(db=None,ipynb=None)
    c.get_new_commit_on_ipynb = duck
    r = c.root
    n1 = c.new_commit(r,)
    n2 = c.new_commit(n1)
    n3 = c.new_commit(n2)
    n4 = c.new_commit(n2)
    assert n4 in n2.children
    assert n4 not in n3.children

def test_new_commit_by_real_ipynb():
    ipynb = '../data/Untitled.ipynb'

    db = '../data/spam'
    c = Commit_Tree(db=db,ipynb=ipynb)
    # c.get_new_commit_on_ipynb = duck
    r = c.root
    n1 = c.new_commit(r,)
    n2 = c.new_commit(n1)
    n3 = c.new_commit(n2)
    n4 = c.new_commit(n3)
    assert n4 in n3.children
    assert n4 not in n2.children

def test_change_commit_to():
    c = Commit_Tree(db=None, ipynb=None)
    c.get_new_commit_on_ipynb = duck
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

def test_commits_userdict_load():
    c = Commits()
    with open('../data/datas_for_tests.json','rb') as f:
        datas = json.loads(f.read().decode('utf-8'))
        c.build_from(datas['commits'])
    assert len(c)>0
    assert isinstance(c,UserDict)
    for cm in c.values():
        assert isinstance(cm,Commit)
    assert "abcd1234" in c
    assert c["abcd1234"] in c


def test_load_commit_tree():
    c = Commit_Tree(None,None,'../data/datas_for_tests.json')


