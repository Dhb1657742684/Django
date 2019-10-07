from flask import Blueprint

main = Blueprint('main', __name__)  # 创建蓝图
from . import views  # 导入执行，执行整个views里的视图
