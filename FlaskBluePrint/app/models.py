from app import models


class BaseModel(models.Model):
    __abstract__ = True  # 声明当前类是抽象类，被继承调用不被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()


class Curriculum(BaseModel):  # 定义表
    __tablename__ = 'curriculum'
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)


class User(BaseModel):  # 定义表
    __tablename__ = 'user'
    username = models.Column(models.String(32))
    email = models.Column(models.String(32))
    password = models.Column(models.String(32))


class Leave(BaseModel):
    __tablename__ = 'leave'
    leave_id = models.Column(models.Integer)  # 请假人id
    leave_name = models.Column(models.String(32))  # 请假人姓名
    leave_type = models.Column(models.String(32))  # 假期类型
    leave_start = models.Column(models.String(32))  # 起始时间
    leave_end = models.Column(models.String(32))  # 结束时间
    leave_desc = models.Column(models.Text)  # 请假描述
    leave_phone = models.Column(models.String(32))  # 联系方式
    leave_status = models.Column(models.String(32))  # 假条状态 0 请假 1 批准 2 驳回 3 销假
