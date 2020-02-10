import os
import os.path as osp
import shelve

from nb.config import bare_db_json, workspace_dir, base_node_json,get_base_node_json


class ShelveDB(object):

    def __init__(self, dir_):
        self.db = shelve.open(dir_, writeback=True)

    def create_bare_db(self):
        self.db.clear()
        self.db.update(bare_db_json)
        # self.db['nodes'].append(bare_db_json)
        self.db['cache']=get_base_node_json()
        self.db['cache']['parents']=['root']
        # node0 = self.db['nodes'][0]
        # node0['index'] = 'root'
        # node0['parents'] = ['root', ]
        

    def get_item(self, key):
        """
        get db part, like 'lines','branche_refs','current_branch'
        """
        return self.db[key]

    def sync(self):
        self.db.sync()


def get_db_dir(current_ipynb):
    """
    get db full path from current ipynb path
    """
    dirname = osp.dirname(current_ipynb)
    name = osp.basename(current_ipynb)
    if name.endswith('.ipynb'):
        name = name[:-6]
    else:
        raise IOError('suffix error on {}'.format(name))
    # workspace = osp.join(full_workspace_dir,)

    full_workspace_dir = osp.join(dirname, workspace_dir)
    if not osp.exists(full_workspace_dir):
        os.mkdir(full_workspace_dir)

    return osp.join(full_workspace_dir, name)
