import david_user_interface

a = david_user_interface.InformUser()
message = """\
Subject: Message from test.py
This message is sent from Python."""
a.mail(message)