Ansible-Nginx
=========
Role for install and configure nginx server

Role Variables
--------------

Dependencies
------------
Role use official nginx repo
https://nginx.org/ru/linux_packages.html#RHEL-CentOS

And custom modules
https://github.com/deepdivenow/nginx-modules

Example Playbook
----------------
    - hosts: cents
      name: nginx
      become: true
      roles:
        - ansible-nginx
      tags:
      - nginx

Custom site template usage:
---------------------------

    nginx_http_template:
      default:
        template_file: http/default.conf.j2
        conf_file_name: default.conf
        conf_file_location: /etc/nginx/conf.d/
        port: 8081
        server_name: localhost
        error_page: /usr/share/nginx/html
        root: /usr/share/nginx/html
        https_redirect: false
        autoindex: false
        ssl:
          cert: /etc/ssl/certs/default.crt
          key: /etc/ssl/private/default.key
        web_server:
          locations:
            default:
              location: /
              html_file_location: /usr/share/nginx/html
              html_file_name: index.html
              autoindex: false
              auth_basic: null
              auth_basic_file: null
          http_demo_conf: false
        reverse_proxy:
          proxy_cache_path:
            - path: /var/cache/nginx/proxy/backend
              keys_zone:
                name: backend_proxy_cache
                size: 10m
              levels: "1:2"
              max_size: 10g
              inactive: 60m
              use_temp_path: true
          proxy_temp_path:
            path: /var/cache/nginx/proxy/temp
          proxy_cache_lock: true
          proxy_cache_min_uses: 5
          proxy_cache_revalidate: true
          proxy_cache_use_stale:
            - error
            - timeout
          proxy_ignore_headers:
            - Expires
          locations:
            backend:
              location: /
              proxy_pass: http://backend
              proxy_cache: frontend_proxy_cache
              proxy_temp_path:
                path: /var/cache/nginx/proxy/backend/temp
              proxy_cache_lock: false
              proxy_cache_min_uses: 3
              proxy_cache_revalidate: false
              proxy_cache_use_stale:
                - http_403
                - http_404
              proxy_ignore_headers:
                - Vary
                - Cache-Control
              websocket: false
              auth_basic: null
              auth_basic_file: null
          health_check_plus: false
        proxy_cache:
          proxy_cache_path:
            path: /var/cache/nginx
            keys_zone:
              name: one
              size: 10m
          proxy_temp_path:
            path: /var/cache/nginx/proxy
        upstreams:
          upstream1:
            name: backend
            lb_method: least_conn
            zone_name: backend_mem_zone
            zone_size: 64k
            sticky_cookie: false
            servers:
              server1:
                address: localhost
                port: 8081
                weight: 1
                health_check: max_fails=1 fail_timeout=10s

License
-------

Apache

Author Information
------------------

Andrey Kislyak <andrey@kislyak.com>
