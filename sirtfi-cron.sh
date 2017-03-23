#!/bin/bash      
# retrieve edugain metadata
curl http://mds.edugain.org/feed-sha256.xml > /var/sirtfi/edugain-metadata.xml
chmod 777 /var/sirtfi/edugain-metadata.xml

# run metadata aggregator
. /opt/pyff/bin/activate
pyff --loglevel=DEBUG /var/sirtfi/pipeline.fd
chmod +r /var/www/sirtfi/sirtfi-metadata.xml

python /var/sirtfi/sirtfi-simple-list.py -i /var/sirtfi/edugain-metadata.xml -o /var/www/sirtfi/table.txt

