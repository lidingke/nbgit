import os
import os.path as osp
import shelve

from nb.config import bare_db_json, workspace_dir


class ShelveDB(object):

    def __init__(self, dir_):
        self.db = shelve.open(dir_, writeback=True)


    def create_bare_db(self):
        self.db.clear()
        self.db.update(bare_db_json) 


    def get_item(self, key):
        """
        get db part, like 'lines','branche_refs','current_branch'
        """
        return self.db[key]


def get_db_dir(current_ipynb):
    """
    get db full path from current ipynb path
    """
    dirname = osp.dirname(current_ipynb)
    name = osp.basename(current_ipynb)
    # name = ".".join(name.split('.')[:-1])
    if name.endswith('.ipynb'):
        name = name[:-6]
    else:
        raise IOError('suffix error on {}'.format(name))
    # workspace = osp.join(full_workspace_dir,)
    # import pdb; pdb.set_trace()
    full_workspace_dir = osp.join(dirname,workspace_dir)
    if not osp.exists(full_workspace_dir):
        os.mkdir(full_workspace_dir)
    # sdb = ShelveDB(dir_=))
    return osp.join(full_workspace_dir,name)