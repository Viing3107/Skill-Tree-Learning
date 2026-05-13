# 🧠 Skill Tree Learning - AI Roadmap Generator

Một ứng dụng web hiện đại giúp tự động hóa việc xây dựng lộ trình học tập (Skill Tree) cho bất kỳ chủ đề nào bằng trí tuệ nhân tạo (Google Gemini AI).

![Giao diện ứng dụng](https://img.shields.io/badge/UI-Neon_Dark-blueviolet)
![AI](https://img.shields.io/badge/AI-Google_Gemini-blue)
![Tech](https://img.shields.io/badge/Tech-Vue.js_%2B_FastAPI-green)

## 🌟 Tính năng nổi bật

- **AI Roadmap Generation**: Chỉ cần nhập chủ đề, AI sẽ thiết kế một cây kỹ năng từ cơ bản đến nâng cao.
- **Neon Dark UI**: Giao diện tối hiện đại với hiệu ứng ánh sáng Neon và tương tác mượt mà.
- **Interactive Skill Progression**: Theo dõi tiến trình học tập, mở khóa (Unlock) các kỹ năng mới sau khi hoàn thành kỹ năng tiên quyết.
- **XP System**: Hệ thống điểm kinh nghiệm (XP) giúp tăng động lực học tập.
- **Sidebar Details**: Xem chi tiết mô tả và yêu cầu của từng node kỹ năng.

## 🛠 Công nghệ sử dụng

### Frontend:
- **Vue.js 3**: Framework chính.
- **Vue Flow**: Thư viện hiển thị sơ đồ/cây tương tác.
- **Vanilla CSS**: Hiệu ứng Neon và Dark Mode tùy chỉnh.
- **Vite**: Công cụ build siêu nhanh.

### Backend:
- **FastAPI**: Python framework cho hiệu suất cực cao.
- **Google Generative AI SDK**: Tích hợp mô hình Gemini 1.5 Flash.
- **Uvicorn**: ASGI server để chạy ứng dụng.

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.10+
- Node.js 18+

### 2. Cấu hình Backend
1. Di chuyển vào thư mục backend:
   ```bash
   cd backend
   ```
2. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. Tạo file `.env` và thêm API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   PORT=8000
   ```
4. Chạy server:
   ```bash
   python app/main.py
   ```

### 3. Cấu hình Frontend
1. Di chuyển vào thư mục frontend:
   ```bash
   cd frontend
   ```
2. Cài đặt dependencies:
   ```bash
   npm install
   ```
3. Chạy môi trường phát triển:
   ```bash
   npm run dev
   ```

## 🌐 Triển khai (Deployment)

Dự án này được thiết kế để dễ dàng triển khai trên:
- **Backend**: Render, Railway hoặc Fly.io.
- **Frontend**: Vercel hoặc Netlify.

---
*Phát triển bởi Đỗ Quang Vinh*