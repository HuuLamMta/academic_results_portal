# 🎓 Tra Cứu Điểm Thi Sinh Viên

Ứng dụng Flask + SQLite tra cứu điểm thi, với dữ liệu thực từ file Excel.

## 📦 Cấu trúc

```
student-grades/
├── app.py              # Flask app chính
├── wsgi.py             # Entry point Gunicorn
├── grades.db           # SQLite database (98 SV, 107 môn, 5947 điểm)
├── requirements.txt
├── render.yaml
└── templates/
    └── index.html
```

## 🚀 Chạy local

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

## ☁️ Deploy lên Render

1. Push code lên GitHub (bao gồm cả file `grades.db`)
2. Vào [render.com](https://render.com) → **New → Blueprint** → kết nối repo
3. Render tự đọc `render.yaml` và deploy

> ⚠️ Commit `grades.db` vào git để dữ liệu có sẵn trên Render Free tier.
> Với dữ liệu cần cập nhật thường xuyên, dùng Render Disk hoặc PostgreSQL.

## 🔍 Tra cứu

Nhập MSSV, ví dụ: `2022010167`, `2022010056`, `2022010178`
