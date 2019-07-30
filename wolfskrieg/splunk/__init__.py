from .splunkeventcollector import SplunkEventCollector
from .config import url, headers

EventCollector=SplunkEventCollector(config.url, config.headers)
