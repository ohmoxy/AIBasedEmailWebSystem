from flask import Flask, jsonify, render_template, request, url_for, redirect,session,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
import config
from exts import db
from models import User,Mail
from blueprints.auth import bp as auth_bp
from blueprints.msend import bp as msend_bp
from blueprints.mlist import bp as mlist_bp
from blueprints.userfile import bp as userfile_bp
from apscheduler.schedulers.background import BackgroundScheduler  


app = Flask(__name__)

#绑定配置文件
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(auth_bp)
app.register_blueprint(msend_bp)
app.register_blueprint(mlist_bp)
app.register_blueprint(userfile_bp)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 测试数据库连接
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())


# 创建数据库表
with app.app_context():
    db.create_all()

@app.route("/")
def index0():
    return redirect(url_for('index'))

@app.route("/index")
def index():
    user = g.user
    if user:
        mails = Mail.query.filter(Mail.userID==user.id,Mail.state!='垃圾').order_by(Mail.mail_id.desc()).limit(3).all()
        mail_count = Mail.query.filter_by(userID=user.id).count()
        return render_template('index.html', user=user, mails=mails, mail_count=mail_count)
    else:
        return redirect(url_for('auth.login'))


@app.before_request
def my_before_request():
    #获取session中的user_id
    user_id = session.get("user_id")
    #根据user_id从数据库拿用户信息
    if user_id:
        user = User.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return{"user":g.user}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
