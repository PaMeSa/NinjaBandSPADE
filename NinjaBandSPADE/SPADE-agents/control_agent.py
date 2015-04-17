#The control agent acts as the auctioneer, calling for proposals and gathering them from the agents. Then
#a function builds the packages and chooses the best one according to the objective function defined.

import time, os, sys, unittest, json, math, threading, requests
#,time, httplib, urllib

#global variables:
#ip_address='192.168.0.100' #Comment/uncomment depending on the network the system is running -> Home
ip_address='10.12.19.67'	#Comment/uncomment depending on the network the syste is running -> ITESM
#ip_address='192.168.0.116'		#Comment/uncomment depending on the network the system is running -> Local
sys.path.append('../..')
import spade

light_sensed=-1
activity=""
cfp_timer=-1
num_proposals0=0
num_proposals1=0
num_proposals2=0
num_proposals3=0
costs0=[]
costs1=[]
costs2=[]
costs3=[]
luminance0=[]
luminance1=[]
luminance2=[]
luminance3=[]
senders0=[]
senders1=[]
senders2=[]
senders3=[]
lock_thread=threading.Lock()
cost_coef=0.99
light_coef=0.01

#Define a behaviour to receive the amount of light sensed.
class ControlAgent(spade.Agent.Agent):

	def _setup(self):
		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("rec_agent@"+ip_address,["xmpp://rec_agent@"+ip_address]))
		template.setOntology("light")
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.LightBehav(),t)

		#Define a second template for the activity

		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("rec_agent@"+ip_address,["xmpp://rec_agent@"+ip_address]))
		template.setOntology("activity")
		template.setPerformative("inform")
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.ActivBehav(),t)

		#Define a third template for the proposals

		template = spade.Behaviour.ACLTemplate()
		template.setOntology("auction")
		template.setPerformative("propose")
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.PropBehav(),t)

		#Add the behaviour for the timer

		self.addBehaviour(self.TimerBehav(0.1),None)

		#Define a fourth template for the bids creation

		template = spade.Behaviour.ACLTemplate()
		template.setOntology("auction")
		template.setSender(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
		template.setPerformative("request")
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.CreateBidsBehav(),t)

		print "All the behaviours have been configured and added."

	class LightBehav(spade.Behaviour.EventBehaviour):

		def _process(self):
			global light_sensed
			msg = self._receive(block=False,timeout=10)
			print "Control Agent has received a light message:"
			try:
				m_content=int(msg.getContent())
			except ValueError:
				print "Not a number"
			light_sensed=m_content

	#Define another behaviour to receive the activity from the user.

	class ActivBehav(spade.Behaviour.EventBehaviour):

		def _process(self):
			print "Control Agent has received an activity message:"
			global activity, light_sensed
			msg = self._receive(block=False,timeout=10)
			m_content=msg.getContent()
			activity=m_content
			#Now send a cfp to the agents that are idle and can provide illumination to the room
			msg2 = spade.ACLMessage.ACLMessage()
			msg2.setPerformative("cfp")
			msg2.setOntology("auction")
			msg2.addReceiver(spade.AID.aid("light_bulb_agent@"+ip_address,["xmpp://light_bulb_agent@"+ip_address]))
			msg2.addReceiver(spade.AID.aid("night_stand_agent@"+ip_address,["xmpp://night_stand_agent@"+ip_address]))
			msg2.addReceiver(spade.AID.aid("lamp_agent@"+ip_address,["xmpp://lamp_agent@"+ip_address]))
			msg2.addReceiver(spade.AID.aid("blinds_agent@"+ip_address,["xmpp://blinds_agent@"+ip_address]))
			msg2.setContent(light_sensed)
			self.myAgent.send(msg2)
			print "control_agent has made a CFP:"

	#Define another behaviour to receive proposals from the agents

	class PropBehav(spade.Behaviour.EventBehaviour):

		def _process(self):
			global cfp_timer, num_proposals0,num_proposals1,num_proposals2,num_proposals3
			global costs0, costs1, costs2, costs3, luminance0, luminance1, luminance2, luminance3
			global senders0, senders1, senders2, senders3
			cfp_timer=10
			msg = self._receive(block=False,timeout=10)
			print "Control Agent has received a proposal from: "
			cost, l_amount, sender = msg.getContent().split(" ",2)
			try:
				cost=int(cost)
				l_amount=int(l_amount)
				sender=str(sender)
			except ValueError:
				print "Not a number"
			lock_thread.acquire()
			if sender=='blinds_agent0':
				num_proposals0+=1
				print "Cost of this proposal is: {0}".format(cost)
				costs0.append(cost)
				print "The amount of light provided in this proposal is: {0}".format(l_amount)
				luminance0.append(l_amount)
				print "The sender of this proposal is: "+sender
				senders0.append(sender)
			elif sender=='blinds_agent1':
				num_proposals1+=1
				print "Cost of this proposal is: {0}".format(cost)
				costs1.append(cost)
				print "The amount of light provided in this proposal is: {0}".format(l_amount)
				luminance1.append(l_amount)
				print "The sender of this proposal is: "+sender
				senders1.append(sender)
			elif sender=='blinds_agent2':
				num_proposals2+=1
				print "Cost of this proposal is: {0}".format(cost)
				costs2.append(cost)
				print "The amount of light provided in this proposal is: {0}".format(l_amount)
				luminance2.append(l_amount)
				print "The sender of this proposal is: "+sender
				senders2.append(sender)
			elif sender=='blinds_agent3':
				num_proposals3+=1
				print "Cost of this proposal is: {0}".format(cost)
				costs3.append(cost)
				print "The amount of light provided in this proposal is: {0}".format(l_amount)
				luminance3.append(l_amount)
				print "The sender of this proposal is: "+sender
				senders3.append(sender)
			else:
				num_proposals0+=1
				num_proposals1+=1
				num_proposals2+=1
				num_proposals3+=1
				print "Cost of this proposal is: {0}".format(cost)
				costs0.append(cost)
				costs1.append(cost)
				costs2.append(cost)
				costs3.append(cost)
				print "The amount of light provided in this proposal is: {0}".format(l_amount)
				luminance0.append(l_amount)
				luminance1.append(l_amount)
				luminance2.append(l_amount)
				luminance3.append(l_amount)
				print "The sender of this proposal is: "+sender
				senders0.append(sender)
				senders1.append(sender)
				senders2.append(sender)
				senders3.append(sender)
			lock_thread.release()

	#Define a behaviour to create a timer that waits until the call for proposals is over

	class TimerBehav(spade.Behaviour.PeriodicBehaviour):

		def _onTick(self):
			global cfp_timer
			if cfp_timer>0:
				cfp_timer-=1
			if cfp_timer == 0:
				cfp_timer=-1
				print "The call for proposals is finished"
				msg = spade.ACLMessage.ACLMessage()
				msg.setPerformative("request")
				msg.setOntology("auction")
				msg.addReceiver(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
				self.myAgent.send(msg)

	class CreateBidsBehav(spade.Behaviour.EventBehaviour):

		def _process(self):
			print "Starting to create bids"
			global num_proposals0,num_proposals1,num_proposals2,num_proposals3
			global costs0, costs1, costs2, costs3, luminance0, luminance1, luminance2, luminance3
			global senders0, senders1, senders2, senders3
			msg = self._receive(block=False,timeout=10)
			bid0=calc_auction(senders0,luminance0,costs0,num_proposals0)
			bid1=calc_auction(senders1,luminance1,costs1,num_proposals1)
			bid2=calc_auction(senders2,luminance2,costs2,num_proposals2)
			bid3=calc_auction(senders3,luminance3,costs3,num_proposals3)
			best_bid=min(bid0['minim'],bid1['minim'],bid2['minim'],bid3['minim'])
			if bid0['minim']==best_bid:
				print "The min cost is = "+str(bid0['minim'])
				print bid0['min_cluster']
				print senders0
				send_post_reqs(senders0,bid0['min_cluster'])
			if bid1['minim']==best_bid:
				print "The min cost is = "+str(bid1['minim'])
				print bid1['min_cluster']
				print senders1
				send_post_reqs(senders1,bid1['min_cluster'])
			if bid2['minim']==best_bid:
				print "The min cost is = "+str(bid2['minim'])
				print bid2['min_cluster']
				print senders2
				send_post_reqs(senders2,bid2['min_cluster'])
			if bid3['minim']==best_bid:
				print "The min cost is = "+str(bid3['minim'])
				print bid3['min_cluster']
				print senders3
				send_post_reqs(senders3,bid3['min_cluster'])
			num_proposals0=0
			num_proposals1=0
			num_proposals2=0
			num_proposals3=0
			del costs0[:]
			del luminance0[:]
			del senders0[:]
			del costs1[:]
			del luminance1[:]
			del senders1[:]
			del costs2[:]
			del luminance2[:]
			del senders2[:]
			del costs3[:]
			del luminance3[:]
			del senders3[:]
			print "Is it empty?"
			print senders3
			

def calc_auction(senders,luminance,costs,num_proposals):
	global cost_coef, light_coef, activity
	minim=10000000
	min_cluster=[]
	cluster=[]
	sum_cost=0
	sum_lum=0
	print "Creating bundles"
	limit=math.pow(2,num_proposals)
	for i in range (0,int(limit)):
		if i>0:
			x=math.floor(math.log(i,2)+1)
		else:
			x=1
		k=i
		for j in range (0,int(x)):
			if k & 1 == 1:
				sum_cost+=costs[j]
				sum_lum+=luminance[j]
				cluster.append(j)
			k=k>>1
		if activity=="read":
			l_required=500
		elif activity == "tv":
			l_required=150
		elif activity == "sleep":
			l_required=0
		elif activity == "eat":
			l_required=250
		else:
			print "The activity is not recognized!"
		bid_value=cost_coef*sum_cost+light_coef*math.pow((sum_lum-l_required),2)
		if bid_value < minim:
			minim=bid_value
			min_cluster=cluster[:]
		sum_cost=0
		sum_lum=0
		del cluster[:]
	return {'minim':minim,'min_cluster':min_cluster}

def send_post_reqs(senders,min_cluster):
	url="http://ninjamultiagents.herokuapp.com"
	#make sure everything's OFF
	r=requests.post(url+"/turn_off_all")
	for y in min_cluster:
		if senders[y]=="light_bulb_agent":
			r=requests.post(url+"/turn_onL0")
		elif senders[y]=="lamp_agent":
			r=requests.post(url+"/turn_onL1")
		elif senders[y]=="night_stand_agent":
			r=requests.post(url+"/turn_onL2")
		elif senders[y]=="blinds_agent0":
			r=requests.post(url+"/turn_onL3_0")
		elif senders[y]=="blinds_agent1":
			r=requests.post(url+"/turn_onL3_1")
		elif senders[y]=="blinds_agent2":
			r=requests.post(url+"/turn_onL3_2")
		elif senders[y]=="blinds_agent3":
			r=requests.post(url+"/turn_onL3_3")
		else:
			print "Sorry but I don't know which light to turn ON"


a = ControlAgent("control_agent@"+ip_address, "secret")
a.start()
alive = True
while alive:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		alive=False
a.stop()
sys.exit(0)		