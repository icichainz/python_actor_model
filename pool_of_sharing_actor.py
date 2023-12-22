import pprint 
import socket 
import sys

import pykka  

""" 
 Resolve a bunch of IP addresses using a pool of resolvers actors.
 
 Either run without arguments:
    ./filename.py 
    
 Or specify pool size and IPs to resolve:
   ./filename.py 3 193.35.52.{1,2,3,4,5,6,7,8,9}
"""

class Resolver(pykka.ThreadingActor):
    """ The field allow the resolvation of ips address"""
    def resolve(self,ip):
        try:
            info = socket.gethostbyaddr(ip)
            print(f"Finished resolvinf {ip}")
            return info[0]
        except Exception :
            print(f"failed resolving {ip}")
            return None 

def run(pool_size ,*ips):   
    # start resolvers
    resolvers = [Resolver.start().proxy() for _ in range(pool_size)]
    
    # Distribute work by mapping IPs to resolvers (not blocking)
    hosts = []
    for i,ip in enumerate(ips):
        hosts.append(resolvers[i % len(resolvers)].resolve(ip))
    
    # gather results (blocking)
    ip_to_host = zip(ips,pykka.get_all(hosts))
    pprint.pprint(list(ip_to_host))
    
    # clean up
    pykka.ActorRegistry.stop_all()

if __name__ ==  "__main__":
    if len(sys.argv[1:]) >= 2 :
        run(int(sys.argv[1]),*sys.argv[2:])
    else:
        ips = [f"193.35.52.{i}" for i in range(1,50)]
        run(10,*ips)