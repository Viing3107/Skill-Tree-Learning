import os
import json
from google import genai
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model_name = "gemini-2.5-flash"

def generate_skill_tree(subject: str):
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

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    
    return json.loads(response.text)