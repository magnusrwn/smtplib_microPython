import socket
import time
import ssl
import binascii


class SMTPPPico:
	def __init__(self, key_16:str, sender_email:str, name:str, port:int = 587, server:str = 'smtp.gmail.com'):
		self.port:int=port
		self.sender_email:str=sender_email
		self.server:str=server
		self.key_16:str=key_16
		self.nl:str="\r\n"
		self.name = name

	def __encode_to_base_64(self, text:str):
		return (binascii.b2a_base64(text.encode('utf-8'))).strip()

	def __validate_recipient_email(self, recip:str) -> None:
		necessary_chars = ['.', '@']
		if not all(c in recip for c in necessary_chars):
			raise Exception("Err validating email. Email recipient email must include '@' and '.'")
		return
	
	def establish_socket(self):
		gmail_smtp_ip = socket.getaddrinfo(self.server, self.port, socket.AF_INET)[0][-1]
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((gmail_smtp_ip))
		reci = sock.recv(1024)
		reci = reci.decode().split(" ")
		
		if reci[0][:1] != '2':
			raise Exception('Err with establsihing smtp connection\nReturning')

		msg = f"EHLO Magnuss-MacBook-Air.local{self.nl}"

		sock.sendall(msg.encode("utf-8"))
		reci = sock.recv(1024).decode().split(" ")
		reci_code = reci[0]

		if reci_code[0] != '2':
			raise Exception('Err with establsihing smtp connection\nReturning')
		return sock

	def add_tls_ssl(self, sock:socket.socket) -> socket.socket:
		msg = f"STARTTLS{self.nl}"
		sock.sendall(msg.encode("utf-8"))
		reci = sock.recv(1042).decode().split(" ")
		reci_code = reci[0]
		if reci_code != '220':
			raise Exception('Err with establsihing TLS on socket')

		context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		context.verify_mode = ssl.CERT_NONE

		ssl_sock = context.wrap_socket(sock, server_hostname=self.server)

		ssl_sock.sendall(f"EHLO Magnuss-MacBook-Air.local{self.nl}".encode('utf-8'))
		reci = ssl_sock.recv(1024)
		print(f"SSL/TSL AUTH RECI: {reci}")
		
		return ssl_sock
	
	def send_email(self, sock:socket.socket, email_msg:str, email_recipient:str, email_subject:str, recipient_name:str):
		self.__validate_recipient_email(email_recipient)

		smtp_command =[
			f"AUTH LOGIN{self.nl}",
			f"{bytes.decode(self.__encode_to_base_64(self.sender_email), 'ascii')}{self.nl}",
			f"{bytes.decode(self.__encode_to_base_64(self.key_16), 'ascii')}{self.nl}",
			f"MAIL FROM:<{self.sender_email}>\r\n",
			f"RCPT TO:<{email_recipient}>\r\n",
			"DATA\r\n",
			(
			f"From:{self.name} <{self.sender_email}>\r\n"
			f"To:{recipient_name} <{email_recipient}>\r\n"
			f"Subject: {email_subject}\r\n"
			f"Date: {str(time.gmtime())}\r\n"
			f"\r\n"
			f"{email_msg}\r\n"
			".\r\n"
			),
			"QUIT\r\n"
		]

		for cmd in smtp_command:
			print(cmd)
			print("\n")
			sock.sendall(bytes(cmd, 'utf-8'))
			reci = sock.recv(1042).decode()
			print(reci)
			print("\n")
			if reci[0] not in {'3', '2'}:
				raise Exception(f'Error in executing email-sending-commands')
		
		return
	
	def close_socket(self, sock:socket.socket) -> None:
		sock.close()
		return

