# Copyright 2019 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

import json
import os
import paunch as p
import re
import yaml
from paunch import runner as prunner
from paunch.builder import compose1 as pcompose1
from paunch.builder import podman as ppodman
from paunch.utils import common as putils_common


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: paunch
author:
    - OpenStack TripleO Contributors
version_added: '1.0'
short_description: Manage containers with Paunch
notes: []
requirements:
  - "paunch module"
  - "podman or docker"
description:
    - Start or stop containers with Paunch
options:
  config:
    description:
      - JSON file or directory of JSON files containing configuration data
  config_id:
    description:
      - ID to assign to containers
    required: True
    type: list
  action:
    description:
      - The desired action to apply for the container.
    default: apply
    choices:
      - apply
      - cleanup
  container_cli:
    description:
      - The container CLI.
    default: podman
    choices:
      - podman
      - docker
  container_log_stdout_path:
    description:
      - Absolute path to a directory where container stdout will be stored.
    default: /var/log/containers/stdouts
  healthcheck_disabled:
    description:
      - Whether or not we disable the Containers Healthchecks
    type: bool
    default: False
  managed_by:
    description:
      - Name of the tool managing the containers. Only containers labelled with
        this will be modified
    default: paunch
  debug:
    description:
      - Whether or not we enable Debug
    type: bool
    default: True
  log_file:
    description:
      - Absolute path for the paunch log file.
    default: /var/log/paunch.log
"""

EXAMPLES = """
# Paunch apply example
- name: Start containers for step 1
  paunch:
    config: /var/lib/tripleo-config/hashed-container-startup-config-step_1.json
    config_id: tripleo_step1
    action: apply
# Paunch cleanup example
- name: Cleanup containers for step 1 and step 2
  paunch:
    config_id:
      - tripleo_step1
      - tripleo_step2
    action: cleanup
"""


class PaunchManager:

    def __init__(self, module, results):

        super(PaunchManager, self).__init__()

        self.module = module
        self.results = results
        self.config = self.module.params['config']
        self.config_id = self.module.params['config_id']
        self.action = self.module.params['action']
        self.healthcheck_disabled = \
            self.module.params['healthcheck_disabled']
        self.container_cli = self.module.params['container_cli']
        self.container_log_stdout_path = \
            self.module.params['container_log_stdout_path']
        self.managed_by = self.module.params['managed_by']
        self.debug = self.module.params['debug']
        self.log_file = self.module.params['log_file']

        if self.debug:
            self.log_level = 3
        else:
            # if debug is disabled, only show WARNING level
            self.log_level = 1

        self.log = putils_common.configure_logging('paunch-ansible',
                                                   level=self.log_level,
                                                   log_file=self.log_file)

        if self.config:
            if os.path.isdir(self.config):
                container_configs = {}
                config_files = [c_json for c_json in
                                os.listdir(self.config)
                                if c_json.startswith('hashed-')
                                and c_json.endswith('.json')]
                for cf in config_files:
                    with open(os.path.join(self.config, cf), 'r') as f:
                        c = re.sub('^hashed-', '', os.path.splitext(cf)[0])
                        container_configs[c] = {}
                        container_configs[c].update(yaml.safe_load(f))
                self.config_yaml = container_configs
            else:
                with open(self.config, 'r') as f:
                    self.config_yaml = yaml.safe_load(f)

        if self.action == 'apply':
            self.paunch_apply()
        elif self.action == 'cleanup':
            self.paunch_cleanup()

    def paunch_apply(self):

        self.results['action'].append('Applying config_id %s' % self.config_id)
        if not self.config:
            self.module.fail_json(
                msg="Paunch apply requires 'config' parameter",
                stdout='',
                stderr='',
                rc=1)

        stdout_list, stderr_list, rc = p.apply(
            self.config_id,
            self.config_yaml,
            managed_by=self.managed_by,
            labels=[],
            cont_cmd=self.container_cli,
            log_level=self.log_level,
            log_file=self.log_file,
            cont_log_path=self.container_log_stdout_path,
            healthcheck_disabled=self.healthcheck_disabled
        )
        stdout, stderr = ["\n".join(i) for i in (stdout_list, stderr_list)]

        # Test paunch idempotency how we can.
        changed_strings = ['rm -f', 'Completed', 'Created']
        if any(s in stdout for s in changed_strings):
            self.results['changed'] = True

        self.results.update({"stdout": stdout, "stderr": stderr, "rc": rc})
        if rc != 0:
            self.module.fail_json(
                msg="Paunch failed with config_id %s" % self.config_id,
                stdout=stdout,
                stderr=stderr,
                rc=rc)

        self.module.exit_json(**self.results)

    def paunch_cleanup(self):

        self.results['action'].append('Cleaning-up config_id(s) '
                                      '%s' % self.config_id)
        p.cleanup(
            self.config_id,
            managed_by=self.managed_by,
            cont_cmd=self.container_cli,
            log_level=self.log_level,
            log_file=self.log_file
        )

        self.module.exit_json(**self.results)


def main():
    module = AnsibleModule(
        argument_spec=yaml.safe_load(DOCUMENTATION)['options'],
        supports_check_mode=False,
    )

    results = dict(
        changed=False,
        action=[]
    )

    PaunchManager(module, results)


if __name__ == '__main__':
    main()
