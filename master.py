#modules import
from socket import *

#bind port
master = socket(AF_INET, SOCK_DGRAM)
master.bind(('', 20510))


