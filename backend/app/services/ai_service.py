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

list_models = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-flash-latest",
    "models/gemini-flash-lite-latest",
    "models/gemini-pro-latest",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.5-flash-image",
    "models/gemini-3.1-flash-lite",
    "models/gemini-2.5-flash-native-audio-latest"
]

def generate_skill_tree(subject: str):
    for model_name in list_models:
        try:
            print(f"Trying AI with model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""
            Vai trò: Bạn là một Chuyên gia Thiết kế Chương trình Giảng dạy (Curriculum Architect) và Chuyên gia về {subject}. Nhiệm vụ của bạn là xây dựng một bản đồ lộ trình học tập (Learning Path) logic, có chiều sâu và khả thi cho người mới bắt đầu đến khi đạt mức độ chuyên sâu.

            Nhiệm vụ: Hãy tạo một Skill Tree chi tiết cho chủ đề: {subject}.

            Yêu cầu:
                1. Cấu trúc nội dung:
                    - Số lượng node: Từ 6 đến 14 nodes.
                    - Phân cấp: Chia lộ trình thành 3 giai đoạn: Cơ bản (Foundational), Trung cấp (Intermediate), và Nâng cao (Advanced/Specialized).
                    - Tính logic: Node sau phải kế thừa kiến thức từ node trước (dựa trên mảng prerequisites).

                2. Chi tiết từng Node:
                    - title: Tên chủ đề ngắn gọn, chuyên nghiệp.
                    - description: Mô tả từ 20-30 từ, nêu rõ người học sẽ làm được gì sau khi hoàn thành node này.
                    - difficulty: Mức độ khó (Beginner, Intermediate, Advanced).
                    - estimated_hours: Thời gian ước tính để nắm vững (số nguyên).

                3. Ràng buộc kỹ thuật:
                    - CHỈ trả về mã JSON hợp lệ (Valid JSON). Không thêm lời dẫn, không giải thích thêm, không sử dụng Markdown code blocks (json ... ).
                    - Đảm bảo không có dấu phẩy thừa ở cuối phần tử cuối cùng (tránh lỗi parse JSON).
                    - Ngôn ngữ: Tiếng Việt (Trừ khi yêu cầu Tiếng Anh, hoặc {subject} là chuyên ngành kỹ thuật).

            Định dạng JSON:
            {{
            "nodes": [
                {{
                "id": "1",
                "title": "Topic name",
                "description": "Short description",
                "prerequisites": []
                }},
                {{
                "id": "2",
                "title": "Next Topic",
                "description": "Short description",
                "prerequisites": ["1"]
                }}
            ]
            }}
            """

            response = model.generate_content(prompt)
            
            # Kiểm tra xem response có hợp lệ không
            if not response or not response.text:
                continue
                
            text = response.text.strip()
            
            # Làm sạch JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            print(f"--- SUCCESS WITH MODEL: {model_name} ---")
            return json.loads(text)

        except Exception as e:
            print(f"Error with {model_name}: {e}")
            continue

    # Fallback cuối cùng
    return {
        "nodes": [
            {"id": "1", "title": f"Nhập môn {subject}", "description": "Kiến thức cơ bản.", "prerequisites": []},
            {"id": "2", "title": "Kỹ năng thực hành", "description": "Làm chủ kiến thức.", "prerequisites": ["1"]}
        ]
    }