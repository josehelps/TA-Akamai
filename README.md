TA-Akamai
=========

TA to consume logs from Akamai and Akamai cloud products like Kona. This handles both https and ftp method of delivery

## Requirements 
### HTTPS/HTTP  method
* Apache 2.2 
* DumpIO module configured in Apache (see installation steps for details)
### FTP method
* vsftp

## Installtion Steps
### http
We have tested with CentOS 6.8 and Apache 2.2 cannot assure you will get the same results with other Distro/Apache versions

1. git clone this package
2. `yum install httpd` - install apache 
3. `vim /etc/httd/conf/httpd.conf` - uncomment the *LoadModule dumpio_module modules/mod_dumpio.so* module
4. `mv TA-Akamai/conf.examples/dumpio.conf /etc/httpd/conf.d/dumpio.conf` - add a config file to turn on DumpIO

