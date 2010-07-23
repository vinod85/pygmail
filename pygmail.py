import imaplib, re

class PyGmail(object):

	def __init__(self):
		self.IMAP_SERVER='imap.gmail.com'
		self.IMAP_PORT=993
		self.M = None

	def login (self, username, password):
		self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
		status, message = self.M.login(username, password)

	def get_mailbox_list(self):
		status, folders = self.M.list()
		return folders

	def get_mail_count(self, folder='Inbox'):
		status, count = self.M.select(folder, readonly=1)
		return count[0]

	def get_unread_count(self, folder='Inbox'):
		status, message = self.M.status(folder, "(UNSEEN)")
		unreadCount = re.search("UNSEEN (\d+)", message[0]).group(1)
		return unreadCount

