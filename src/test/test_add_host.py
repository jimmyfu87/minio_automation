# test_add_host.py

import sys
sys.path.insert(0, '../')
from add_host import add_host
from bmc import config_host_list
from util import alias


def test_add_host():
    alias_exist = False
    if add_host():
        response = config_host_list()
        hosts = response.content
        for host in hosts:
            if host['alias'] == alias:
                alias_exist = True
        assert alias_exist == True
