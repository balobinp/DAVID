import david_user_interface
import david_healthcheck


a = david_user_interface.InformUser()
message = """\
Subject: Message from test.py
This message is sent from Python."""
a.mail(message)