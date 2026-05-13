import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Tìm đường dẫn tuyệt đối đến file .env
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "../../.env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_skill_tree(subject: str):
    # Dùng thẳng model ổn định nhất, không gọi list_models() để tránh bị Google check vùng
    model_name = "gemini-1.5-flash"
    
    try:
        print(f"Đang gọi AI (Gemini 1.5 Flash) cho chủ đề: {subject}")
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        Vai trò: Bạn là một Chuyên gia Thiết kế Chương trình Giảng dạy và Chuyên gia về {subject}.
        Nhiệm vụ: Tạo một Skill Tree chi tiết cho chủ đề: {subject}.

        Yêu cầu:
            1. Cấu trúc: 6 đến 10 nodes, chia thành 3 giai đoạn: Cơ bản, Trung cấp, Nâng cao.
            2. Chi tiết từng Node: title, description (20-30 từ), difficulty, estimated_hours.
            3. Ràng buộc: CHỈ trả về mã JSON hợp lệ, Tiếng Việt.

        Định dạng JSON:
        {{
          "nodes": [
            {{
              "id": "1",
              "title": "Tên chủ đề",
              "description": "Mô tả ngắn",
              "prerequisites": []
            }},
            {{
              "id": "2",
              "title": "Chủ đề tiếp theo",
              "description": "Mô tả ngắn",
              "prerequisites": ["1"]
            }}
          ]
        }}
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    except Exception as e:
        print(f"LỖI TẠI RENDER: {str(e)}")
        # Trả về dữ liệu mẫu nếu bị Google chặn vùng
        return {
            "nodes": [
                {"id": "1", "title": f"Nhập môn {subject}", "description": "Lỗi vùng địa lý Google Gemini trên Render. Đang dùng dữ liệu tạm.", "prerequisites": []},
                {"id": "2", "title": "Kiến thức cơ bản", "description": "Vui lòng thử đổi Region trên Render sang Singapore.", "prerequisites": ["1"]},
                {"id": "3", "title": "Kỹ năng thực chiến", "description": "Hoặc thử lại sau ít phút.", "prerequisites": ["2"]}
            ]
        }