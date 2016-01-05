#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
class IotTopo(Topo):
    def __init__(self, n=2, **opts):
		Topo.__init__(self, **opts)
		#make switchs
		self.G1 = self.addSwitch('G1')
		self.G2 = self.addSwitch('G2')
	#	self.G3 = self.addSwitch('G3')
	#	self.S1 = self.addSwitch('S1')
		self.S2 = self.addSwitch('S2')
		#make host
		self.H_1 = self.addHost('H1')
		self.H_2 = self.addHost('H2')
		#make link
		#self.addLink(self.Iot_1,self.H_1,0,0)
		#self.addLink(self.Iot_1,self.Iot_2,1,0)
		#self.addLink(self.Iot_2,self.H_2,1,0)
		#self.addLink(self.Iot_3,self.H_2,1,1)
		#self.addLink(self.Iot_3,self.H_1,0,1)
		
		#self.addLink(sw2, sw1, bw = 10, max_queue_size = 1000, use_htb = True)
		self.addLink(self.G1,self.H_1)
		self.addLink(self.G1,self.S2)
		self.addLink(self.S2,self.G2)
	#	self.addLink(self.G2,self.H_2)
	#	self.addLink(self.G1,self.G3)
	#	self.addLink(self.G3,self.G4)
		self.addLink(self.G2,self.H_2)
def IotTest():
        controllerInstance = RemoteController('Iot-Controller',ip='10.108.101.212',port=6633)
	#controllerInstance = RemoteController('Iot-Controller',ip='127.0.0.1',port=6633)
	topo = IotTopo(n=4)
	net = Mininet(topo,build=False,controller = RemoteController, host = CPULimitedHost, link = TCLink,ipBase='192.168.3.0/24')
	net.addController(controllerInstance)
	net.build()
	net.start()
	CLI(net)
	dumpNodeConnections(net.hosts)       
	#net.ping(net.hosts)    
	net.stop()       
if __name__ == '__main__':
	setLogLevel('info')
	IotTest()
