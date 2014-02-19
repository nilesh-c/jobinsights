from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler, ScrapyAgent
import re

from time import time
from cStringIO import StringIO
from urlparse import urldefrag

from zope.interface import implements
from twisted.internet import defer, reactor, protocol
from twisted.web.http_headers import Headers as TxHeaders
from twisted.web.iweb import IBodyProducer
from twisted.internet.error import TimeoutError
from twisted.web.http import PotentialDataLoss
from scrapy.xlib.tx import Agent, ProxyAgent, ResponseDone, \
    HTTPConnectionPool, TCP4ClientEndpoint

from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.core.downloader.webclient import _parse
from scrapy.utils.misc import load_object

from txsocksx.http import SOCKS5Agent

class TorProxyDownloadHandler(HTTP11DownloadHandler):

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        agent = ScrapyTorAgent(contextFactory=self._contextFactory, pool=self._pool)
        return agent.download_request(request)


class ScrapyTorAgent(ScrapyAgent):
    def _get_agent(self, request, timeout):
        bindaddress = request.meta.get('bindaddress') or self._bindAddress
        proxy = request.meta.get('proxy')
        if proxy:
            _, _, proxyHost, proxyPort, proxyParams = _parse(proxy)
            scheme = _parse(request.url)[0]
            omitConnectTunnel = proxyParams.find('noconnect') >= 0
            if  scheme == 'https' and not omitConnectTunnel:
                proxyConf = (proxyHost, proxyPort,
                             request.headers.get('Proxy-Authorization', None))
                return self._TunnelingAgent(reactor, proxyConf,
                    contextFactory=self._contextFactory, connectTimeout=timeout,
                    bindAddress=bindaddress, pool=self._pool)
            else:
                _, _, host, port, proxyParams = _parse(request.url)
                proxyEndpoint = TCP4ClientEndpoint(reactor, proxyHost, proxyPort,
                    timeout=timeout, bindAddress=bindaddress)
                agent = SOCKS5Agent(reactor, proxyEndpoint=proxyEndpoint)
                return agent

        return self._Agent(reactor, contextFactory=self._contextFactory,
            connectTimeout=timeout, bindAddress=bindaddress, pool=self._pool)
