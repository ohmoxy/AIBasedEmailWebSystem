from flask import Blueprint,request,render_template,jsonify,g
from smtp import smtp_connect,smtp_send
from decorators import login_required

bp=Blueprint("msend",__name__,url_prefix="/")

@bp.route("/send",methods=['GET','POST'])
@login_required
def send_mail():
    if request.method == 'POST':
        if g.user:
            #发件服务器
            fr_mailserv=g.user.send_serv
            #发件端口
            fr_mailport=g.user.send_port
            #发件账户地址
            fr_mailaddr=g.user.send_addr
            #发件账户密码
            fr_mailpass=g.user.send_pwd
            try:    
                smtp_connect(fr_mailserv,fr_mailport,fr_mailaddr,fr_mailpass)
                #发件人昵称
                fr_nickname = request.form['nickname']
                #收件方信息
                to_mailaddr = request.form['rc_mailaddr']
                #构造文本邮件
                subject = request.form['subject']
                text_info = request.form['content']
                
            except:
                return jsonify({'message': '登录服务器{{fr_mailserv}}失败，请检查发件服务器设置'})
            try: 
                smtp_send(fr_mailserv,fr_mailport,fr_mailaddr,fr_mailpass,fr_nickname,to_mailaddr,subject,text_info)
                return jsonify({'message': '发送成功！'})
            except:
                return jsonify({'message': '发件失败，请检查表单信息。'})
            
        return jsonify({'message': '您还未登陆'})
            


        
    return render_template('msend.html')