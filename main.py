import socket
import time
# goog shi (below)
# dxpo grji cmsp zuir

class SMTPPPico:
	def __init__(self, key_16:str, sender:str, server:str, port:int):
		self.port:int=port
		self.server:str=server
		self.sender:str=sender
		self.key_16:str=key_16
		self.nl:str="\r\n"

	def establish_socket(self) -> socket.socket:
		gmail_smtp_ip = socket.getaddrinfo(self.server, self.port, socket.AF_INET)[0][-1]
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((gmail_smtp_ip))
		reci = sock.recv(1024)
		reci = reci.decode().split(" ")
		
		if reci[0][:1] != '2':
			raise Exception('Err with establsihing smtp connection\nReturning')

		msg = f"HELO Magnuss-MacBook-Air.local{self.nl}"

		sock.sendall(msg.encode("utf-8"))
		reci = sock.recv(1024).decode().split(" ")
		reci_code = reci[0]

		if reci_code[0] != '2':
			raise Exception('Err with establsihing smtp connection\nReturning')
		return sock

	def add_tls(self, sock:socket.socket) -> socket.socket:
		msg = f"STARTTLS{self.nl}"
		sock.sendall(msg.encode("utf-8"))
		reci = sock.recv(1042).decode().split(" ")
		reci_code = reci[0]
		if reci_code[0] != '2':
			raise Exception('Err with establsihing TLS on socket')
		return sock

	def validate_recipient_email(self, recip:str) -> None:
		necessary_chars = ['.', '@']
		if not all(c in recip for c in necessary_chars):
			raise Exception("Err validating email. Email recipient email must include '@' and '.'")
		return

	def build_smtp_commands(self, message, recipient:str, subject:str):
		# assume OK
		smtp_command = [
			f"MAIL FROM:{self.sender}\r\n",
			f"RCPT TO:{recipient}\r\n",
			"DATA\r\n",
			bytes((
			f"From: Alice {self.sender}\r\n"
			f"To: Bob {recipient}\r\n"
			f"Subject: {subject}\r\n"
			f"Date: {str(time.gmtime())}\r\n" # spec dates/ types
			# f"Message-ID: <20261112120000.12345@sender.com>\r\n" # neccessary?
			# f"MIME-Version: 1.0\r\n"
			# f'Content-Type: text/plain; charset="utf-8"\r\n' # neccessary?
			f"\r\n"
			f"{message}"
			".\r\n"
			), 'utf-8')
		]


	def send_email(self, sock:socket.socket, msg:str, recipient:str, email_subject:str):
		self.validate_recipient_email(recipient)
		commads = self.build_smtp_commands(msg, recipient, email_subject)

		# send them all
		# for mail_from, rcpt_to, data_cmd, payload in commads:
		# 	for step in (mail_from, rcpt_to, data_cmd, payload):
		# 		sock.sendall(step)
		# 		response = sock.recv(1024)
		# 		print(response.decode())

		

		sock.sendall(b"QUIT\r\n")
		
		return
	
	
	def close_socket(self, sock:socket.socket) -> None:
		sock.close()
		return

