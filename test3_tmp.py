#FatTreeTopo.py 

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI 
from mininet.node import RemoteController

class MyTopo(Topo):
    "Simple Data Center Topology"

    "l1:core ovs, 12:aggregation ovs, 13:edge ovs"
    def __init__(self):
	#Initialize topology and default options
	Topo.__init__(self)
	
	#Change L1's value to generate difference topology
	L1 = 2
	L2 = L1 * 2
	L3 = L2 * 2
	L4 = L3 * 2
	c = []
	a1 = []
	a2 = []
	e = []
	
	#add core ovs
	for i in range(L1):
	    sw = self.addSwitch('c{}'.format(i + 1))
	    c.append(sw)

	#add aggregation1 ovs
	for i in range(L2):
	    sw = self.addSwitch('a1{}'.format(L1 + i + 1))
	    a1.append(sw)	    

	#add aggregation2 ovs
	for i in range(L3):
	    sw = self.addSwitch('a2{}'.format(L1 + L2 + i + 1))
	    a2.append(sw)	    

	#add edge ovs
	for i in range(L4):
	    sw = self.addSwitch('e{}'.format(L1 + L2 + L3 + i + 1))
	    e.append(sw)

	#add links between core and aggregation ovs
	for i in range(L1):
	    sw1 = c[i]
	    for sw2 in a1[(i/2)::(L1/2)]:
		#self.addLink(sw2, sw1, bw = 10, delay = '5ms', loss = 10, max_queue_size = 1000, use_htb = True)
		self.addLink(sw2, sw1)

	#add links between aggregation1 and aggregation2 ovs
	for i in range(0, L2, 2):
	    for sw1 in a1[i:(i + 2)]:
		for sw2 in a2[(i * 2):(i * 2 + 2)]:
		    #self.addLink(sw2, sw1, bw = 10, delay = '5ms', loss = 10, max_queue_size = 1000, use_htb = True)
		    self.addLink(sw2, sw1)

	#add links between aggregation2 and edge ovs
	for i in range(0, L3, 2):
	    for sw1 in a2[i:(i + 2)]:
		for sw2 in e[(i * 2):(i * 2 + 2)]:
		    #self.addLink(sw2, sw1, bw = 10, delay = '5ms', loss = 10, max_queue_size = 1000, use_htb = True)
		    self.addLink(sw2, sw1)

	#add hosts and its links with edge ovs
	count = 1
	for sw1 in e:
	    for i in range(2):
		host = self.addHost('h{}'.format(count))
		self.addLink(sw1,host)
		count += 1

topos = {'mytopo':(lambda:MyTopo())}

def simpleTest():
    "Create and test a simple network"
    topo = MyTopo()
    net = Mininet(topo, controller = RemoteController, host = CPULimitedHost, link = TCLink)
    net.addController('c0', controller = RemoteController, ip = '10.108.100.254', port=6633)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 with h2, h3, h5"
    h1, h2 = net.get('h1', 'h2')
    net.iperf((h1, h2))
    h1, h3 = net.get('h1', 'h3')
    net.iperf((h1, h3))
    h1, h5 = net.get('h1', 'h5')
    net.iperf((h1, h5))
    net.stop()

def IotTest():
        controllerInstance = RemoteController('Iot-Controller',ip='10.108.100.254',port=6633)
        #controllerInstance = RemoteController('Iot-Controller',ip='127.0.0.1',port=6633)
        topo = MyTopo()
        net = Mininet(topo,build=False,ipBase='192.168.3.0/24')
        net.addController(controllerInstance)
        net.build()
        net.start()
        CLI(net)
        dumpNodeConnections(net.hosts)    
        #net.ping(net.hosts)    
        net.stop() 

if __name__ == '__main__':
    #Tell mininet to print useful information
    setLogLevel('info')
    #simpleTest()
    IotTest()





