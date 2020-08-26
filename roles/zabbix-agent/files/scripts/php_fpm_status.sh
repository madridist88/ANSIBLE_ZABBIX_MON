#!/bin/bash

if [ -z ${2} ]; then
        pools=`ps aux | grep php-fpm.*poo[l] | sed -e 's/.*php.*pool\ //g' | sort | uniq`
        json="{ \"data\":["
        for pool in ${pools}; do
        json=${json}"{ \"{#POOL}\":\"${pool}\"},"
        done
        json=${json}"]}"
        echo ${json}|sed '$s/,]}$/]}/'
else

POOL=$2

general_conf=`ps aux | grep php-fpm.*maste[r] | sed -e 's/.*(//' -e 's/).*//'`
includes=`grep include= /etc/php-fpm.conf | sed 's/include=//g'`
echo -n  > /tmp/php_pool_incl.txt
for incl in ${includes}; do
  grep -lrw ${POOL} ${incl} >> /tmp/php_pool_incl.txt
done
pool_incl=`cat /tmp/php_pool_incl.txt | grep -v '^$'`
POOL_SOCKET=`grep -w 'listen' ${pool_incl} | grep -E '\:' | head -1 | sed -e 's/listen.*=//g' -e "s/pool/$POOL/g" | tr -d ' $'`

function rps() {
      current_req=`SCRIPT_NAME="/fpm71-status-${POOL}" SCRIPT_FILENAME="/fpm71-status-${POOL}" REQUEST_METHOD=GET cgi-fcgi -bind -connect ${POOL_SOCKET} | grep -w '^accepted conn' |  tr -d ' ' | awk -F ':' '{print $2}'`
      current_date=`date +%s`
      prev_date=`cat /tmp/fpm_$POOL_prev_req.txt | awk '{print $1}'`
      prev_req=`cat /tmp/fpm_$POOL_prev_req.txt | awk '{print $2}'`
      rps=`echo "scale=3;(($current_req-$prev_req)/($current_date-$prev_date))" | bc -l | awk '{printf "%.3f\n", $0}'`
      echo "$current_date $current_req" > /tmp/fpm_$POOL_prev_req.txt
      echo $rps
}
function max_child() {
        SCRIPT_NAME="/fpm71-status-${POOL}" SCRIPT_FILENAME="/fpm71-status-${POOL}" REQUEST_METHOD=GET cgi-fcgi -bind -connect ${POOL_SOCKET} | grep -w '^max active processes' | tr -d ' ' | awk -F ':' '{print $2}'
}
function active() {
        SCRIPT_NAME="/fpm71-status-${POOL}" SCRIPT_FILENAME="/fpm71-status-${POOL}" REQUEST_METHOD=GET cgi-fcgi -bind -connect ${POOL_SOCKET} | grep -w '^active processes' |  tr -d ' ' | awk -F ':' '{print $2}'
}
function total() {
        SCRIPT_NAME="/fpm71-status-${POOL}" SCRIPT_FILENAME="/fpm71-status-${POOL}" REQUEST_METHOD=GET cgi-fcgi -bind -connect ${POOL_SOCKET} | grep -w '^total processes' |  tr -d ' ' | awk -F ':' '{print $2}'
}
function idle() {
        SCRIPT_NAME="/fpm71-status-${POOL}" SCRIPT_FILENAME="/fpm71-status-${POOL}" REQUEST_METHOD=GET cgi-fcgi -bind -connect ${POOL_SOCKET} | grep -w '^idle processes' |  tr -d ' ' | awk -F ':' '{print $2}'
}
case "$1" in
        rps)
                rps;;
        max_child)
                max_child;;
        active)
                active;;
        total)
                total;;
        idle)
                idle;;
        *)
                echo $"Usage $0 {check|rps|max_child|active|total|idle}"
                exit
esac
fi
