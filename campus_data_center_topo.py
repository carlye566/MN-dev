#simulate the network topology of BUPT datacenter campus.

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class MyTopo(Topo):
	"simulate BUPT datacenter campus network topology"

	"l1:core ovs, l2:aggregation ovs, l3:edge ovs"
	def __init__(self):
		#Initialize topology and default options
		Topo.__init__(self)

		#setup every layer's switch number
		L1 = 1
		L2 = 3
		L3_study = 3
		L3_service = 1
		L3_dorm = 3
		L3 = L3_study + L3_service + L3_dorm
		soft_num = 4
		soft_count = 1
		core = []
		aggregation = []
		edge = []
		#soft_name = ['s1', 's2', 's3', 's4']
		soft = []

		#add core ovs
		for i in range(L1):
			core_sw = self.addSwitch('c{}'.format(i+1))
			#print "core: " + core_sw
			soft_sw = self.addSwitch("s{}".format(soft_count))
			soft_count = soft_count + 1
			core.append(core_sw)
			soft.append(soft_sw)
		'''
		for sw in soft_name:
			soft_sw = self.addSwitch(sw)
			soft.append(soft_sw)
		'''
		#add aggregation ovs
		for i in range(L2):
			aggre_sw = self.addSwitch("a{}".format(i+1+L1))
			soft_sw = self.addSwitch("s{}".format(soft_count))			
			soft_count += 1
			aggregation.append(aggre_sw)
			soft.append(soft_sw)

		#add edge ovs: the studying buildings part
		for i in range(L3_study):
			edge_sw = self.addSwitch("e_st{}".format(L1+L2+i+1))
			edge.append(edge_sw)
		#add edge ovs: the service part
		for i in range(L3_service):
			edge_sw = self.addSwitch("e_se{}".format(L1+L2+L3_study+i+1))
			edge.append(edge_sw)
		#add edge ovs: the dorm building part
		for i in range(L3_dorm):
			edge_sw = self.addSwitch("e_d{}".format(L1+L2+L3_service+L3_study+i+1))
			edge.append(edge_sw)

		#add links between core and aggregation ovs
		soft_count = 0
		for i in range(L1):
			core_sw = core[i]
			soft_sw = soft[soft_count]
			print "core_sw: " + core_sw
			print "soft_sw: " + soft_sw
			self.addLink(soft_sw, core_sw)
			j = 0
			for j in range(L2):
				aggre_sw = aggregation[j]
				self.addLink(core_sw, aggre_sw)
				self.addLink(soft_sw, aggre_sw)
			soft_count += 1

		#add links between aggregation and edge ovs
		for i in range(L2):
			aggre_sw = aggregation[i]
			soft_sw = soft[soft_count]
			soft_count += 1
			self.addLink(aggre_sw, soft_sw)
			#edge and aggregation ovs which is in the study building part
			if i == 0:
				for edge_sw in edge[0:L3_study]:
					self.addLink(edge_sw, aggre_sw)
					self.addLink(edge_sw, soft_sw)
			#edge and aggregation ovs which is in the service server part
			elif i == 1:
				for edge_sw in edge[L3_study:(L3_study+L3_service)]:
					self.addLink(edge_sw, aggre_sw)
					self.addLink(edge_sw, soft_sw)
			#edge and aggregation ovs which is in the dorm building part
			else:
				for edge_sw in edge[(L3_service+L3_study):L3]:
					self.addLink(edge_sw, aggre_sw)
					self.addLink(edge_sw, soft_sw)

		#add hosts and its links with edge ovs
		host_coefficient = 1
		host_number = L3 * host_coefficient
		study_host_number = L3_study * host_coefficient
		service_host_number = L3_service * host_coefficient
		dorm_host_number = L3_dorm * host_coefficient
		host_count = 0
		for edge_sw in edge:
			host_count += 1
			for i in range(host_coefficient):
				if host_count <= study_host_number:
					host = self.addHost("st_h{}".format(host_count))
					self.addLink(host, edge_sw)
					#print "the host name in study: " + host
				elif host_count > study_host_number and host_count <= (study_host_number+service_host_number):
					host = self.addHost("se_h{}".format(host_count))
					self.addLink(host, edge_sw)
					#print "the host name in service: " + host
				else:
					#print "hello"
					host = self.addHost("d_h{}".format(host_count))
					#print "the host name in dorm: " + host
				if i < (host_coefficient-1):
					host_count += 1
				self.addLink(host, edge_sw)
		
topos = {'mytopo':(lambda:MyTopo())}