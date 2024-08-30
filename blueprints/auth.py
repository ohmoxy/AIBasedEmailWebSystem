# auth.py
from flask import Blueprint,request,render_template,jsonify,redirect,url_for,session
from models import User
from exts import db
from .forms import RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash

bp=Blueprint("auth",__name__,url_prefix="")

@bp.route("/login/reg", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(request.form)
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': '用户名已存在，请选择其他用户名。'})
        
        form = RegisterForm(request.form)
        if form.validate():
        # 创建新用户
            new_user = User(username=username, password = generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': '注册成功，请登录!'})
        else:
            return jsonify({'message': '用户名或密码非法（后端检查）'})

    return render_template('register.html')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'该用户不存在'})
        
        #哈希验证 数据库中保存的加密值与此时输入的值对比验证
        if check_password_hash(user.password,password):
            #登录cookie
            session['user_id'] = user.id
            return jsonify({'message': '登录成功!'})
        else:
            # 登录失败
            print(user)
            return jsonify({'message': '用户名或密码错误。'})

    return render_template('login.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")