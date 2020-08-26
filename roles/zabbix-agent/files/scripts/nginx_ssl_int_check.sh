#!/bin/bash

if [ -z ${2} ]; then
  echo -n > /tmp/crts.txt
  for incl in `grep include /etc/nginx/nginx.conf | grep -v '#' | awk '{print $2}' | tr -d ';' | sed '/^[a-z]/s/^/\/etc\/nginx\//'`; do
      crt=`cat ${incl} | grep -w ssl_certificate | grep -v "#" | awk '{print $2}' | sed 's/;//g' | sed '/^[a-z]/s/^/\/etc\/nginx\//'`
      echo ${crt} >> /tmp/crts.txt
  done
  certs=`grep -v "^$" /tmp/crts.txt`
  if [[ -n ${certs} ]]; then
    JSON="{ \"data\":["
    for CRT in ${certs}; do
  JSON=${JSON}"{ \"{#CERTIFICATE}\":\"${CRT}\"},"
    done
    JSON=${JSON}"]}"
   echo ${JSON}|sed '$s/,]}$/]}/'
  fi
else

f=$1
cert=$2

case $f in
-d)
end_date=`openssl x509 -noout -enddate -in $cert | cut -d '=' -f 2`

if [ -n "$end_date" ]
then
    end_date_seconds=`date '+%s' --date "$end_date"`
    now_seconds=`date '+%s'`
    echo "($end_date_seconds-$now_seconds)/24/3600" | bc
fi
;;

-i)
issue_dn=`openssl x509 -noout -text -in $cert |sed -n 's/ *Issuer: *//p'`

if [ -n "$issue_dn" ]
then
    issuer=`echo $issue_dn | sed -n 's/.*CN=*//p'`
    echo $issuer
fi
;;
*)
echo "usage: $0 [-i|-d] /path/to/crt"
echo "    -i Show Issuer"
echo "    -d Show valid days remaining"
;;
esac
fi
