#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import smtplib
import socket
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import parseaddr, formataddr

logging.basicConfig(level=logging.INFO,
                    format='%(acstime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class MailUtil(object):
    """Class of sendmail
    """

    def __init__(self, host, port=25, user, password, from_addr):
        # from_user_name <from_user@example.com>
        self.from_addr = from_addr
        self.server = self.instance_smtp(host, port, user, password)

    def instance_smtp(self, host, port, user, password):
        try:
            server = smtplib.SMTP(host, port)
            server.login(user, password)
        except socket.error as e:
            logging.error("Could not connect to {0}:{1}".format(host, port))
        except:
            logging.exception(str(e))
        finally:
            if server != None:
                server.quit()
        return server

    def format_addr(self, mail_addr):
        name, addr = parseaddr(mail_addr)
        return formataddr(Header(name, 'utf-8').encode(), addr)

    def send(self, to_addrs, cc_addrs, subject, context, files):
        """
        Invoke method to send mail
        :param to_addrs: Ex. ["Atom <atom@example.com>","Jason <jason@example.com>"]
        :param cc_addrs: Ex. ["Atom <atom@example.com>","Jason <jason@example.com>"]
        :param subject: The subject of mail
        :param context: The context of mail, default HTML format
        :param files: The attachs of mail
        :return:
        """
        server = self.server
        from_addr = self.from_addr
        msg_context = MIMEText(context, 'html', 'utf-8')
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = ",".join(self.format_addr(x) for x in to_addrs)
        if cc_addrs != None:
            msg["CC"] = ",".join(self.format_addr(x) for x in cc_addrs)
        msg["Subject"] = Header(subject, 'utf-8').encode()
        if files != None and len(files) > 0:
            for file in files:
                if os.path.isfile(file):
                    part = MIMEApplication(open(file, 'rb').read(), 'utf-8')
                    part.add_header('Content-Disposition', 'attachment',
                                    filename=os.path.basename(file))
                    msg.attach(part)
        msg.attach(msg_context)
        try:
            server.sendmail(from_addr, to_addrs + cc_addrs, msg.as_string())
        except socket.error as e:
            logging.error("Could not connect to {0}:{1}".format(host, port))
        except:
            logging.exception(str(e))
        finally:
            if server != None:
                server.quit()
