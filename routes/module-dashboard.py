from flask import Blueprint, render_template
from flask_login import login_required
from app.services.analytics_service import AnalyticsService

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    """Trang chủ dashboard - index.html"""
    stats = AnalyticsService.get_overview_stats()
    return render_template('dashboard/index.html', stats=stats)

@bp.route('/tong-quan')
@login_required
def tongguan():
    """Tổng quan - tongguan.html"""
    data = AnalyticsService.get_detailed_stats()
    return render_template('dashboard/tongguan.html', data=data)

@bp.route('/analytics')
@login_required
def analytics():
    """Phân tích - analytics.html"""
    analytics_data = AnalyticsService.get_analytics()
    return render_template('dashboard/analytics.html', data=analytics_data)
