#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, sky-joker
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: zabbix_user
short_description: Create/update/delete Zabbix users
author:
    - sky-joker (@sky-joker)
version_added: '2.10'
description:
    - This module allows you to create, modify and delete Zabbix users.
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    alias:
        description:
            - Name of the user alias in Zabbix.
            - alias is the unique identifier used and cannot be updated using this module.
        required: true
        type: str
    name:
        description:
            - Name of the user.
        default: ''
        type: str
    surname:
        description:
            - Surname of the user.
        default: ''
        type: str
    usrgrps:
        description:
            - User groups to add the user to.
        required: true
        type: list
        elements: str
    passwd:
        description:
            - User's password.
        required: true
        type: str
    override_passwd:
        description:
            - Override password.
        default: no
        type: bool
    lang:
        description:
            - Language code of the user's language.
        default: 'en_GB'
        choices:
            - 'en_GB'
            - 'en_US'
            - 'zh_CN'
            - 'cs_CZ'
            - 'fr_FR'
            - 'he_IL'
            - 'it_IT'
            - 'ko_KR'
            - 'ja_JP'
            - 'nb_NO'
            - 'pl_PL'
            - 'pt_BR'
            - 'pt_PT'
            - 'ru_RU'
            - 'sk_SK'
            - 'tr_TR'
            - 'uk_UA'
        type: str
    theme:
        description:
            - User's theme.
        default: 'default'
        choices:
            - 'default'
            - 'blue-theme'
            - 'dark-theme'
        type: str
    autologin:
        description:
            - Whether to enable auto-login.
            - If enable autologin, cannot enable autologout.
        default: false
        type: bool
    autologout:
        description:
            - User session life time in seconds. If set to 0, the session will never expire.
            - If enable autologout, cannot enable autologin.
        default: '0'
        type: str
    refresh:
        description:
            - Automatic refresh period in seconds.
        default: '30'
        type: str
    rows_per_page:
        description:
            - Amount of object rows to show per page.
        default: '50'
        type: str
    after_login_url:
        description:
            - URL of the page to redirect the user to after logging in.
        default: ''
        type: str
    user_medias:
        description:
            - Set the user's media.
        default: []
        suboptions:
            mediatype:
                description:
                    - Media type name to set.
                default: 'Email'
                type: str
            sendto:
                description:
                    - Address, user name or other identifier of the recipient.
                required: true
                type: str
            period:
                description:
                    - Time when the notifications can be sent as a time period or user macros separated by a semicolon.
                    - Please review the documentation for more information on the supported time period.
                    - https://www.zabbix.com/documentation/4.0/manual/appendix/time_period
                default: '1-7,00:00-24:00'
                type: str
            severity:
                description:
                    - Trigger severities to send notifications about.
                suboptions:
                   not_classified:
                       description:
                           - severity not_classified enable/disable.
                       default: True
                       type: bool
                   information:
                       description:
                           - severity information enable/disable.
                       default: True
                       type: bool
                   warning:
                       description:
                           - severity warning enable/disable.
                       default: True
                       type: bool
                   average:
                       description:
                           - severity average enable/disable.
                       default: True
                       type: bool
                   high:
                       description:
                           - severity high enable/disable.
                       default: True
                       type: bool
                   disaster:
                       description:
                           - severity disaster enable/disable.
                       default: True
                       type: bool
                default:
                  not_classified: True
                  information: True
                  warning: True
                  average: True
                  high: True
                  disaster: True
                type: dict
            active:
                description:
                    - Whether the media is enabled.
                default: true
                type: bool
        type: list
        elements: dict
    type:
        description:
            - Type of the user.
        default: 'Zabbix user'
        choices:
            - 'Zabbix user'
            - 'Zabbix admin'
            - 'Zabbix super admin'
        type: str
    state:
        description:
            - State of the user.
            - On C(present), it will create if user does not exist or update the user if the associated data is different.
            - On C(absent) will remove a user if it exists.
        default: 'present'
        choices: ['present', 'absent']
        type: str
