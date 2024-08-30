from flask import Blueprint,request,render_template,jsonify,redirect,url_for,session,g
from models import User
from exts import db
from models import Mail
from decorators import login_required

bp=Blueprint("userfile",__name__,url_prefix="")

@bp.route('/userfile', methods=['GET', 'POST'])
@login_required
def userfile():
    user = User.query.filter(User.id == g.user.id).first()
    if request.method == 'POST':
        # 获取表单数据
        
        user.recv_serv = request.form['recv_serv']
        user.recv_port = request.form['recv_port']
        user.recv_addr = request.form['recv_addr']
        user.recv_pwd = request.form['recv_pwd']

        user.send_serv = request.form['send_serv']
        user.send_port = request.form['send_port']
        user.send_addr = request.form['send_addr']
        user.send_pwd = request.form['send_pwd']

        db.session.commit() 
        return jsonify('用户配置已保存')
    else:
        return render_template('userfile.html',user = user)

        

        

    return render_template('login.html')