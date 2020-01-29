import os
import os.path as osp
import sys

__version__ = 'v.1.0.0'


workspace_dir = '.jupyter_notebook'

bare_db_json={
  "lines": {},
  "branch_refs":{
    "master":'root',
  },
  "nodes":[],
  "current_branch":"master"
}


base_node_json = {
    'index':'',
    'lines':[],
    'commit':'',
    'tags':[''],
    'parents':[]
}

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
    def __init__(self,err='cache lock, pls save current cache.'):
        Exception.__init__(self,err)

class InitError(ValueError):
    pass

        