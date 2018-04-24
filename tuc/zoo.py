import time
from kazoo.client import KazooClient
import sys 
from os.path import dirname, abspath
import json

class Zooconf:
	__zkcon = None
	__test = ""
	__serviceConfig = None
	
	def __init__(self):
		sys.stderr.write("Fileservicepython start initialization at " + str(int(round(time.time() * 1000))))
		sys.stderr.flush()
		
		self.__initConfProperties()
		self.__zooConnect()
		self.__publishService()
        

	def __initConfProperties(self):
		sys.stderr.write(dirname(dirname(abspath(__file__))))
		sys.stderr.flush()
		self.__serviceConfig = dict()
		
		with open(dirname(dirname(abspath(__file__)))+"/config.properties", 'r') as f:
			for line in f:
				line = line.rstrip()

				if "=" not in line: 
					continue #skips blanks and comments w/o =
				if line.startswith("#"): 
					continue #skips comments which contain =
				k, v = line.split("=", 1)
				self.__serviceConfig[k] = v
			f.close() 
			
	def __zooConnect(self):
		sys.stderr.write("Start zooconnect")
		sys.stderr.flush()
		
		config = self.getServiceConfig();
		
		self.__zkcon = KazooClient(hosts=config["ZOOKEEPER_HOST"])
		self.__zkcon.start()
		digest_auth = "%s:%s" % (config["ZOOKEEPER_USER"], config["ZOOKEEPER_PASSWORD"])
		self.__zkcon.add_auth("digest", digest_auth)
		
		#ZooKeeper zk = new ZooKeeper(config.getProperty("ZOOKEEPER_HOST"), 3000, new Watcher() {
		#	@Override
		#	public void process(WatchedEvent we) {
		#		if (we.getState() == KeeperState.SyncConnected) {
		#			connectedSignal.countDown();
		#		}
		#	}
		#});
		#connectedSignal.await();
		#
		#zk.addAuthInfo("digest", new String(config.getProperty("ZOOKEEPER_USER")+":"+config.getProperty("ZOOKEEPER_PASSWORD")).getBytes()); 
		#
		#System.err.println("finished zooConnect");
		#
		#return zk;
	#}
	def __publishService(self):
		from kazoo.security import make_digest_acl
		config = self.getServiceConfig();
		acl = make_digest_acl(config["ZOOKEEPER_USER"], config["ZOOKEEPER_PASSWORD"], all=True)
		
	
		dataJsonDict = {}
		dataJsonDict['SERVERHOSTNAME'] = config["SERVERHOSTNAME"]
		dataJsonDict['SERVER_PORT'] = config["SERVER_PORT"]
		dataJsonDict['SERVER_SCHEME'] = config["SERVER_SCHEME"]
		dataJsonDict['HMACKEY'] = config["HMACKEY"]
		dataJsonDict['CONTEXT'] = config["CONTEXT"]
		
		self.__zkcon.create("/plh414/fileservices/"+config["ID"], json.JSONEncoder().encode(dataJsonDict).encode(), [acl], ephemeral=True)
		#instance.zk.create("/plh414/fileservices/"+instance.serviceConfig.getProperty("ID"), data.toString().getBytes("UTF-8"), Arrays.asList(acl), CreateMode.EPHEMERAL);	


	def getTest(self):
		return self.__test
	
	def getZooConnection(self):
		return self.__zkcon

	def getServiceConfig(self):
		return self.__serviceConfig

#imported only once per module
zk = Zooconf()