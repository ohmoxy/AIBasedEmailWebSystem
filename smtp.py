import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

def smtp_connect(fr_mailserv,fr_mailport,fr_mailaddr,fr_mailpass):
    try:
        #连接服务器地址与端口
        smtp_my=smtplib.SMTP_SSL(fr_mailserv)
        smtp_my.connect(fr_mailserv, fr_mailport)
        #登录服务器
        smtp_my.login(fr_mailaddr, fr_mailpass)
        return 1
    except:
        return 0
    finally:
    #关闭连接
        smtp_my.quit()

def smtp_send(fr_mailserv,fr_mailport,fr_mailaddr,fr_mailpass,fr_nickname,to_mailaddr,subject,text_info):
    try:
        my_msg = MIMEText(text_info,  #正文内容
                'plain',    #正文内容类型 plain：纯文本
                'utf-8'     #编码方式
                )
        
        #邮件头Header（QQ邮箱标准 RFC5322, RFC2047, RFC822）
        my_msg['From'] = f'=?UTF-8?B?{base64.b64encode(fr_nickname.encode()).decode()}?= <{fr_mailaddr}>'
        my_msg['To'] = Header(to_mailaddr)
        my_msg['Subject'] = Header(subject,'utf-8')

        #连接服务器地址与端口
        smtp_my=smtplib.SMTP_SSL(fr_mailserv)
        smtp_my.connect(fr_mailserv, fr_mailport)
        #登录服务器
        smtp_my.login(fr_mailaddr, fr_mailpass)
        #发送邮件
        smtp_my.sendmail(fr_mailaddr, to_mailaddr, my_msg.as_string())
        print("邮件发送成功")
        return 1
    except smtplib.SMTPException:
        print("邮件发送失败")
        return 0
    finally:
        #关闭连接
        smtp_my.quit()