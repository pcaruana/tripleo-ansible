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

import json
import yaml

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.six as six

six.add_metaclass(type)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: podman_container_info
author:
    - Sagi Shnaidman (@sshnaidm)
    - Emilien Macchi (@EmilienM)
version_added: '2.9'
short_description: Gather facts about containers using podman
notes:
    - Podman may required elevated privileges in order to run properly.
description:
    - Gather facts about containers using C(podman)
requirements:
    - "Podman installed on host"
options:
    executable:
        description:
            - Path to C(podman) executable if it is not in the C($PATH) on the
              machine running C(podman)
        default: 'podman'
        type: str
    name:
        description:
            - List of tags or UID to gather facts about. If no name is given
              return facts about all containers.
        type: list
        elements: str

"""

EXAMPLES = """
- name: Gather facts for all containers
  podman_container_info:

- name: Gather facts on a specific container
  podman_container_info:
    name: web1

- name: Gather facts on several containers
  podman_container_info:
    name:
      - redis
      - web1
"""

RETURN = """
containers:
    description: Facts from all or specificed containers
    returned: always
    type: dict
    sample: [
        {
            "Id": "c5c39f9b80a6ea2ad665aa9946435934e478a0c5322da835f3883872f",
            "Created": "2019-10-01T12:51:00.233106443Z",
            "Path": "dumb-init",
            "Args": [
                "--single-child",
                "--",
                "kolla_start"
            ],
            "State": {
                "OciVersion": "1.0.1-dev",
                "Status": "configured",
                "Running": false,
                "Paused": false,
                "Restarting": false,
                "OOMKilled": false,
                "Dead": false,
                "Pid": 0,
                "ExitCode": 0,
                "Error": "",
                "StartedAt": "0001-01-01T00:00:00Z",
                "FinishedAt": "0001-01-01T00:00:00Z",
                "Healthcheck": {
                    "Status": "",
                    "FailingStreak": 0,
                    "Log": null
                }
            },
            "Image": "0e267acda67d0ebd643e900d820a91b961d859743039e620191ca1",
            "ImageName": "docker.io/tripleomaster/centos-haproxy:latest",
            "Rootfs": "",
            "Pod": "",
            "ResolvConfPath": "",
            "HostnamePath": "",
            "HostsPath": "",
            "OCIRuntime": "runc",
            "Name": "haproxy",
            "RestartCount": 0,
            "Driver": "overlay",
            "MountLabel": "system_u:object_r:svirt_sandbox_file_t:s0:c78,c866",
            "ProcessLabel": "system_u:system_r:svirt_lxc_net_t:s0:c785,c866",
            "AppArmorProfile": "",
            "EffectiveCaps": [
                "CAP_CHOWN",
                "CAP_DAC_OVERRIDE",
                "CAP_FSETID",
                "CAP_FOWNER",
                "CAP_MKNOD",
                "CAP_NET_RAW",
                "CAP_SETGID",
                "CAP_SETUID",
                "CAP_SETFCAP",
                "CAP_SETPCAP",
                "CAP_NET_BIND_SERVICE",
                "CAP_SYS_CHROOT",
                "CAP_KILL",
                "CAP_AUDIT_WRITE"
            ],
            "BoundingCaps": [
                "CAP_CHOWN",
                "CAP_DAC_OVERRIDE",
                "CAP_FSETID",
                "CAP_FOWNER",
                "CAP_MKNOD",
                "CAP_NET_RAW",
                "CAP_SETGID",
                "CAP_SETUID",
                "CAP_SETFCAP",
                "CAP_SETPCAP",
                "CAP_NET_BIND_SERVICE",
                "CAP_SYS_CHROOT",
                "CAP_KILL",
                "CAP_AUDIT_WRITE"
            ],
            "ExecIDs": [],
            "GraphDriver": {
                "Name": "overlay",
                }
            },
            "Mounts": [],
            "Dependencies": [],
            "NetworkSettings": {
                "Bridge": "",
                "SandboxID": "",
                "HairpinMode": false,
                "LinkLocalIPv6Address": "",
                "LinkLocalIPv6PrefixLen": 0,
                "Ports": [],
                "SandboxKey": "",
                "SecondaryIPAddresses": null,
                "SecondaryIPv6Addresses": null,
                "EndpointID": "",
                "Gateway": "",
                "GlobalIPv6Address": "",
                "GlobalIPv6PrefixLen": 0,
                "IPAddress": "",
                "IPPrefixLen": 0,
                "IPv6Gateway": "",
                "MacAddress": ""
            },
            "ExitCommand": [
                "/usr/bin/podman",
                "--root",
                "/var/lib/containers/storage",
                "--runroot",
                "/var/run/containers/storage",
                "--log-level",
                "error",
                "--cgroup-manager",
                "systemd",
                "--tmpdir",
                "/var/run/libpod",
                "--runtime",
                "runc",
                "--storage-driver",
                "overlay",
                "--events-backend",
                "journald",
                "container",
                "cleanup",
                "c9e813703f9b80a6ea2ad665aa9946435934e478a0c5322da835f3883872f"
            ],
            "Namespace": "",
            "IsInfra": false,
            "Config": {
                "Hostname": "c5c39e813703",
                "Domainname": "",
                "User": "",
                "AttachStdin": false,
                "AttachStdout": false,
                "AttachStderr": false,
                "Tty": false,
                "OpenStdin": false,
                "StdinOnce": false,
                "Env": [
                    "PATH=/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                    "TERM=xterm",
                    "HOSTNAME=",
                    "container=oci",
                    "KOLLA_INSTALL_METATYPE=rdo",
                    "KOLLA_BASE_DISTRO=centos",
                    "KOLLA_INSTALL_TYPE=binary",
                    "KOLLA_DISTRO_PYTHON_VERSION=2.7",
                    "KOLLA_BASE_ARCH=x86_64"
                ],
                "Cmd": [
                    "kolla_start"
                ],
                "Image": "docker.io/tripleomaster/centos-haproxy:latest",
                "Volumes": null,
                "WorkingDir": "/",
                "Entrypoint": "dumb-init --single-child --",
                "OnBuild": null,
                "Labels": {
                    "build-date": "20190919",
                    "kolla_version": "8.1.0",
                    "name": "haproxy",
                    "org.label-schema.build-date": "20190801",
                    "org.label-schema.license": "GPLv2",
                    "org.label-schema.name": "CentOS Base Image",
                    "org.label-schema.schema-version": "1.0",
                    "org.label-schema.vendor": "CentOS"
                },
                "Annotations": {
                    "io.kubernetes.cri-o.ContainerType": "sandbox",
                    "io.kubernetes.cri-o.TTY": "false",
                    "io.podman.annotations.autoremove": "FALSE",
                    "io.podman.annotations.init": "FALSE",
                    "io.podman.annotations.privileged": "FALSE",
                    "io.podman.annotations.publish-all": "FALSE"
                },
                "StopSignal": 15
            },
            "HostConfig": {
                "Binds": [],
                "ContainerIDFile": "",
                "LogConfig": {
                    "Type": "k8s-file",
                    "Config": null
                },
                "NetworkMode": "default",
                "PortBindings": {},
                "RestartPolicy": {
                    "Name": "",
                    "MaximumRetryCount": 0
                },
                "AutoRemove": false,
                "VolumeDriver": "",
                "VolumesFrom": null,
                "CapAdd": [],
                "CapDrop": [],
                "Dns": [],
                "DnsOptions": [],
                "DnsSearch": [],
                "ExtraHosts": [],
                "GroupAdd": [],
                "IpcMode": "",
                "Cgroup": "",
                "Links": null,
                "OomScoreAdj": 0,
                "PidMode": "",
                "Privileged": false,
                "PublishAllPorts": false,
                "ReadonlyRootfs": false,
                "SecurityOpt": [],
                "Tmpfs": {},
                "UTSMode": "",
                "UsernsMode": "",
                "ShmSize": 65536000,
                "Runtime": "oci",
                "ConsoleSize": [
                    0,
                    0
                ],
                "Isolation": "",
                "CpuShares": 0,
                "Memory": 0,
                "NanoCpus": 0,
                "CgroupParent": "",
                "BlkioWeight": 0,
                "BlkioWeightDevice": null,
                "BlkioDeviceReadBps": null,
                "BlkioDeviceWriteBps": null,
                "BlkioDeviceReadIOps": null,
                "BlkioDeviceWriteIOps": null,
                "CpuPeriod": 0,
                "CpuQuota": 0,
                "CpuRealtimePeriod": 0,
                "CpuRealtimeRuntime": 0,
                "CpusetCpus": "",
                "CpusetMems": "",
                "Devices": [],
                "DiskQuota": 0,
                "KernelMemory": 0,
                "MemoryReservation": 0,
                "MemorySwap": 0,
                "MemorySwappiness": -1,
                "OomKillDisable": false,
                "PidsLimit": 0,
                "Ulimits": [
                    {
                        "Name": "RLIMIT_NOFILE",
                        "Soft": 1048576,
                        "Hard": 1048576
                    },
                    {
                        "Name": "RLIMIT_NPROC",
                        "Soft": 1048576,
                        "Hard": 1048576
                    }
                ],
                "CpuCount": 0,
                "CpuPercent": 0,
                "IOMaximumIOps": 0,
                "IOMaximumBandwidth": 0
            }
        }
    ]
"""


def get_containers_facts(module, executable, name):
    if not name:
        all_names = [executable, 'container', 'ls', '-q', '-a']
        rc, out, err = module.run_command(all_names)
        name = out.split()
        if not name:
            return [], out, err
    command = [executable, 'container', 'inspect']
    command.extend(name)
    rc, out, err = module.run_command(command)
    if not out or rc != 0:
        return [], out, err
    return json.loads(out), out, err


def main():
    module = AnsibleModule(
        argument_spec=yaml.safe_load(DOCUMENTATION)['options'],
        supports_check_mode=True,
    )

    executable = module.params['executable']
    name = module.params.get('name')
    executable = module.get_bin_path(executable, required=True)

    inspect_results, out, err = get_containers_facts(module, executable, name)

    results = dict(
        changed=False,
        containers=inspect_results,
        ansible_facts=dict(podman_containers=inspect_results),
        stdout=out,
        stderr=err
    )

    module.exit_json(**results)


if __name__ == '__main__':
    main()
