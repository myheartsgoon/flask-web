#-*- coding: utf8 -*-
from flask import Blueprint
from flask_mail import Mail, Message
import os

mail_bp = Blueprint('mail', __name__, template_folder='templates')

mail = Mail()
@mail_bp.route('/mail')
def sendmail():
    msg = Message('Hi', sender='408168042@qq.com', recipients=['408168042@qq.com'], html='<b>Hello Web</b>',
                  body='The first email!')
    mail.send(msg)
    return '<h1>OK!</h1>'

