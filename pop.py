import poplib,time
from colorama import Fore,Back,Style
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
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
print('------------------------lines----------------------------')
print('邮件内容：',lines)
#获取邮件原始文本
rc_mail.ogcont= b'\r\n'.join(lines).decode('utf-8')
print('------------------------ogcont----------------------------')
print(rc_mail.ogcont)
#解析邮件内容
rc_mail.msg=Parser().parsestr(rc_mail.ogcont)
print('------------------------msg----------------------------')
print(rc_mail.msg)
#解析邮件头
rc_mail.sender=rc_mail.msg.get('From')      #发送者
rc_mail.receiver=rc_mail.msg.get('To')      #接收者
rc_mail.subject=rc_mail.msg.get('Subject')     #主题
print('------------------------email header----------------------------')
print(rc_mail.sender)
print(rc_mail.receiver)
print(rc_mail.subject)
#发送者的昵称、地址解码
print('----------------------------------------------------')
rc_mail.nickname,rc_mail.addr=parseaddr(rc_mail.sender)
print(rc_mail.nickname,'1',rc_mail.addr)
rc_mail.addr,rc_mail.charset=decode_header(rc_mail.addr)[0]     #获取地址
if rc_mail.charset:
    rc_mail.addr=rc_mail.addr.decode(rc_mail.charset)           #地址解码
    print('发件地址：',rc_mail.addr)
else:
    print('发件地址：',rc_mail.addr)
rc_mail.nickname,rc_mail.charset=decode_header(rc_mail.nickname)[0]     #获取昵称
if rc_mail.charset:
    rc_mail.nickname=rc_mail.nickname.decode(rc_mail.charset)           #昵称解码
    print('发件人：',rc_mail.nickname)
else:
    print('发件人：',rc_mail.nickname)
#信件主题解码
rc_mail.subject,rc_mail.charset=decode_header(rc_mail.subject)[0]
if rc_mail.charset:
    rc_mail.subject=rc_mail.subject.decode(rc_mail.charset)
print('邮件主题：',rc_mail.subject)
#邮件内容解码
print('------------------------email text----------------------------')
rc_mail.charset=rc_mail.msg.get_charset()
rc_mail.content_type=rc_mail.msg.get_content_type()
print('邮件内容类型：',rc_mail.content_type)
print('正文编码方式：',rc_mail.charset)

if(rc_mail.msg.is_multipart()):
    parts=rc_mail.msg.get_payload()
print(parts)
print(list(enumerate(parts)))
for n,part in enumerate(parts):
    content_type = part.get_content_type()
    print('邮件的第{}部分内容，类型为{}.'.format(n+1,content_type))
    if content_type == 'multipart/alternative':
        content =part.get_payload()
        # print(content)
        for p in content:
            content_type =p.get_content_type()
            if content_type =='text/plain' or content_type == 'text/html':
                content =p.get_payload(decode=True)
                print('这部分邮件内容:',content)

                if charset is None:   #注意这个charset
                    #获取邮件对象的编码方式
                    content_type =p.get('Content-Type','').lower()
                    print(content_type)
                    pos = content_type.find('charset=')
                    if pos >= 0:
                        charset =content_type[pos +8:].strip()
                        if charset:
                            #解码后的邮件内容
                            content=content.decode(charset)
                print('正文内容是:{}'.format(content))
            else:
                # print(part,type(part))
                filename = part.get('Content-Disposition')
                # print(type(filename))
                pos = filename.find('filename=')
                filename = filename[pos+9:].strip('"')
                # print(filename)

                # charset = part.get('Content-Transfer-Encoding')
                # print(charset)
                content = part.get_payload(decode=True)
                #print('附件邮件对象是:content)

                with open(filename,'wb')as f:
                    f.write(content)
                print('第{个附件{}下载完毕'.format(n,filename))





if(rc_mail.msg.is_multipart()):
    parts=rc_mail.msg.get_payload()
print(parts)
print(list(enumerate(parts)))
for n,part in enumerate(parts):
    content_type = part.get_content_type()
    print('邮件的第{}部分内容，类型为{}.'.format(n+1,content_type))
    if content_type == 'multipart/alternative':
        content =part.get_payload()
        # print(content)
        for p in content:
            content_type =p.get_content_type()
            if content_type =='text/plain' or content_type == 'text/html':
                content =p.get_payload(decode=True)
                print('这部分邮件内容:',content)

                if charset is None:   #注意这个charset
                    #获取邮件对象的编码方式
                    content_type =p.get('Content-Type','').lower()
                    print(content_type)
                    pos = content_type.find('charset=')
                    if pos >= 0:
                        charset =content_type[pos +8:].strip()
                        if charset:
                            #解码后的邮件内容
                            content=content.decode(charset)
                print('正文内容是:{}'.format(content))
            else:
                # print(part,type(part))
                filename = part.get('Content-Disposition')
                # print(type(filename))
                pos = filename.find('filename=')
                filename = filename[pos+9:].strip('"')
                # print(filename)

                # charset = part.get('Content-Transfer-Encoding')
                # print(charset)
                content = part.get_payload(decode=True)
                #print('附件邮件对象是:content)

                with open(filename,'wb')as f:
                    f.write(content)
                print('第{个附件{}下载完毕'.format(n,filename))
#退出服务
pop_my.quit()