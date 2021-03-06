#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) me@mimiko.me
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

RETURN = r'''
---
hosts:
  description: List of Zabbix hosts. See https://www.zabbix.com/documentation/3.4/manual/api/reference/host/get for list of host values.
  returned: success
  type: dict
  sample: [ { "available": "1", "description": "", "disable_until": "0", "error": "", "flags": "0", "groups": ["1"], "host": "Host A", ... } ]
'''

DOCUMENTATION = r'''
---
module: zabbix_login_try
short_description: Gather information about Zabbix host
description:
   - This module allows you to search for Zabbix host entries.
   - This module was called C(zabbix_host_facts) before Ansible 2.9. The usage did not change.
version_added: "2.7"
author:
    - "Michael Miko (@RedWhiteMiko)"
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
'''

EXAMPLES = r'''
- name: Get host info
  local_action:
    module: zabbix_login_try
    server_url: http://monitor.example.com
    login_user: username
    login_password: password
'''


import atexit
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

try:
    from zabbix_api import ZabbixAPI
    HAS_ZABBIX_API = True
except ImportError:
    ZBX_IMP_ERR = traceback.format_exc()
    HAS_ZABBIX_API = False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            server_url=dict(type='str', required=True, aliases=['url']),
            login_user=dict(type='str', required=True),
            login_password=dict(type='str', required=True, no_log=True),
            http_login_user=dict(type='str', required=False, default=None),
            http_login_password=dict(type='str', required=False, default=None, no_log=True),
            validate_certs=dict(type='bool', required=False, default=True),
            timeout=dict(type='int', default=10)
        ),
        supports_check_mode=True
    )
    if module._name == 'zabbix_host_facts':
        module.deprecate("The 'zabbix_host_facts' module has been renamed to 'zabbix_host_info'", version='2.13')

    if not HAS_ZABBIX_API:
        module.fail_json(msg=missing_required_lib('zabbix-api', url='https://pypi.org/project/zabbix-api/'), exception=ZBX_IMP_ERR)

    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    timeout = module.params['timeout']

    zbx = None
    # login to zabbix
    try:
        zbx = ZabbixAPI(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password,
                        validate_certs=validate_certs)
        zbx.login(login_user, login_password)
        atexit.register(zbx.logout)
    except Exception as ex:
        if 'urllib2.URLError' in str(ex):
            module.fail_json(msg="Failed to connect to Zabbix server: %s" % ex)
        else:
            module.exit_json(ok=False, result="User login fail", error=str(ex))

    module.exit_json(ok=True, result="User login OK")


if __name__ == '__main__':
    main()
