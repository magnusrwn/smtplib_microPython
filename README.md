# Rasp Pi Pico W SMTP module


Others exist but I wanted to hand-code this for "fun"

Here are my terribel and short docs:

  - This is an imported object. You calls its methods to send you email
  - This is just made for text emails, but it really isnt to hard to add/chage things to make it more than text...
## Object description
  - Name: 'SMTPPico'
  - Methods: `[[__init__], establish_socket, dd_tls_ssl, send_email, close_socket]`
  - The above methods are ran in that order... usually...
  - Always close the socket

## Ipnuts in object definition
  - key_16:str, your google App Password
  - sender_email:str, your email
  - server:str, the server you want to sue to send the email (e.g., 'smtl.gmail.com')
        - Defualt to str:'smtp.gmail.com'
  - port:int, the port you will use
        - Defualt to int:587
  - name:str, the senders name

  ## Inputs in email sendings
  - sock:socket.socket, your secure socket
  - email_msg:str, your message for the email
  - email_recipient:str, the recipients email
  - email_subject:str, the subject of the email
  - recipient_name:str, the name of the recipient
