#This agent creates a server, waits for incoming HTTP requests and channels them to the proper agent. In this
#case the values received are the value of the light sensed through the photoresistor in the Arduino and a command 
#from the user stating the activity he wants to perform. 

import time, httplib, urllib, os, sys, json, unittest, thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

#global variables:
#ip_address="192.168.0.100" #Comment/uncomment depending on the network the system is running -> Home
#ip_address='10.20.218.197'	#Comment/uncomment depending on the network the syste is running -> ITESM
ip_address="127.0.0.1"		#Comment/uncomment depending on the network the system is running -> Local
sys.path.append('../..')
import spade

light_sensed=-1
luz_0=1000
luz_100=1100
luz_200=1200
luz_300=1300
luz_400=1400
luz_500=1500
luz_600=1600
luz_700=1700
luz_800=1800
luz_900=1900
luz_1000=2000
activity_change=0
activity=""


class RecAgent(spade.Agent.Agent):

	def _setup(self):
		b = self.RecBehav()
		self.addBehaviour(b, None)
		print "Receiver just started"

	class RecBehav(spade.Behaviour.Behaviour):

		def _process(self):
			global light_sensed, activity, activity_change
			#try:
			 #   mode=int(raw_input('Input: '))
			#except ValueError:
			 #   print "Not a number"
			if activity_change: #*****Remember to change this during implementation to activity_change instead of mode.
				#If the activity changed, send the amount of light received from the sensors.
				print 'The amount of light is: {0}'.format(light_sensed)
				msg = spade.ACLMessage.ACLMessage()
				msg.setPerformative("inform")
				msg.setOntology("light")
				msg.addReceiver(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
				msg.setContent(light_sensed)
				self.myAgent.send(msg)
				print "Rec has sent a message to inform the ligth sensed to the control agent:"
				#print str(msg)

				#Also send the activity requested by the user.
				print 'The activity requested is: {0}'.format(activity)
				msg = spade.ACLMessage.ACLMessage()
				msg.setPerformative("inform")
				msg.setOntology("activity")
				msg.addReceiver(spade.AID.aid("control_agent@"+ip_address,["xmpp://control_agent@"+ip_address]))
				msg.setContent(activity)
				self.myAgent.send(msg)
				print "Rec has sent a message to inform the activity requested to the control agent:"
				#print str(msg)
				activity_change=0
			

#HTTP server!.....................................................................................		

class NinjaHttpRequestHandler(BaseHTTPRequestHandler):
	
# 	#handle POST command
	def do_POST(self):
		global light_sensed, activity_change, activity
		rf_guid='1313BB000464_0_0_11' #ID of the RF sensor

		rootdir = '/' #file location
		try:
				print('A POST request has been made to the receiver_agent...')
				content_len = int(self.headers.getheader('content-length', 0))
				post_body = self.rfile.read(content_len)
				print post_body
				try:
					decoded_body = json.loads(post_body)
					# pretty printing of json-formatted string
					print json.dumps(decoded_body, sort_keys=True, indent=4)
					if decoded_body['activity'] == 'read':
						print 'I want to read.'
						activity_change=1
						activity=decoded_body['activity']
					elif decoded_body['activity'] == 'tv':
						print 'I think I will watch TV.'
						activity_change=1
						activity=decoded_body['activity']
					elif decoded_body['activity'] == 'eat':
						print 'I am starving, I will grab a bite to eat.'
						activity_change=1
						activity=decoded_body['activity']
					elif decoded_body['activity'] == 'sleep':
						print 'I am so sleepy, I will call it a day.'
						activity_change=1
						activity=decoded_body['activity']

					if decoded_body['GUID'] == rf_guid:
						if int(decoded_body['DA'],2) == luz_0:
							light_sensed=0
						elif int(decoded_body['DA'],2) == luz_100:
							light_sensed=100
						elif int(decoded_body['DA'],2) == luz_200:
							light_sensed=200
						elif int(decoded_body['DA'],2) == luz_300:
							light_sensed=300
						elif int(decoded_body['DA'],2) == luz_400:
							light_sensed=400
						elif int(decoded_body['DA'],2) == luz_500:
							light_sensed=500
						elif int(decoded_body['DA'],2) == luz_600:
							light_sensed=600
						elif int(decoded_body['DA'],2) == luz_700:
							light_sensed=700
						elif int(decoded_body['DA'],2) == luz_800:
							light_sensed=800
						elif int(decoded_body['DA'],2) == luz_900:
							light_sensed=900
						elif int(decoded_body['DA'],2) == luz_1000:
							light_sensed=1000

				except (ValueError, KeyError, TypeError):
					print "JSON format error"
					
				#send code 200 response
				self.send_response(200)
				return
			
		except IOError:
			self.send_error(500, 'server error p')		
	
	#handle GET command
	def do_GET(self):
		rootdir = '/' #file location
		print('A GETrequest has been made to the receiver_agent...')
		try:
			if self.path.endswith('.html'):
				f = open(rootdir + self.path) #open requested file

				#send code 200 response
				self.send_response(200)

				#send header first
				self.send_header('Content-type','text-html')
				self.end_headers()

				#send file content to client
				self.wfile.write(f.read())
				f.close()
				return
			
		except IOError:
			self.send_error(404, 'file not found')


def run():
	print('http server is starting...')

	#ip and port of servr
	#by default http server port is 80
	server_address = (ip_address, 8008)
	httpd = HTTPServer(server_address, NinjaHttpRequestHandler)
	print('http server is running...')
	try: 
		httpd.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)


#.....................................................................    	
a = RecAgent("rec_agent@"+ip_address, "secret")
thread.start_new_thread(run, ())
a.start()
alive = True
while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
a.stop()
sys.exit(0)

