import time, sys
from time import gmtime
import httplib, urllib

ip_address='10.12.19.67'
#ip_address='127.0.0.1'
#ip_address='10.20.218.197'
cost='0'
weather='overcast'
#local_hour=time.localtime().tm_hour
sun_percentage=[0,0,0,0,0,0,0.2305,0.6537,0.8328,0.9215,0.9689,0.9927,1,0.9927,0.9689,0.9215,0.8328,0.6537,0.2305,0,0,0,0,0]
local_hour=6
alt_hour=sun_percentage[local_hour]
if weather=='daylight':
	max_light=10750*0.45*alt_hour
elif weather=='overcast':
	max_light=1075*0.45*alt_hour
elif weather=='dark':
	max_light=107.5*0.45*alt_hour
l_amount=''+str(int(max_light))
print l_amount
sys.path.append('../..')
import spade
in_use=False
name="blinds_agent"

class MyAgent(spade.Agent.Agent):
	def _setup(self):

		template = spade.Behaviour.ACLTemplate()
		template.setSender(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
		template.setOntology("auction")
		t = spade.Behaviour.MessageTemplate(template)
		self.addBehaviour(self.RecBehav(),t)
		print "Receiver Light template behaviour just started!"

	class RecBehav(spade.Behaviour.EventBehaviour):

		def _process(self):
			global in_use
			msg = self._receive(block=False,timeout=10)
			print name+" has received a CFP:"
			try:
			    m_content=int(msg.getContent())
			except ValueError:
			    print "Not a number"
			light_sensed=m_content
			if not in_use:
				msg = spade.ACLMessage.ACLMessage()
				msg.setPerformative("propose")
				msg.setOntology("auction")
				msg.addReceiver(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
				msg.setContent(cost+" "+str(int(int(l_amount)*0.25))+" "+name+"0")
				self.myAgent.send(msg)
				msg.setContent(cost+" "+str(int(int(l_amount)*0.50))+" "+name+"1")
				self.myAgent.send(msg)
				msg.setContent(cost+" "+str(int(int(l_amount)*0.75))+" "+name+"2")
				self.myAgent.send(msg)
				msg.setContent(cost+" "+str(int(int(l_amount)*1))+" "+name+"3")
				self.myAgent.send(msg)
				print name+" has sent a proposal to the control_agent:"
			

a = MyAgent(name+"@"+ip_address, "secret")
a.start()
alive = True
while alive:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		alive=False
a.stop()
sys.exit(0)	
		