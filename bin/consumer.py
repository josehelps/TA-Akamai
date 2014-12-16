import re
import urllib
import json

# pull JSON from error_log
payload_rex = re.compile(r'\(data\-HEAP\)\:\s(?P<json>\{.+\}\})')
fh = open('/var/log/httpd/error_log')
p = 0

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
            #right now I am just pretty printing but this needs to be written to splunk.
            #looking into http://docs.splunk.com/Documentation/Splunk/6.2.0/AdvancedDev/ModInputsScripts
            print json.dumps(json_payload,sort_keys=True,indent=4, separators=(',', ': '))
