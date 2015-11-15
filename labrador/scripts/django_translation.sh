#!/usr/bin/env bash

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $THIS_DIR

# 翻译locales
cd ../templates/
django-admin.py makemessages -l zh_CN >/dev/null
django-admin.py compilemessages >/dev/null
echo `pwd`

cd ../labrador/
APPS_DIR=`pwd`

for i in `find $APPS_DIR -maxdepth 1 -type d`;
    do if [ `pwd` != $i ];then
        cd $i
        if [ -d $i/locale ];then
            django-admin.py makemessages -l zh_CN >/dev/null
            django-admin.py compilemessages >/dev/null
            echo $i
        fi
       fi
    done;
