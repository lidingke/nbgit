import os
import os.path as osp
import sys
from copy import deepcopy

__version__ = 'v.1.0.0'


workspace_dir = '.jupyter_notebook'

"""
current_branch == HEAD 
"""
bare_db_json = {
    "lines": {},
    "branch_refs": {
        "master": 'root',
    },
    "nodes": ['root'],
    "current_branch": "master",
    "cache":None,
}


base_node_json = {
    'index': '',
    'line_index': [],
    'commit': '',
    'tags': [''],
    'parents': []
}


def get_base_node_json():
    return deepcopy(base_node_json)


cell_line = {
    "cell_type": "code",
    "execution_count": 1,
    "metadata": {},
    "outputs": [
        # {
        #  "name": "stdout",
        #  "output_type": "stream",
        #  "text": ""
        # }
    ],
    "source": [
        "print('abcd')"
    ]
}


class CacheLockError(Exception):
    def __init__(self, err='cache lock, pls save current cache.'):
        Exception.__init__(self, err)


class InitError(ValueError):
    pass


class NodeError(ValueError):
    pass


class BranchError(ValueError):
    pass


# git clone https://github.com/dulwich/dulwich.git