extends_documentation_fragment:
  - zabbix
'''

EXAMPLES = r'''
- name: create of zabbix user.
  zabbix_user:
    server_url: "http://zabbix.example.com/zabbix/"
    login_user: Admin
    login_password: secret
    alias: example
    name: user name
    surname: user surname
    usrgrps:
      - Guests
      - Disabled
    passwd: password
    lang: en_GB
    theme: blue-theme
    autologin: no
    autologout: '0'
    refresh: '30'
    rows_per_page: '200'
    after_login_url: ''
    user_medias:
      - mediatype: Email
        sendto: example@example.com
        period: 1-7,00:00-24:00
        severity:
          not_classified: no
          information: yes
          warning: yes
          average: yes
          high: yes
          disaster: yes
        active: no
    type: Zabbix super admin
    state: present

- name: delete of zabbix user.
  zabbix_user:
    server_url: "http://zabbix.example.com/zabbix/"
    login_user: admin
    login_password: secret
    alias: example
    usrgrps:
      - Guests
    passwd: password
    user_medias:
      - sendto: example@example.com
    state: absent
'''

RETURN = r'''
user_ids:
    description: User id created or changed
    returned: success
    type: dict
    sample: { "userids": [ "5" ] }
'''

import atexit
import traceback

try:
    from zabbix_api import ZabbixAPI
    from zabbix_api import Already_Exists

    HAS_ZABBIX_API = True
except ImportError:
    ZBX_IMP_ERR = traceback.format_exc()
    HAS_ZABBIX_API = False

from distutils.version import LooseVersion
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import copy


class User(object):
    def __init__(self, module, zbx):
        self._module = module
        self._zapi = zbx

    def check_user_exist(self, alias):
        zbx_user = self._zapi.user.get({'output': 'extend', 'filter': {'alias': alias},
                                        'getAccess': True, 'selectMedias': 'extend',
                                        'selectUsrgrps': 'extend'})
        return zbx_user


    def passwd(self, zbx_user, alias, passwd, zbx_api_version):

        user_ids = {}

        request_data = {
            'userid': zbx_user[0]['userid'],
            'alias': alias,
            'passwd': passwd
        }

        try:
            user_ids = self._zapi.user.update(request_data)
        except Exception as e:
            self._module.fail_json(msg="Failed to update user %s: %s" % (alias, e))

        return user_ids


def main():
    module = AnsibleModule(
        argument_spec=dict(
            server_url=dict(type='str', required=True, aliases=['url']),
            login_user=dict(type='str', required=True),
            login_password=dict(type='str', required=True, no_log=True),
            http_login_user=dict(type='str', required=False, default=None),
            http_login_password=dict(type='str', required=False, default=None, no_log=True),
            validate_certs=dict(type='bool', required=False, default=True),
            alias=dict(type='str', required=True),
            passwd=dict(type='str', required=True, no_log=True),
            timeout=dict(type='int', default=10)
        ),
        supports_check_mode=True
    )

    if not HAS_ZABBIX_API:
        module.fail_json(msg=missing_required_lib('zabbix-api', url='https://pypi.org/project/zabbix-api/'),
                         exception=ZBX_IMP_ERR)

    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    alias = module.params['alias']
    passwd = module.params['passwd']
    timeout = module.params['timeout']

    zbx = None

    # login to zabbix
    try:
        zbx = ZabbixAPI(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password,
                        validate_certs=validate_certs)
        zbx.login(login_user, login_password)
        atexit.register(zbx.logout)
    except Exception as e:
        module.fail_json(msg="Failed to connect to Zabbix server: %s" % e)

    user = User(module, zbx)

    user_ids = {}
    zbx_api_version = zbx.api_version()[:3]
    zbx_user = user.check_user_exist(alias)

    if zbx_user:
        user_ids = user.passwd(zbx_user, alias, passwd, zbx_api_version)

    module.exit_json(changed=True, user_ids=user_ids)

if __name__ == "__main__":
    main()
