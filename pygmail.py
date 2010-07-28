#Fri Jul 23 12:51:57 IST 2010
# pygmail.py - A Python Library For Gmail

import imaplib, re

class pygmail(object):
	def __init__(self):
		self.IMAP_SERVER='imap.gmail.com'
		self.IMAP_PORT=993
		self.M = None
		self.response = None
		self.mailboxes = []

	def login(self, username, password):
		self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
		rc, self.response = self.M.login(username, password)
		return rc

	def get_mailboxes(self):
		rc, self.response = self.M.list()
		for item in self.response:
			self.mailboxes.append(item.split()[-1])
		return rc

	def get_mail_count(self, folder='Inbox'):
		rc, self.response = self.M.select(folder)
		return self.response[0]

	def get_unread_count(self, folder='Inbox'):
		rc, self.response = self.M.status(folder, "(UNSEEN)")
		unreadCount = re.search("UNSEEN (\d+)", self.response[0]).group(1)
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

	def rename_mailbox(self, oldmailbox, newmailbox):
		rc, self.response = self.M.rename(oldmailbox, newmailbox)
		return rc

	def create_mailbox(self, mailbox):
		rc, self.response = self.M.create(mailbox)
		return rc

	def delete_mailbox(self, mailbox):
		rc, self.response = self.M.delete(mailbox)
		return rc

	def logout(self):
		self.M.logout()
