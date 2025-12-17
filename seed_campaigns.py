from app import create_app, db
from app.models.campaign import Campaign
from datetime import datetime

app = create_app()

# Dữ liệu mẫu (Platform: facebook, google, tiktok, youtube)
SAMPLE_CAMPAIGNS = [
    {
        "name": "Khuyến mãi Mùa Hè 2025 - Facebook Ads",
        "platform": "facebook",
        "status": "active",
        "budget": 5000000,
        "spent": 1250000,
        "reach": 15000,
        "clicks": 4500,
        "conversions": 210,
        "start_date": "2025-06-01",
        "end_date": "2025-06-30"
    },
    {
        "name": "Quảng cáo tìm kiếm - Google Search",
        "platform": "google",
        "status": "active",
        "budget": 10000000,
        "spent": 8500000,
        "reach": 8500,
        "clicks": 1200,
        "conversions": 340,
        "start_date": "2025-01-01",
        "end_date": "2025-01-15"
    },
    {
        "name": "Video giới thiệu Khách sạn - Youtube",
        "platform": "youtube",
        "status": "paused",
        "budget": 2000000,
        "spent": 500000,
        "reach": 5000,
        "clicks": 100,
        "conversions": 10,
        "start_date": "2025-11-20",
        "end_date": "2025-11-30"
    },
    {
        "name": "Chiến dịch Tết 2026",
        "platform": "tiktok",
        "status": "scheduled",
        "budget": 15000000,
        "spent": 0,
        "reach": 0,
        "clicks": 0,
        "conversions": 0,
        "start_date": "2025-12-01",
        "end_date": "2026-01-31"
    }
]

with app.app_context():
    db.create_all()
    print("🚀 Đang tạo dữ liệu chiến dịch mẫu...")
    
    # Xóa cũ (nếu muốn reset)
    # Campaign.query.delete()

    count = 0
    for data in SAMPLE_CAMPAIGNS:
        if not Campaign.query.filter_by(name=data["name"]).first():
            camp = Campaign(
                name=data["name"],
                platform=data["platform"],
                status=data["status"],
                budget=data["budget"],
                spent=data["spent"],
                reach=data["reach"],
                clicks=data["clicks"],
                conversions=data["conversions"],
                start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(data["end_date"], "%Y-%m-%d")
            )
            db.session.add(camp)
            count += 1
    
    db.session.commit()
    print(f"✅ Đã thêm {count} chiến dịch!")
