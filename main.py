import socket
import time
# goog shi (below)
# dxpo grji cmsp zuir

class SMTPPPico:
	def __init__(self):
		self.port:int=587
		self.server:str="smtp.gmail.com"
		self.sender:str="magnurnew@gmail.com"
		self.key_16:str="dxpogrjicmspzuir"
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

	def format_message(self, message, recipient:str, subject:str):
		self.validate_recipient_email(recipient)

		smtp_commands = [
			# b"EHLO sender.com\r\n", # should be done?
			f"MAIL FROM:{self.sender}{self.nl}",
			f"RCPT TO:{recipient}\r\n",
			b"DATA\r\n",
			(
			f"From: Alice {self.sender}\r\n"
			f"To: Bob {recipient}\r\n"
			f"Subject: {subject}\r\n"
			f"Date: {time.gmtime()}\r\n" # spec dates/ types
			f"Message-ID: <20261112120000.12345@sender.com>\r\n"
			f"MIME-Version: 1.0\r\n"
			f'Content-Type: text/plain; charset="utf-8"\r\n'
			f"\r\n"
			f"Hi Bob,\r\n"
			f"\r\n"
			f"Here is the update you asked for. The report is attached.\r\n"
			f"\r\n"
			f"Best,\r\n"
			f"Alice\r\n"
			f".\r\n"
			),
			f"QUIT{self.nl}",
		]


	def send_email(self, sock:socket.socket, msg:str):
		sock.send(f"{self.nl}{msg.encode("urf-8")}{self.nl}")

	def close_socket(self, sock:socket.socket) -> None:
		sock.close()
		return
	
	def wrap_socket(self):
		'''
		
		Wrap the socekt in security
		'''
		pass
