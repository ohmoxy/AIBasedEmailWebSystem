# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header


# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = 'zijie.oy@bupt.edu.cn'
password = '20042004323oySTU'
# 收信方邮箱
to_addr = '1634734562@qq.com'
# 发信服务器
smtp_server = 'smtp.exmail.qq.com'

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
msg = MIMEText('使用python发送邮件测试', 'plain', 'utf-8')
# 邮件头信息
msg['From'] = Header(from_addr)  # 发送者
msg['To'] = Header(to_addr)  # 接收者
subject = 'Python SMTP 邮件测试'
msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题

try:
    smtpobj = smtplib.SMTP_SSL(smtp_server)
    # 建立连接--qq邮箱服务和端口号（可百度查询）
    smtpobj.connect(smtp_server, 465)    
    # 登录--发送者账号和口令
    smtpobj.login(from_addr, password)   
    # 发送邮件
    smtpobj.sendmail(from_addr, to_addr, msg.as_string()) 
    print("邮件发送成功")
except smtplib.SMTPException:
    print("无法发送邮件")
finally:
    # 关闭服务器
    smtpobj.quit()

