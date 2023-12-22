import pprint 
import socket 
import sys

import pykka  

class Resolver(pykka.ThreadingActor):
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