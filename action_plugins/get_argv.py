#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import os

# Get Ansible context parser
from ansible import context

# ADT base class for our Ansible Action Plugin
from ansible.plugins.action import ActionBase

# Load the display handler to send logging to CLI or relevant display mechanism
try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


# Get all Ansible commandline arguments and place these in the
# `facts` dictionairy as `ansible_facts['argv']`
class ActionModule(ActionBase):

    # No file transfer needed
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        '''Run action plugin'''

        # All checks (file, exists, etc) are already done
        # by the Ansible context
        playbooks = list(map(os.path.abspath, list(context.CLIARGS['args'])))

        # Create the result JSON blob
        result = {
            'changed': False,
            'failed': False,
            'skipped': False,
            'msg': '',
            'ansible_facts': {
                'argv' : sys.argv,
                'playbooks': playbooks,
            }
        }

        return result
