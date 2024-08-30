import wtforms
from wtforms.validators import Length,EqualTo
from models import User
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=1,max=20,message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=8,max=32,message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    #用户名是否已注册
    def validate_username(self,field):
        username=field.data
        user = User.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError(message="该用户名已经被注册！")