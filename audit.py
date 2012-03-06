import argparse
import json
import requests
import link
import sys

def extract_users(userlist, json_blob):
	for object in json_blob:
		for field, value in object.iteritems():
			if field == 'author':
				if value == None:
					hash = object['sha']
					if not hash in userlist['suspicious']:
						userlist['suspicious'].append(hash)
				else:
					id = value['id'];
					if id in userlist['authors']:
						userobj = userlist['authors'][id]
					else:
						userobj = []
						userlist['authors'][id] = userobj
					username = value['login']
					if not username in userobj:
						userobj.append(username)
			if field == 'committer':
				if value == None:
					hash = object['sha']
					if not hash in userlist['suspicious']:
						userlist['suspicious'].append(hash)
				else:
					id = value['id'];
					if id in userlist['committers']:
						userobj = userlist['committers'][id]
					else:
						userobj = []
						userlist['committers'][id] = userobj
					username = value['login']
					if not username in userobj:
						userobj.append(username)
			if field =='commit':
				#extract committer
				email = value['author']['email']
				name = value['author']['name']
				if email in userlist['authors']:
					userobj = userlist['authors'][email]
				else:
					userobj = []
					userlist['authors'][email] = userobj
				if not name in userobj:
					userobj.append(name)
					
				#extract author
				email = value['committer']['email']
				name = value['committer']['name']
				if email in userlist['committers']:
					userobj = userlist['committers'][email]
				else:
					userobj = []
					userlist['committers'][email] = userobj
				if not name in userobj:
					userobj.append(name)
		

def main():
	parser = argparse.ArgumentParser("Builds an audit trace of the specified repo.")
	parser.add_argument("-o", "--owner", action="store", default=None, dest="user", help="The github user that owns a repo")
	parser.add_argument("-r", "--repo", action="store", default=None, dest="repo", help="The github repo to audit")
	parser.add_argument("-u", "--user", action="store", default=None, dest="user", help="Username")
	parser.add_argument("-p", "--pass", action="store", default=None, dest="password", help="Password")
	parser.add_argument("-w", "--write", action="store", default=None, dest="filename", help="File to write results to")
	
	args = parser.parse_args()
	audit_root = { 'committers' : {}, 'authors' : {}, 'suspicious': []
				}
	
	if args.user != None:
		auth = (args.user, args.password)
	else:
		auth = None
		
	#grab first page of commits for the repo
	path = "https://api.github.com/repos/{0}/{1}/commits?page=1&per_page=100".format(args.user, args.repo)
	print ("Requesting commit list for repo {0} owned by {1}".format(args.repo, args.user))
	sys.stdout.write("Working")
	r = requests.get(path, auth = auth)
	sys.stdout.write(".")
	sys.stdout.flush()
	if r.status_code == 200:
		extract_users(audit_root, json.loads(r.content))
    
	while('link' in r.headers and r.headers['link'].find("rel=\"next\"") != -1):
		nextUrl = None;
		l = link.parse_link_value(r.headers['link'])
		for key, value in l.iteritems():
			if value['rel'] == 'next':
				nextUrl = key
			 	break
		
		if (nextUrl != None):
			r = requests.get(nextUrl,auth = auth)
			sys.stdout.write(".")
			sys.stdout.flush()
		 	if r.status_code == 200:
		   		extract_users(audit_root, json.loads(r.content))
		file = None
	
	print(" finished")
	result = json.dumps(audit_root, sort_keys=True, indent=2)
	if args.filename == None:
		file = sys.stdout
	else:
		file = open(args.filename, "w")
		
	
	file.write(result)
	file.flush()
	if args.filename != None:
		file.close()

    
if __name__ == "__main__":
    main()
