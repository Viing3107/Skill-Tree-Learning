import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model_list = genai.list_models()

def generate_skill_tree(subject: str):
    for model in model_list:
        if 'generateContent' in model.supported_generation_methods:
            # Thử với model này trước, nếu báo lỗi thì thử model tiếp theo
            curModel = genai.GenerativeModel(model.name)
            try:
                prompt = f"""
                Vai trò: Bạn là một Chuyên gia Thiết kế Chương trình Giảng dạy (Curriculum Architect) và Chuyên gia về {subject}. Nhiệm vụ của bạn là xây dựng một bản đồ lộ trình học tập (Learning Path) logic, có chiều sâu và khả thi cho người mới bắt đầu đến khi đạt mức độ chuyên sâu.

                Nhiệm vụ: Hãy tạo một Skill Tree chi tiết cho chủ đề: {subject}.

                Yêu cầu:
                    1. Cấu trúc nội dung:
                        - Số lượng node: Từ 6 đến 10 nodes.
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

                response = curModel.generate_content(prompt)
                text = response.text.strip()
                
                # Làm sạch JSON nếu AI trả về kèm markdown
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()

                return json.loads(text)

            except Exception as e:
                # Model hiện tại bị lỗi hoặc hết Quota
                print(f"Model {model.name} hết Quota hoặc bị lỗi")
                continue
    # Nếu tất cả model đều hết Quota thì trả về dữ liệu mẫu
    print("Đã hết Quota hoặc gặp lỗi, trả về dữ liệu mẫu.")
    return {
        "nodes": [
            {"id": "1", "title": f"Nhập môn {subject}", "description": "Các khái niệm cơ bản và thiết lập.", "prerequisites": []},
            {"id": "2", "title": "Kiến thức cơ bản", "description": "Nguyên lý và cú pháp cốt lõi.", "prerequisites": ["1"]},
            {"id": "3", "title": "Các chủ đề nâng cao", "description": "Đi sâu vào các tính năng phức tạp.", "prerequisites": ["2"]},
            {"id": "4", "title": "Dự án thực tế", "description": "Xây dựng các ứng dụng thực tế.", "prerequisites": ["3"]},
            {"id": "5", "title": "Tối ưu hóa hiệu năng", "description": "Làm cho nó nhanh và hiệu quả.", "prerequisites": ["3"]},
            {"id": "6", "title": "Triển khai", "description": "Chia sẻ công việc của bạn với thế giới.", "prerequisites": ["4", "5"]}
        ]
    }