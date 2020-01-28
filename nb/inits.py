import os
import os.path as osp
import sys

from nb.config import workspace_dir
from nb.db import ShelveDB, get_db_dir


def init_bare_repo(current_ipynb):
    """
    nbgit init: run cmd in ipynb, create a emputy file.
    """
    
    dir_= get_db_dir(current_ipynb)
    sdb = ShelveDB(dir_=dir_)
    sdb.create_bare_db()
    return sdb
