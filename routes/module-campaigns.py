from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

bp = Blueprint('chienich', __name__, url_prefix='/chienich')

@bp.route('/')
@login_required
def index():
    """Danh sách chiến dịch - chienich.html"""
    return render_template('chienich/chienich.html')

@bp.route('/chitiet/<int:id>')
@login_required
def chitiet(id):
    """Chi tiết chiến dịch - chienichchitiet.html"""
    return render_template('chienich/chienichchitiet.html', id=id)

@bp.route('/dang-chay')
@login_required
def dang_chay():
    """Chiến dịch đang chạy - chienichchitamdung.html"""
    return render_template('chienich/chienichchitamdung.html')

@bp.route('/tam-dung')
@login_required
def tam_dung():
    """Chiến dịch tạm dừng - chienichtamdung.html"""
    return render_template('chienich/chienichtamdung.html')
