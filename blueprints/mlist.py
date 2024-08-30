from flask import Blueprint,request,render_template,jsonify,g,redirect,url_for
from models import Mail,User
from ppp import pop_connect,pop_check,pop_get
import requests
import json
import poplib
from decorators import login_required
from sqlalchemy import or_
from exts import db

bp = Blueprint("mlist",__name__,url_prefix="/")

@bp.route("/list",methods=['GET','POST'])
@login_required
def mlist():
    if g.user.recv_serv:
        mails = Mail.query.filter(Mail.userID == g.user.id).order_by(Mail.mail_id.desc()).all()
        rc_mailserv = g.user.recv_serv
        rc_mailport = g.user.recv_port
        rc_mailaddr = g.user.recv_addr
        rc_mailpass = g.user.recv_pwd
        last_num=''
        if request.method == ('POST'):
            
            pop_my=poplib.POP3(rc_mailserv)
            #服务器欢迎文字
            print(f'请求连接收件服务器{rc_mailserv}')
            print('----------------------------------------------------')
            try:
                login_welcome=pop_my.getwelcome()
                print(f'连接收件服务器{rc_mailserv}成功：\n{login_welcome}')
            except:
                print(f'连接收件服务器{rc_mailserv}失败')
                return jsonify({'message':f"连接发件服务器{rc_mailserv}失败"})
            print('----------------------------------------------------')

            #登录
            try:
                pop_my.user(rc_mailaddr)
                pop_my.pass_(rc_mailpass)
                print(f'登录收件账号{rc_mailaddr}成功：')
            except:
                print(f'登录收件账号{rc_mailaddr}失败：\n请检查收件账户账号mailaddr与收件账户密码mailpass{poplib.error_proto}')
            print('----------------------------------------------------')

            if pop_check(pop_my)<g.user.mail_num:
                user = User.query.get(g.user.id)
                user.mail_num = pop_check(pop_my)
                
            if pop_check(pop_my)>g.user.mail_num:
                last_num = g.user.mail_num
                pop_get(pop_my,last_num)
            return redirect(url_for('mlist.mlist'))

        return render_template("mlist.html",mails=mails)
    else : 
        return render_template("mlist.html")
@bp.route("/search",methods=['GET','POST'])
@login_required
def search():
    
    key = request.args.get("key", "")
    cate = request.args.getlist("cate")
    state = request.args.get("state", "")
    
    filters = [
        or_(Mail.subject.contains(key), Mail.content.contains(key)),
        Mail.userID == g.user.id
    ]
    
    if cate:
        filters.append(Mail.messagecategory.in_(cate))
    
    if state:
        filters.append(Mail.state == state)
    
    mails = Mail.query.filter(*filters).order_by(Mail.mail_id.desc()).all()
    return render_template("mlist.html", mails=mails, key=key, cate=cate, state=state)

@bp.route("/list/detail/<mail_getid>",methods=['GET','POST'])
@login_required
def mdetail(mail_getid):
    if g.user:
        dmail = Mail.query.filter_by(mail_id=mail_getid,userID=g.user.id).first()
        print (dmail.mail_id)
        return render_template('detail.html',dmail=dmail)
    
@bp.route("/list/delete/<mail_getid>",methods=['GET','POST'])
@login_required
def mdelete(mail_getid):
    if g.user:
        dmail = Mail.query.filter_by(mail_id=mail_getid, userID=g.user.id).first()
        if dmail:
            db.session.delete(dmail)
            db.session.commit()
            return redirect(url_for('mlist.mlist'))  # 假设你有一个视图函数列出所有邮件
        else:
            return "未找到邮件或无权限删除", 404
    return "用户未登录", 401