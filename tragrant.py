#!/usr/bin/env python2

import ConfigParser
import smtplib
import subprocess
import sys
import time
from optparse import OptionParser

class Watcher:
    def __init__(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.process = config.get('DEFAULT', 'process_to_monitor')
        self.smtp_server = config.get('DEFAULT', 'smtp_server')
        self.email = config.get('DEFAULT', 'email_addr')
        self.passwd = config.get('DEFAULT', 'email_passwd')
        self.text_addr = config.get('DEFAULT', 'text_addr')

    def wait_for_process(self):
        process_status = 0
        while process_status != -1:
            process_status = self.query_process()
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
    
    def query_process(self):
        p = subprocess.Popen(["ps", "axu"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, 
                stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        check = out.find(self.process)
        return check
    
    def send_text(self):
        server = smtplib.SMTP(self.smtp_server)
        server.login(self.email, self.passwd)
        server.sendmail(self.email, self.text_addr, 
                        '%s has finished! :-D :-D' % self.process)
        server.quit()
    
def parse_args():
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config', default=None,
                      help='Config file to use')
    return parser.parse_args()
    
def main():
    (options, args) = parse_args()
    if not options.config:
        print "Input a config file!"
        return 

    watch = Watcher(options.config)
    watch.wait_for_process()
    watch.send_text()
    print "ok"

if __name__ == '__main__':
    main()
