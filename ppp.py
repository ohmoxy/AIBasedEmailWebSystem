import poplib
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import policy
from email.message import EmailMessage
import os
from exts import db
from models import Mail,User
from flask import g  # 导入全局变量g
from ai_bd import main as ai_main


# 定义邮件内容类型类
class rc_mail:
    ogcont = "正文未导入"
    msg = "解析文本未导入"
    sender = ''       # 发送者未解包
    nickname = ''     # 发送者昵称
    addr = ''         # 发件者地址
    receiver = ''     # 收件者地址
    subject = ''      # 信件主题
    content_type = '' # 内容类型
    text = ''         # 正文内容
    charset = ''
    attachments = []  # 附件路径列表
    


def pop_connect(rc_mailserv,rc_mailport,rc_mailaddr,rc_mailpass):
    # 连接收件服务器
    pop_my = poplib.POP3(rc_mailserv, rc_mailport)
    print(f'请求连接收件服务器 {rc_mailserv}')
    print('----------------------------------------------------\n')
    try:
        login_welcome = pop_my.getwelcome().decode('utf-8')
        print(f'连接收件服务器 {rc_mailserv} 成功：\n{login_welcome}')
        print('----------------------------------------------------\n')
    except:
        print(f'连接收件服务器 {rc_mailserv} 失败:')
        print('----------------------------------------------------\n')
        return 0

    try:
        pop_my.user(rc_mailaddr)
        pop_my.pass_(rc_mailpass)
        print(f'登录收件账号 {rc_mailaddr} 成功：\n')
        print('----------------------------------------------------')
        return 1
    except:
        print( f'登录收件账号 {rc_mailaddr} 失败：\n请检查收件账户账号和密码')
        print('----------------------------------------------------')
        return 0

def pop_check(pop_my):
    print('邮件数量：%s 占用空间：%s' % pop_my.stat())
    resp, mails_num, octets = pop_my.list()
    print(mails_num)
    index = len(mails_num)
    print(f'最新邮件编号：{index}')
    return index

def pop_get(pop_my, last_num):
    # 获取邮箱信息
    print('邮件数量：%s 占用空间：%s' % pop_my.stat())
    resp, mails_num, octets = pop_my.list()
    print(mails_num)
    index = len(mails_num)
    print(f'邮件编号：{index}')
    
    newindexs = range(last_num + 1, index + 1)
    for index in newindexs:
        resp, lines, octets = pop_my.retr(index)
        print('------------------------邮件内容----------------------------')
        rc_mail.ogcont = b'\r\n'.join(lines).decode('utf-8')
        print(rc_mail.ogcont)
        rc_mail.msg = Parser(policy=policy.default).parsestr(rc_mail.ogcont)
        print('------------------------解析后的邮件----------------------------')
        print(rc_mail.msg)
        rc_mail.sender = rc_mail.msg.get('From')
        rc_mail.receiver = rc_mail.msg.get('To')
        rc_mail.subject = rc_mail.msg.get('Subject')
        print('------------------------邮件头----------------------------')
        print(rc_mail.sender)
        print(rc_mail.receiver)
        print(rc_mail.subject)
        print('----------------------------------------------------')
        
        rc_mail.nickname, rc_mail.addr = parseaddr(rc_mail.sender)
        
        decoded_addr = decode_header(rc_mail.addr)[0]
        if isinstance(decoded_addr[0], bytes):
            rc_mail.addr = decoded_addr[0].decode(decoded_addr[1] or 'utf-8')
        else:
            rc_mail.addr = decoded_addr[0]
        print('发件地址：', rc_mail.addr)
        
        decoded_nickname = decode_header(rc_mail.nickname)[0]
        if isinstance(decoded_nickname[0], bytes):
            rc_mail.nickname = decoded_nickname[0].decode(decoded_nickname[1] or 'utf-8')
        else:
            rc_mail.nickname = decoded_nickname[0]
        print('发件人：', rc_mail.nickname)
        
        decoded_subject = decode_header(rc_mail.subject)[0]
        if isinstance(decoded_subject[0], bytes):
            rc_mail.subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
        else:
            rc_mail.subject = decoded_subject[0]
        print('邮件主题：', rc_mail.subject)
        
        print('------------------------邮件正文----------------------------')
        rc_mail.charset = rc_mail.msg.get_charset()
        rc_mail.content_type = rc_mail.msg.get_content_type()
        print('邮件内容类型：', rc_mail.content_type)
        print('正文编码方式：', rc_mail.charset)
        rc_mail.msg.get('Date')
        rc_mail.attachments = []
        extract_content(rc_mail.msg)
        save_mail_to_db(rc_mail)

def extract_content(msg):
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                charset = part.get_content_charset() or 'utf-8'
                content = part.get_payload(decode=True).decode(charset, errors='ignore')
                print('邮件内容是：', content)
                if content_type == 'text/html':
                    rc_mail.text = content
            else:
                filename = part.get_filename()
                if filename:
                    decoded_filename = decode_header(filename)[0]
                    if isinstance(decoded_filename[0], bytes):
                        filename = decoded_filename[0].decode(decoded_filename[1] or 'utf-8')
                    else:
                        filename = decoded_filename[0]
                    save_attachment(part, filename)
    else:
        charset = msg.get_content_charset() or 'utf-8'
        content = msg.get_payload(decode=True).decode(charset, errors='ignore')
        print('邮件内容是：', content)
        rc_mail.text = content


def save_attachment(part, filename):
    user_id = g.user.id
    user_folder = os.path.join('files', str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'wb') as f:
        f.write(part.get_payload(decode=True))
    print(f'附件 {filename} 下载完毕')
    rc_mail.attachments.append(filepath)

def save_mail_to_db(rc_mail):
    try:
        aimail = ai_main(rc_mail.text)
        print('ai分析成功')
    except:
        print('ai分析失败')
    mail = Mail(
        time=rc_mail.msg.get('Date'),
        send_addr=rc_mail.addr,
        userID=g.user.id,
        nickname=rc_mail.nickname,
        recv_addr=rc_mail.receiver,
        subject=rc_mail.subject,
        content=rc_mail.text,
        messagecategory=aimail.mail_class1,
        state=aimail.mail_status,
        sum=aimail.mail_sum,
        attached=len(rc_mail.attachments) > 0,
        attachments=','.join(rc_mail.attachments)
    )
    user = User.query.get(g.user.id)
    user.mail_num += 1
    db.session.add(mail)
    db.session.commit()
