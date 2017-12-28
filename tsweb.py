from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import getpass
import sys
import telnetlib
import socket

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.args.get('server'):
      try:
        socket.gethostbyname(request.args.get('server'))
      except:
        params = [['Author', '@UltraDesu']]
      else:
        host = request.args.get('server')
        telnet = telnetlib.Telnet(host,"10011")
        telnet.read_until(b'Welcome to the TeamSpeak 3 ServerQuery interface, type "help" for a list \
         of commands and "help <command>" for information on a specific command.\n')
        telnet.write(b"use 1 \n")
        telnet.write(b"serverinfo\n")
        telnet.write(b"quit\n")
        response = str(telnet.read_all())
        params = []
        for line in str(response[25:][:-47]).split():
          params.append(line.replace('\/','').replace('\\\\s', ' ').split('='))
      
    #   for param in params:
    #     try:
    #      print('{}="{}"'.format(param[0], param[1]))
    #     except:
    #      print('{}="{}"'.format(param[0], 'None'))
    else:
      params = [['Author', '@UltraDesu']]
    return render_template(
        'index.html',
        params=params
    )

if __name__ == '__main__':
    app.run(port=5050)
