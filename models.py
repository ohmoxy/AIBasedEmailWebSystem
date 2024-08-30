from exts import db
from datetime import datetime
# 用户模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default = datetime.now)

    recv_addr = db.Column(db.String(100))
    recv_serv = db.Column(db.String(100))
    recv_port = db.Column(db.Integer)
    recv_pwd = db.Column(db.String(100))

    send_addr = db.Column(db.String(100))
    send_serv = db.Column(db.String(100))
    send_port = db.Column(db.Integer)
    send_pwd = db.Column(db.String(100))

    mail_num = db.Column(db.Integer, default = 0, nullable=False)

class Mail(db.Model):
    __tablename__ = "mail_management_system"
    #邮件id
    mail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(100), nullable=False)
    send_addr = db.Column(db.String(100),nullable=False)
    #userID 改为 整型
    userID = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(100))
    recv_addr = db.Column(db.String(100),nullable=False)
    subject = db.Column(db.Text)
    content = db.Column(db.Text)

    messagecategory = db.Column(db.String(100))
    state = db.Column(db.String(100))
    sum = db.Column(db.Text)
    attached = db.Column(db.Boolean)
    attachments = db.Column(db.Text)  # 附件路径