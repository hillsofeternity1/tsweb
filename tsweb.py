from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import getpass
import sys
import telnetlib
import socket
import datetime

APP = Flask(__name__)
NOW = datetime.datetime.now()

@APP.route("/", methods=['GET'])
def index():
    if request.args.get('server'):
        try:
            # does host valid?
            socket.gethostbyname(request.args.get('server'))
        except:
            # if no, return stub
            params = {'Author': '@UltraDesu'}
        else:
            # oherwise proceed
            host = request.args.get('server')
            try:
                # does port valid? if no, use default port
                if int(request.args.get('port')):
                    port = request.args.get('port')
                else:
                    port = '10011'
            except:
                port = '10011'
            try:
                # trying to connect and fetch data via telnet server query protocol
                telnet = telnetlib.Telnet(host=host, port=port, timeout=3)
                telnet.read_until(b'Welcome to the TeamSpeak 3 ServerQuery '\
                  b'interface, type "help" for a list of commands and "help '\
                  b'<command>" for information on a specific command.\n')
                telnet.write(b"use 1 \n")
                telnet.write(b"serverinfo\n")
                telnet.write(b"quit\n")
                # here is response in raw text
                response = str(telnet.read_all())
                params = {}
                # here is parsing plain text server params.
                # drop some junk at the start and in the end
                # also make some cleanup
                for line in str(response[25:][:-47]).split():
                    try:
                        tmp = {line.\
                          replace('\/', '').\
                          replace('\\\\s', ' ').\
                          replace('\\', '/').\
                          split('=', 1)[0] : \
                          line.replace('\/', '').\
                          replace('\\\\s', ' ').\
                          replace('\\', '/').\
                          split('=', 1)[1]}
                    except:
                        tmp = {line.\
                          strip('/').\
                          replace('\/', '').\
                          replace('\\\\s', ' ').\
                          replace('\\', '/').\
                          split('=', 1)[0] : ""}
                    params = {**params, **tmp}
                # write simple log
                with open("checked_list.txt", "a") as checked_list:
                    checked_list.write("%s-%s - %s\n" % (NOW.month, NOW.day, host))
            except:
                params = {
                    'error': 'Provided server doesn\'t accessible',
                }
    else:
        # some stub info for filling html template
        params = {'Author': '@UltraDesu'}
        host = 'ts.hexor.ru'
        port = '10011'
    return render_template(
        'index.html',
        params=params,
        host=host,
        port=port,
        year=NOW.year
    )
# here is api implementation. Full server info in JSON. it works 
# exactly the same as /index page instead template used jsonify
@APP.route("/api/", methods=['GET'])
def api():
    if request.args.get('server'):
        try:
            socket.gethostbyname(request.args.get('server'))
        except:
            params = {
                'Accepted methods':'GET',
                'Accepted values':'server, port',
                'Author': '@UltraDesu'
            }
        else:
            host = request.args.get('server')
            try:
                if int(request.args.get('port')):
                    port = request.args.get('port')
                else:
                    port = '10011'
            except:
                port = '10011'
            telnet = telnetlib.Telnet(host, port=port, timeout=3)
            telnet.read_until(b'Welcome to the TeamSpeak 3 ServerQuery '\
              b'interface, type "help" for a list of commands and "help '\
              b'<command>" for information on a specific command.\n')
            telnet.write(b"use 1 \n")
            telnet.write(b"serverinfo\n")
            telnet.write(b"quit\n")
            response = str(telnet.read_all())
            params = {}
            # here is parsing plain text server params.
            for line in str(response[25:][:-47]).split():
                try:
                    tmp = {line.\
                      replace('\/', '').\
                      replace('\\\\s', ' ').\
                      replace('\\', '/').\
                      split('=', 1)[0] : \
                      line.replace('\/', '').\
                      replace('\\\\s', ' ').\
                      replace('\\', '/').\
                      split('=', 1)[1]}
                except:
                    tmp = {line.\
                      strip('/').\
                      replace('\/', '').\
                      replace('\\\\s', ' ').\
                      replace('\\', '/').\
                      split('=', 1)[0] : ""}
                params = {**params, **tmp}
    else:
        params = {
            'Accepted methods':'GET',
            'Accepted values':'server, port',
            'Author': '@UltraDesu'
        }
    return jsonify(params)

# starting app
if __name__ == '__main__':
    APP.run(port=5050)
