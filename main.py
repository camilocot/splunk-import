#!/usr/bin/env python
# -*- coding: utf-8 -*-

from splunklib import client
import re
import sys
import getopt
import getpass


def get_alerts(config):

    service = client.connect(
        host=config['sourcehostname'],
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

def gen_savedsearch_alert_param(alert):
    """docstring for gen_alert_param"""
    keep_fields =  ['is_visible', 'display.visualizations.charting.axisTitleY.visibility', 'display.visualizations.charting.axisTitleX.visibility', 'dispatch.max_count', 'display.events.fields', 'display.page.search.patterns.sensitivity', 'actions', 'disabled', 'display.visualizations.charting.axisY.maximumNumber', 'alert.suppress.period', 'display.events.list.drilldown', 'auto_summarize.dispatch.ttl', 'display.visualizations.charting.axisTitleY2.text', 'embed.enabled', 'dispatch.latest_time', 'vsid', 'display.visualizations.charting.chart.bubbleMaximumSize', 'auto_summarize.max_summary_size', 'display.general.type', 'display.visualizations.show', 'dispatch.auto_cancel', 'dispatch.time_format', 'display.visualizations.charting.axisY2.scale', 'display.events.table.drilldown', 'display.visualizations.mapping.markerLayer.markerOpacity', 'realtime_schedule', 'display.visualizations.mapping.map.center', 'display.visualizations.charting.axisTitleY2.visibility', 'auto_summarize.timespan', 'display.visualizations.charting.axisY2.minimumNumber', 'display.visualizations.charting.chart.sliceCollapsingThreshold', 'alert.digest_mode', 'auto_summarize.command', 'display.visualizations.charting.axisTitleX.text', 'display.visualizations.charting.chart.nullValueMode', 'display.visualizations.mapHeight', 'display.visualizations.mapping.markerLayer.markerMaxSize', 'display.page.search.tab', 'display.statistics.wrap', 'dispatch.ttl', 'display.visualizations.charting.axisX.minimumNumber', 'display.visualizations.charting.chart', 'display.visualizations.charting.axisX.scale', 'display.visualizations.mapping.tileLayer.minZoom', 'display.visualizations.chartHeight', 'action.email', 'is_scheduled', 'dispatch.lookups', 'display.visualizations.charting.legend.placement', 'alert_condition', 'dispatch.reduce_freq', 'auto_summarize.max_summary_ratio', 'display.visualizations.mapping.tileLayer.url', 'request.ui_dispatch_app', 'display.events.maxLines', 'display.visualizations.charting.axisLabelsX.majorUnit', 'action.summary_index', 'display.page.search.timeline.scale', 'display.visualizations.singlevalue.beforeLabel', 'triggered_alert_count', 'display.visualizations.charting.chart.overlayFields', 'display.visualizations.charting.axisTitleY.text', 'alert_comparator', 'auto_summarize', 'display.statistics.rowNumbers', 'display.visualizations.charting.gaugeColors', 'display.visualizations.charting.chart.stackMode', 'search', 'display.visualizations.charting.chart.style', 'auto_summarize.cron_schedule', 'request.ui_dispatch_view', 'display.visualizations.charting.axisY.minimumNumber', 'display.visualizations.charting.axisX.maximumNumber', 'display.visualizations.charting.axisY2.enabled', 'display.events.list.wrap', 'action.script', 'display.visualizations.mapping.drilldown', 'display.visualizations.charting.chart.bubbleMinimumSize', 'action.populate_lookup', 'display.visualizations.charting.axisLabelsY.majorUnit', 'dispatch.earliest_time', 'display.visualizations.charting.axisLabelsY2.majorUnit', 'display.visualizations.charting.legend.labelStyle.overflowMode', 'alert.suppress.fields', 'dispatch.rt_backfill', 'display.visualizations.charting.chart.bubbleSizeBy', 'display.visualizations.charting.chart.rangeValues', 'displayview', 'action.rss', 'dispatch.index_earliest', 'alert.suppress', 'next_scheduled_time', 'display.visualizations.mapping.markerLayer.markerMinSize', 'dispatchAs', 'cron_schedule', 'dispatch.indexedRealtime', 'auto_summarize.suspend_period', 'run_on_startup', 'display.events.table.wrap', 'max_concurrent', 'auto_summarize.dispatch.time_format', 'display.visualizations.mapping.tileLayer.maxZoom', 'dispatch.buckets', 'auto_summarize.dispatch.earliest_time', 'auto_summarize.max_disabled_buckets', 'alert_type', 'display.visualizations.charting.axisLabelsX.majorLabelStyle.rotation', 'auto_summarize.dispatch.latest_time', 'display.visualizations.charting.axisY.scale', 'display.events.type', 'qualifiedSearch', 'action.email.sendresults', 'display.visualizations.type', 'display.page.search.mode', 'auto_summarize.max_time', 'alert_threshold', 'display.statistics.drilldown', 'display.visualizations.mapping.map.zoom', 'display.general.timeRangePicker.show', 'display.visualizations.charting.layout.splitSeries', 'display.events.rowNumbers', 'display.visualizations.singlevalue.afterLabel', 'display.visualizations.charting.axisY2.maximumNumber', 'action.email.to', 'dispatch.index_latest', 'action.email.inline', 'dispatch.spawn_process', 'description', 'display.page.search.timeline.format', 'display.visualizations.mapping.data.maxClusters', 'display.general.migratedFromViewState', 'alert.expires', 'display.visualizations.charting.drilldown', 'display.events.raw.drilldown', 'alert.track', 'display.visualizations.singlevalue.underLabel', 'display.page.search.showFields', 'dispatch.max_time', 'display.visualizations.charting.axisLabelsX.majorLabelStyle.overflowMode', 'dispatch.auto_pause', 'restart_on_searchpeer_add', 'action.email.reportServerEnabled', 'display.statistics.overlay', 'alert.severity', 'display.general.enablePreview']
    savedsearch = {}
    for field in keep_fields:
        savedsearch[field] = alert[field]

    return savedsearch

def create_alerts(config, entries):
    service = client.connect(
        host=config['destinationhostname'],
        port=config['port'],
        username=config['username'],
        password=config['password'],
        owner=config['username'],
        app='search')

    for alert in entries:
        print("Creating %s" % alert.name)
        savedsearch = gen_savedsearch_alert_param(alert.content)
        mysavedsearch = service.saved_searches.create(alert.name, savedsearch)
        print "Created: " + mysavedsearch.name

def print_usage():
    """docstring for print_usage"""
    print(
        "main.py -u <username> -p <password> -P <port> -f <filter> -D <destinationhostname> -S <sourcehostname>")


def process_args(argv):
    """docstring for process_args"""
    config = {
        'port': 8089
    }

    try:
        opts, args = getopt.getopt(argv, 'hu:p:P:f:S:D:', [
                                   'help', 'username=', 'password=', 'port=', 'filter=', 'sourcehostname=', 'destinationhostname='])
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
        elif opt in ('-S', '--sourcehostname'):
            config['sourcehostname'] = arg
        elif opt in ('-D', '--destinationhostname'):
            config['destinationhostname'] = arg
        elif opt in ('-f', '--filter'):
            config['filter'] = arg

    return config

def get_password():
    """docstring for get_password"""
    p = getpass.getpass(prompt='Please enter password? ')
    return p

def main(argv):
    """docstring for main"""

    config = process_args(argv)

    if 'password' not in config.keys():
        config['password'] = get_password()

    try:
        entries = get_alerts(config)
        result = filter_alerts(config['filter'], entries)
        create_alerts(config, result)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main(sys.argv[1:])
