import argparse, sys, os.path, time, json
from kink_module.kink import Kink

username = None
password = None

types = ["performer", "p", 
		 "channel", "c",
		 "shoot", "s"]

def print_welcome():
	print("Kink")

def load_credentials(exec_dir):
	credentials_path = os.path.join(exec_dir, "credentials.json")
	if os.path.exists(credentials_path):
		with open(credentials_path) as f:
			credentials = json.loads(f.read())
			
			global username
			global password
			
			if username is None and "username" in credentials.keys():
				username = credentials["username"]
			if password is None and "password" in credentials.keys():
				password = credentials["password"]

def parse_arguments():
	parser = build_argparse()
	args = parser.parse_args()
	
	urls = []
	type = None
	
	if args.type in [types[0], types[1]]:
		type = "performer"
		for id in args.ids:
			urls.append(id)
	elif args.type in [types[2], types[3]]:
		type = "channel"
		for name in args.names:
			urls.append(name)
	elif args.type in [types[4], types[5]]:
		type = "shoot"
		for url in args.urls:
			urls.append(url)
	
	if username is None:
		un = args.un
	else:
		un = username
	if password is None:
		pw = args.pw
	else:
		pw = password
	
	# username, password, dir, process_limit, urls, type, quality, clip_quality, trailer, photos, clips, join
	return un, pw, args.dir, args.processes, urls, type, args.quality, args.clip_quality, args.trailer, args.photos, args.clips, args.join
	
def build_argparse():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-d", "--dir", dest="dir", default="", help="The directory to download to")
	parser.add_argument("-p", "--processes", type=int, dest="processes", default=4, help="The maximum number of processes to run while downloading")
	parser.add_argument("-t", "--type", dest="type", choices=types, help="The type that the ripper needs to aim for. 'p', 'performer', 'c', and 'channel' take a list of names, while 's' and 'shoot' takes a list of URLs")
	parser.add_argument("-n", "--name", dest="names", nargs=argparse.REMAINDER, help="The names to rip for channels")
	parser.add_argument("-i", "--ids", dest="ids", nargs=argparse.REMAINDER, help="The names to rip for performers")
	parser.add_argument("-u", "--url", dest="urls", nargs=argparse.REMAINDER, help="The URLs to rip for shoots")
	parser.add_argument("-q", "--quality", dest="quality", default="HD", help="Set the quality to download videos at; defaults to HD")
	parser.add_argument("-u", "--clipq", dest="clip_quality", default="", help="Set the quality/format to use when downloading clips instead of the final video")
	parser.add_argument("-r", "--trailer", dest="trailer", action="store_true", help="If included, the trailers will be downloaded when available")
	parser.add_argument("-h", "--photos", dest="photos", action="store_true", help="If included, photosets will be downloaded when available")
	parser.add_argument("-c", "--clips", dest="clips", action="store_true", help="If included, clips will be downloaded instead of the big video file")
	parser.add_argument("-j", "--join", dest="join", action="store_true", help="If included, clips will be joined to form a single video (has no effect if '-c' is not set")
	
	if username is None:
		parser.add_argument("-l", "--username", dest="un", default=None, help="The username to use when logging in")
	if password is None:
		parser.add_argument("-s", "--password", dest="pw", default=None, help="The password to use when logging in")
	
	return parser
	
def print_time_taken(start):
	end = time.time()

	duration = end - start
	
	seconds = duration % 60
	minutes = duration // 60
	hours = minutes // 60
	minutes = minutes % 60
	
	print("Time taken (hh:mm:ss): " + str(int(hours)).zfill(2) + ":" + str(int(minutes)).zfill(2) + ":" + str(int(seconds)).zfill(2))

if __name__ == "__main__":
	exec_dir = os.path.dirname(os.path.abspath(__file__))
	
	#args = parse_arguments()
	
	print_welcome()
	load_credentials(exec_dir)
	
	k = Kink(exec_dir, *[username, password, "", 0, ["sexandsubmission"], "channel", None, None, False, False, False, False])#args)
	k.startup()

	start = time.time()
	
	k.rip()
	#k.shutdown()
	
	print_time_taken(start)
