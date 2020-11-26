# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: k8s_nodes
    plugin_type: inventory
    author:
      - Mikalai Davydzenka <mikalai.davydzenka@gmail.com>

    short_description: Kubernetes nodes inventory source

    description:
      - Fetch k8s nodes from cluster.

'''

EXAMPLES = '''
# File
'''

import json

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
import kubernetes.client
import kubernetes.config
from kubernetes.client.rest import ApiException

# TODO: add cache support
#   https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#inventory-cache

class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'k8s_nodes'

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path)

        kubernetes.config.load_kube_config()
        api_instance = kubernetes.client.CoreV1Api()

        try:
            list_nodes = api_instance.list_node()
        except ApiException as e:
            self.display.debug(e)
            raise AnsibleError(
                f"Inventory plugin {InventoryModule.NAME}: "
                f"Exception when calling CoreV1Api->list_node: {e}"
            )

        self.inventory.add_group("k8s_nodes")
        self.inventory.add_group("k8s_masters")
        self.inventory.add_group("k8s_workers")

        for node in list_nodes.items:
            host = None
            for address in node.status.addresses:
                if address.type == "Hostname":
                    host = address.address
            if not host:
                self.display.debug(
                    f"Inventory plugin {InventoryModule.NAME}: "
                    f"{node.metadata.name} - HostName address not found"
                )
                continue
            labels = dict(node.metadata.labels)
            annotations = dict(node.metadata.annotations)

            self.inventory.add_host(host)
            self.inventory.add_child("k8s_nodes", host)
            if labels.get("node-role.kubernetes.io/master", False):
                self.inventory.add_child("k8s_masters", host)
            else:
                self.inventory.add_child("k8s_workers", host)
            self.inventory.set_variable(host, 'labels', labels)
            self.inventory.set_variable(host, 'annotations', annotations)
            # TODO: add more variables, almost all from 'spec' and 'status'
