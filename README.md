TA-Akamai
=========

TA to consume logs from Akamai and Akamai cloud products like Kona. Currently adds the HTTPS delivery method. Has some support (but no docs) for FTP delivery.

## Requirements 

#### HTTPS/HTTP  method
* Apache 2.2 
* DumpIO module configured in Apache (see installation steps for details)

#### FTP method
* vsftp

## Installtion Steps
### HTTP method installation
We have tested with CentOS 6.8 and Apache 2.2 cannot assure you will get the same results with other Distro/Apache versions

1. git clone this package
2. `yum install httpd mod_ssl` - install apache and mod\_ssl  
3. `vim /etc/httd/conf/httpd.conf` - uncomment the *LoadModule dumpio_module modules/mod_dumpio.so* module
4. `mv TA-Akamai/conf.examples/dumpio.conf /etc/httpd/conf.d/dumpio.conf` - add a config file to turn on DumpIO
5. `mv TA-Akamai/conf.examples/ssl.conf /etc/httpd/conf.d/ssl.conf` - add ssl config, make sure to replace <...snip...> with your configuration
6. `vim TA-Akamai/inputs.conf` edit your error log path for apache

#####Addtional considerataions:

* Make sure mod\_ssl is installed
* perform log rotate on `$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log` as it may grow very fast

#### Testing
If you need to test to make sure that you are indeed logging posts and they are landing on your error logs try running:

`curl -X POST https://172.16.138.153:8080/receiver.html -k -d '{ "type": "cloud_monitor", "format": "default", "version": "1.0", "message": { "reqPath": "/", "reqQuery": "action=test", "UA": "Googlebot/2.1 (+http://www.google.com/bot.html)"} , "reqHdr": { "accEnc": "gzip, deflate", "referer": "http://www.google.com", "cookie": "abc123" }}'`

If you are logging apache error logs under **/var/log/httpd/error_log** you should see: 

`[Thu Mar 05 14:37:00 2015] [debug] mod_dumpio.c(74): mod_dumpio:  dumpio_out (data-TRANSIENT): {"type":"cloud_monitor","format":"default","version":"1.0"}\r\n`

And under **$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log** you should see the full JSON object parsed as well. 
 
#### Troubleshooting
Most data of the app running is logged under `$SPLUNK_HOME/var/log/splunk/ta-akamai.log`

The app works in 3 phases and hence issues will show up in any of these three:

1. POST data should be written into apache error log. Make sure apache is running correctly (ssl and all) and dumpio/apache is set to log via debug.
2. Modular input after configured under `inputs.conf` will read in the error log and extract the Akamai logs (json objects) URL decode it and write it back into `$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log`
3. Splunk via `inputs.conf` ingest `$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log`, because it is a JSON object under props.conf we do `KV_MODE = json` and perform CIM compliance on `props.conf`

### FTP method installation
* Install vsftp service, create ftp user
Link to an example on how this can be done (steps in your environment may be different):
https://ostechnix.wordpress.com/2013/12/15/setup-ftp-server-step-by-step-in-centos-6-x-rhel-6-x-scientific-linux-6-x/
* FTP push is from akamai cloud service, most likely you will need to enable port forwarding to a specific directory where logs will be dropped to.
to set this up on akamai’s end, you will need to provide Akamai with:
ftp username
ftp password
ftp hostname / ip address
* Once logs are in, you will need to set up a monitor stanza to index the akamai logs:
inputs.conf
[monitor://$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log]
sourcetype=akamai
disabled = false
