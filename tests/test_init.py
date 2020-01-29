import os
import os.path as osp
import sys

from nb.inits import init_bare_repo

#rm ..\nbgit\data\.jupyter_notebook\*

test_ipynb_dir = 'data/Untitled.ipynb'

def test_init_bare_repo():
    """
    nbgit init: run cmd in ipynb, create a emputy file.
    """
    db = init_bare_repo(test_ipynb_dir)
    assert db
