import re
import urllib
import json
import sys
import logging
import xml.dom.minidom, xml.sax.saxutils

#set up logging suitable for splunkd comsumption
logging.root
logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

#Unless Akamai Changes the way they log this should not be modified
REX = '\(data\-HEAP\)\:\s(?P<json>\{.+\}\})'
#LOG_PATH = '/var/log/httpd/error_log'

#Defines a Scheme 
SCHEME = """<scheme>
    <title>TA-Akamai</title>
    <description>Consume data from Akamai Services. See README.md for inital configuration</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>simple</streaming_mode>
    <endpoint>
        <args>
            <arg name="log_path">
                <title>Log path of Apache Error logs</title>
                <description>This modular input expects Apache to be the HTTP listener for Akamai. README.md has instructions on how to configure it with DumpIO to collect payload. Provide path of error_log.</description>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

#introspection routine
def do_scheme(): 
    print SCHEME

def validate_config(log_path):
#check here to make sure file exist
    pass

# Empty validation routine. This routine is optional.
def validate_arguments(path_provided): 
    pass

def get_config():
    config = {}
    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))

        checkpnt_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpnt_node and checkpnt_node.firstChild and \
           checkpnt_node.firstChild.nodeType == checkpnt_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpnt_node.firstChild.data

        if not config:
            raise Exception, "Invalid configuration received from Splunk."
    
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

def get_akamai_data(REX,LOG_PATH,p):
    # pull JSON from error_log
    payload_rex = re.compile(REX)
    fh = open(LOG_PATH)

  

    #loop that reads throug the error log
    while True:
        fh.seek(p)
        latest_data = fh.read()
        p = fh.tell()
        if latest_data:
            #match the payload
            payload = payload_rex.search(latest_data)
            if payload:
                #turn payload into json
                json_payload = payload.group('json')
                json_payload = json.loads(json_payload)
             
                #URL decode the appropiate fields 
                for ids,content in json_payload.iteritems():
                    if ids == 'message':
                        content['UA'] = urllib.unquote(content['UA']).decode('utf8')
                        content['reqPath'] = urllib.unquote(content['reqPath']).decode('utf8')
                        content['reqQuery'] = urllib.unquote(content['reqQuery']).decode('utf8')
                    if ids == 'reqHdr':
                        content['accEnc'] = urllib.unquote(content['accEnc']).decode('utf8')
                        content['referer'] = urllib.unquote(content['referer']).decode('utf8')
                        content['cookie'] = urllib.unquote(content['cookie']).decode('utf8')
                
                
                return json_payload,p

# Routine to index data
def run(): 
    config = get_config()
    logging.info(config)
    log_path = config['log_path']
    logging.debug('TA-Akamai has been configured with with path {0}'.format(log_path))

    p = 0

    while True:
        
        results,p = get_akamai_data(REX,log_path,p)
        print json.dumps(results,sort_keys=True)
        sleep(2)
        #print json.dumps(results,sort_keys=True,indent=4, separators=(',', ': '))

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            if len(sys.argv)>2:
                validate_arguments(sys.argv[2])
            else:
                print 'supply error_log for apache'
        elif sys.arg[1] == "--test":
            print 'No test for the scheme present'
        else:
            print 'Argggs provided incorrect'
    else:
        run()

    sys.exit(0)


