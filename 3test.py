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
from colorama import Fore,Back,Style

#邮件内容类型定义
class rc_mail:
    ogcont="正文未导入"
    msg="解析文本未导入"
    sender=''       #发送者未解包
    nickname=''     #发送者昵称
    addr=''         #发件者地址
    receiver=''     #收件者地址
    subject=''      #信件主题
    content_type='' #内容类型
    text=''         #
    
    charset=''
#收件服务器
rc_mailserv='imap.exmail.qq.com'
#收件端口
rc_mailport=993
#收件账户地址
rc_mailaddr='zijie.oy@bupt.edu.cn'
#收件账户密码
rc_mailpass='20042004323oySTU'
#连接收件服务器
pop_my=poplib.POP3(rc_mailserv)
#服务器欢迎文字
print(f'请求连接收件服务器{rc_mailserv}')
print('----------------------------------------------------\n')
try:
    login_welcome=pop_my.getwelcome()
    print(Fore.GREEN+f'连接收件服务器{rc_mailserv}成功：\n{login_welcome}')
    print(Style.RESET_ALL)
except:
    print(Fore.RED+f'连接收件服务器{rc_mailserv}失败')
    print(Style.RESET_ALL)
print('----------------------------------------------------\n')

#登录
try:
    pop_my.user(rc_mailaddr)
    pop_my.pass_(rc_mailpass)
    print(f'登录收件账号{rc_mailaddr}成功：\n')
    print(Style.RESET_ALL)
except:
    print(Fore.RED+f'登录收件账号{rc_mailaddr}失败：\n请检查收件账户账号mailaddr与收件账户密码mailpass{poplib.error_proto}')
    print(Style.RESET_ALL)
print('----------------------------------------------------')


def pop_get(pop_my, last_num):
    #获取邮箱信息
    print('邮件数量：%s 占用空间：%s'%pop_my.stat())
    #mails_num获取邮件编号
    resp,mails_num,octets=pop_my.list()
    print(mails_num)
    #利用列表长度获取最新邮件编号
    index=len(mails_num)
    print(f'邮件编号：{index}')
    #获取最新电子邮件
    resp,lines,octets=pop_my.retr(index)
    print ('111')
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
            rc_mail.addr, rc_mail.charset = decode_header(rc_mail.addr)[0]
            if rc_mail.charset:
                rc_mail.addr = rc_mail.addr.decode(rc_mail.charset)
                print('发件地址：', rc_mail.addr)
            else:
                print('发件地址：', rc_mail.addr)
            rc_mail.nickname, rc_mail.charset = decode_header(rc_mail.nickname)[0]
            if rc_mail.charset:
                rc_mail.nickname = rc_mail.nickname.decode(rc_mail.charset)
                print('发件人：', rc_mail.nickname)
            else:
                print('发件人：', rc_mail.nickname)
            rc_mail.subject, rc_mail.charset = decode_header(rc_mail.subject)[0]
            if rc_mail.charset:
                rc_mail.subject = rc_mail.subject.decode(rc_mail.charset)
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
                charset = part.get_content_charset()
                content = part.get_payload(decode=True).decode(charset, errors='ignore')
                print('邮件内容是：', content)
                if content_type == 'text/html':
                    rc_mail.text = content
            else:
                filename = part.get_filename()
                if filename:
                    charset = part.get_content_charset()
                    if charset:
                        filename = decode_header(filename)[0][0].decode(charset)
                    save_attachment(part, filename)
    else:
        rc_mail.charset = msg.get_content_charset()
        if rc_mail.charset:
            content = msg.get_payload(decode=True).decode(rc_mail.charset, errors='ignore')
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
    mail = Mail(
        time=rc_mail.msg.get('Date'),
        send_addr=rc_mail.addr,
        #后续修改
        #userID=g.user.id,
        userID=4,
        nickname=rc_mail.nickname,
        recv_addr=rc_mail.receiver,
        subject=rc_mail.subject,
        content=rc_mail.text,
        messagecategory='',
        state='',
        sum='',
        attached=len(rc_mail.attachments) > 0,
        attachments=','.join(rc_mail.attachments)
    )
    #后续修改
    #user = User.query.get(g.user.id)
    user = User.query.get(4)
    user.mail_num += 1
    db.session.add(mail)
    db.session.commit()

pop_get(pop_my,2)