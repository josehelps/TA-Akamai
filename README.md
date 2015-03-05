TA-Akamai
=========

TA to consume logs from Akamai and Akamai cloud products like Kona. This handles both https and ftp method of delivery

## Requirements 

#### HTTPS/HTTP  method
* Apache 2.2 
* DumpIO module configured in Apache (see installation steps for details)

#### FTP method
* vsftp

## Installtion Steps
#### HTTP method
We have tested with CentOS 6.8 and Apache 2.2 cannot assure you will get the same results with other Distro/Apache versions

1. git clone this package
2. `yum install httpd` - install apache 
3. `vim /etc/httd/conf/httpd.conf` - uncomment the *LoadModule dumpio_module modules/mod_dumpio.so* module
4. `mv TA-Akamai/conf.examples/dumpio.conf /etc/httpd/conf.d/dumpio.conf` - add a config file to turn on DumpIO
5. `vim TA-Akamai/inputs.conf` edit your error log path for apache

#### Testing
If you need to test to make sure that you are indeed logging posts and they are landing on your error logs try running:
`curl -X POST https://127.0.0.1:4443/receiver.html -d '{"type":"cloud_monitor","format":"default","version":"1.0"}'`
If you are logging apache error logs under `/var/log/httpd/error_log` you should see 
`[Thu Mar 05 14:37:00 2015] [debug] mod_dumpio.c(74): mod_dumpio:  dumpio_out (data-HEAP): HTTP/1.1 200 OK\r\nDate: Thu, 05 Mar 2015 22:37:00 GMT\r\nServer: Apache/2.2.15 (Red Hat)\r\nLast-Modified: Thu, 05 Mar 2015 22:25:13 GMT\r\nETag: "fe-1a6-510920aa095c7"\r\nAccept-Ranges: bytes\r\nContent-Length: 422\r\nConnection: close\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n`
And under *$SPLUNK_HOME/etc/apps/TA-Akamai/log/akamai.log* you should see the full JSON object parsed as well. 
 

