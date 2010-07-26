import imaplib, re

class PyGmail(object):

	def __init__(self):
		self.IMAP_SERVER='imap.gmail.com'
		self.IMAP_PORT=993
		self.M = None

	def login (self, username, password):
		self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
		status, message = self.M.login(username, password)

	def get_mailboxes(self):
		status, folders = self.M.list()
		return folders

	def get_mail_count(self, folder='Inbox'):
		status, count = self.M.select(folder, readonly=1)
		return count[0]

	def get_unread_count(self, folder='Inbox'):
		status, message = self.M.status(folder, "(UNSEEN)")
		unreadCount = re.search("UNSEEN (\d+)", message[0]).group(1)
		return unreadCount

	def get_imap_quota(self):
		quotaStr = self.M.getquotaroot("Inbox")[1][1][0]
		r = re.compile('\d+').findall(quotaStr)
		if r == []:
		  r.append(0)
		  r.append(0)
		return float(r[1])/1024, float(r[0])/1024

	def get_mails_from(self, uid, folder='Inbox'):
		status, count = self.M.select(folder, readonly=1)
		status, response = self.M.search(None, 'FROM', uid)
		email_ids = [e_id for e_id in response[0].split()]
		return email_ids

	def get_mail_from_id(self, id):
		status, response = self.M.fetch(id, '(body[header.fields (subject)])')
		return response

