#!/bin/bash
if [ $# -lt 1 ]
then
	echo "$0 <job output dir> [TOR_PROXY_PORT] [TOR_CONTROL_PORT] [scrapy binary]"
	exit;
fi
bin=$4
tor=$3
priv=$2
if [ -z "$4" ]
then
	bin='scrapy'
fi
if [ -z "$3" ]
then
	tor='30001'
fi
if [ -z "$2" ]
then
        priv='30000'
fi
time TOR_PROXY_PORT=$priv TOR_CONTROL_PORT=$tor $bin crawl linkedin -s JOBDIR=$1 --output=$1/output.txt --loglevel=WARNING --logfile=scrapy.log -t bz2json
