#import modules
import socket
import struct

servers = [] #temp same servers


def host2entry(host):
  entry = bytearray()
  hostport = host.split(":")
  octets = [int(oct) for oct in hostport[0].split(".")]
  entry.extend(struct.pack("BBBB", octets[0], octets[1], octets[2], octets[3]))
  entry.extend(struct.pack("!h", int(hostport[1])))
  return entry

	
def sendServerList(sock, ip , port):
  reply = b"\xFF\xFF\xFF\xFFgetserversResponse\\"
  entrydelimiter = b"\\"
  lastp = b"\EOT"
  entries = bytearray()
  for server in servers:
    entries.extend(host2entry(server)+entrydelimiter)
  sock.sendto(reply + entries + lastp, (str(ip), int(port)))
  
  
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', 20510))

while True:
  req, srcaddr = sock.recvfrom(4096)
  print(req)
  srcaddr = str(srcaddr)
  srcaddr = srcaddr.replace("\'", "")
  srcaddr = srcaddr.replace("(", "")
  srcaddr = srcaddr.replace(")", "")
  srcaddr = srcaddr.replace(" ", "")
  srcaddr = srcaddr.split(",")
  reqpart = (req.decode('latin-1'))[4:].split()
  serverip = f"{srcaddr[0]}:{srcaddr[1]}"
  if(reqpart[0] == "getservers"): #respond get servers request
    print(f"Get Servers Request From : {serverip}")
    sendServerList(sock, srcaddr[0],srcaddr[1])
  if(reqpart[0] == "heartbeat"):
    if(reqpart[1] == "COD-1"): #detect CoD 1 server heartbeat
      print(f"Heartbeat From : {serverip}")
      if serverip not in servers:
        servers.append(serverip)
    if(reqpart[1] == "flatline"):
        servers.remove(serverip)
