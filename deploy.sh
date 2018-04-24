#!/bin/bash
if [ "$#" -ne 9 ]; then
    echo "Illegal number of parameters"
    echo "deploy.sh FSID ZOOKEEPER_HOST ZOOKEEPER_USERNAME ZOOKEEPER_PASSWORD SERVERHOSTNAME SERVER_PORT SERVER_SCHEME HMACKEY CONTEXT"
    echo "e.g. ../deploy.sh  FSX snf-814985.vm.okeanos.grnet.gr username password snf-814985.vm.okeanos.grnet.gr 8080 http 7vjTsO0IhSZsNA6ze37Dk/xXw2nphFM9ZAMUkwXgaAA= fileservicejava"
    exit -1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ID=$1 > "$DIR/config.properties"
echo ZOOKEEPER_HOST=$2 >> "$DIR/config.properties"
echo ZOOKEEPER_USER=$3 >> "$DIR/config.properties"
echo ZOOKEEPER_PASSWORD=$4 >> "$DIR/config.properties"
echo SERVERHOSTNAME=$5 >> "$DIR/config.properties"
echo SERVER_PORT=$6 >> "$DIR/config.properties"
echo SERVER_SCHEME=$7 >> "$DIR/config.properties"
echo HMACKEY=$8 >> "$DIR/config.properties"
echo CONTEXT=$9 >> "$DIR/config.properties"


# after deploying, reload apache and wait some time to allow zookeeper to delete a possible previous ephemeral node. Then call status url to reconnect
cd $DIR \
&& rsync -a -v --exclude deploy.sh --exclude .git --exclude data --delete $DIR/ root@$5:/var/www/fileservicepython \
&& ssh root@$5 "chown -R www-data:www-data /var/www/fileservicepython && service apache2 reload && sleep 20 && wget $7://$5:$6/$9/status -O -"
cd $DIR

# ./deploy.sh  PFS2 snf-814985.vm.okeanos.grnet.gr username password snf-816668.vm.okeanos.grnet.gr 80 http 7vjTsO0IhSZsNA6ze37Dk/xXw2nphFM9ZAMUkwXgaAA= fileservicepython
# ./deploy.sh  PFS1 snf-814985.vm.okeanos.grnet.gr username password snf-814985.vm.okeanos.grnet.gr 80 http 7vjTsO0IhSZsNA6ze37Dk/xXw2nphFM9ZAMUkwXgaAA= fileservicepython
# http://snf-814985.vm.okeanos.grnet.gr/fileservicepython/file/aaa.png
# http://snf-816668.vm.okeanos.grnet.gr/fileservicepython/file/aaa.png
