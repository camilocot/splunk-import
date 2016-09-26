#!/usr/bin/env python
# -*- coding: utf-8 -*-

from splunklib import client
import re
import sys
import getopt


def get_alerts(config):

    service = client.connect(
        host=config['hostname'],
        port=config['port'],
        username=config['username'],
        password=config['password'],
        owner=config['username'],
        app='search')
    return service.saved_searches


def filter_alerts(filterstring, entries):
    """docstring for filter_alerts"""
    result = []
    r = re.compile(filterstring, re.IGNORECASE)
    for savedsearch in entries:
        if re.search(r, savedsearch.name):
            result.append(savedsearch)
    return result


def create_alerts(config, entries):
    for alert in entries:
        print("Creating %s" % alert.name)


def print_usage():
    """docstring for print_usage"""
    print(
        "main.py -u <username> -p <password> -P <port> -f <filter> -H <hostname>")


def process_args(argv):
    """docstring for process_args"""
    config = {
        'port': 8089
    }

    try:
        opts, args = getopt.getopt(argv, 'hu:p:P:f:H:', [
                                   'help', 'username=', 'password=', 'port=', 'filter=', 'hostname='])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-u', '--username'):
            config['username'] = arg
        elif opt in ('-p', '--password'):
            config['password'] = arg
        elif opt in ('-P', '--port'):
            config['port'] = arg
        elif opt in ('-H', '--hostname'):
            config['hostname'] = arg
        elif opt in ('-f', '--filter'):
            config['filter'] = arg

    return config


def main(argv):
    """docstring for main"""

    config = process_args(argv)

    try:
        entries = get_alerts(config)
        result = filter_alerts(config['filter'], entries)
        create_alerts(config, result)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main(sys.argv[1:])
