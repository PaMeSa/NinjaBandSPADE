import time, sys
import httplib, urllib

#ip_address="192.168.0.100"
#ip_address='10.20.218.197'
ip_address='10.12.19.67'
cost='60'
l_amount='300'
sys.path.append('../..')
import spade
in_use=False
name="light_bulb_agent"

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
				msg.setContent(cost+" "+l_amount+" "+name)
				self.myAgent.send(msg)
				print "light_bulb_agent has sent a proposal to the control_agent:"
			

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
		