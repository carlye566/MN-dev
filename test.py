#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class IotTopo(Topo):
    def __init__(self, **opts):
	Topo.__init__(self, **opts)
		#make switchs
	self.Iot_1 = self.addSwitch('Iot1')
	self.Iot_2 = self.addSwitch('IoT2')
	self.Iot_3 = self.addSwitch('IoT3')
	self.Iot_left = self.addSwitch('Iot4')
	self.Iot_right = self.addSwitch('Iot5')
	#make host
	self.H_1 = self.addHost('H1')
	self.H_2 = self.addHost('H2')
		#make link
		#self.addLink(self.Iot_1,self.H_1,0,0)
		#self.addLink(self.Iot_1,self.Iot_2,1,0)
		#self.addLink(self.Iot_2,self.H_2,1,0)
		#self.addLink(self.Iot_3,self.H_2,1,1)
		#self.addLink(self.Iot_3,self.H_1,0,1)
		
	self.addLink(self.Iot_left,self.H_1)
	self.addLink(self.Iot_1,self.Iot_left)
	self.addLink(self.Iot_1,self.Iot_2)
	self.addLink(self.Iot_2,self.Iot_right)
	self.addLink(self.Iot_3,self.Iot_right)
	self.addLink(self.Iot_3,self.Iot_left)
	self.addLink(self.Iot_right,self.H_2)
def IotTest():
    controllerInstance = RemoteController('Iot-Controller',ip='10.108.102.225',port=6633)
    topo = IotTopo()
    net = Mininet(topo,build=False,ipBase='192.168.3.0/24')
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
