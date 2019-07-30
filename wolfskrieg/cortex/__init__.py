from .connector import CortexConnector
from .config import url, headers, post_header
CortexConnection = CortexConnector(url, headers, post_header)
