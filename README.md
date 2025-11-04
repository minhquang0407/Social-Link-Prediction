
Phân tích Mạng xã hội Người nổi tiếng & Dự đoán Mối liên kết (KLTN 2025)

Dự án Khóa luận Tốt nghiệp của Nhóm 3:
Quân: Extractor
Tân: Transformer / AI Lead
Quang: Loader / App Lead

1. 📜 Giới thiệu Dự án (Project Manifesto)

Dự án này là một ứng dụng Khoa học Dữ liệu End-to-End, thực hiện việc xây dựng và phân tích mạng lưới liên kết xã hội của những người nổi tiếng dựa trên dữ liệu từ The Movie Database (TMDb).
Dự án giải quyết hai mục tiêu chính:
Module 1: Phân tích "Sáu Bậc Xa cách" (Mô tả)
Xây dựng một đồ thị mạng lưới khổng lồ từ dữ liệu phim ảnh.
Triển khai thuật toán Tìm kiếm theo Chiều rộng (BFS) để tìm và trực quan hóa đường đi ngắn nhất (số "bậc" xa cách) giữa hai diễn viên bất kỳ.
Module 2: Dự đoán Mối liên kết (Dự đoán)
Sử dụng dữ liệu lịch sử (release_year) để "dạy" mô hình AI.
Xây dựng mô hình Machine Learning (Random Forest) để dự đoán xác suất hai diễn viên chưa từng hợp tác sẽ hợp tác với nhau trong tương lai, dựa trên các đặc trưng cấu trúc đồ thị (như Adamic-Adar, Jaccard...).

2. 🛠️ Ngăn xếp Công nghệ (Tech Stack)

Đây là các công cụ và thư viện chính được sử dụng trong dự án:
Ngôn ngữ: Python 3.9+
Thu thập Dữ liệu (ETL): requests (TMDb API), Pandas
Phân tích & Xử lý Đồ thị: NetworkX
Huấn luyện AI/ML: Scikit-learn
Ứng dụng Web (Demo): Streamlit
Trực quan hóa Đồ thị: Pyvis
Quản lý Mã nguồn: Git & GitHub

3. 🏗️ Kiến trúc Dự án

Dự án được chia thành 3 phần chính, tương ứng với 3 thành viên:
Pipeline Dữ liệu (ETL):
data_pipeline/data_collector.py (Quân): Lấy dữ liệu thô từ API.
data_pipeline/data_cleaner.py (Tân): Làm sạch và chuyển đổi sang "Golden Format".
data_pipeline/graph_builder.py (Quang): Nạp CSV, xây dựng và lưu đồ thị G_full.gpickle.
Logic Ứng dụng:
src/module_1_bfs.py (Quang): Chứa logic tìm đường đi ngắn nhất.
src/ai_utils.py (Tân): Chứa logic tạo bộ dữ liệu AI, trích xuất đặc trưng và dự đoán.
Giao diện Người dùng:
src/app.py (Quang): Ứng dụng Streamlit để tích hợp và demo cả 2 module.

4. 🚀 Hướng dẫn Cài đặt & Chạy (Setup & Run)

Đây là các bước để chạy dự án này trên máy của bạn.

A. Yêu cầu Tiên quyết

Python 3.9+
Git
Một API Key từ TMDb

B. Cài đặt

Clone (Tải về) kho chứa:
Bash
git clone https://[URL-CUA-BAN]/KLTN-Link-Prediction.git
cd KLTN-Link-Prediction


Tạo môi trường ảo (Khuyến nghị):
Bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .\.venv\Scripts\activate


Cài đặt thư viện:
Bash
pip install -r requirements.txt


Thiết lập API Key (Quan trọng):
Tạo một file tên là .env ở thư mục gốc.
Thêm vào file đó 1 dòng:
TMDB_API_KEY="KEY_CUA_BAN_DAT_VAO_DAY"


(File .env này đã được .gitignore phớt lờ để bảo mật)

C. Chạy Dự án


Bước 1: Chạy Pipeline Dữ liệu (Chỉ chạy 1 lần)

(Lưu ý: Bước này sẽ mất vài giờ để lấy dữ liệu và xây dựng đồ thị)
Chạy script của Quân (Extractor):
Bash
python data_pipeline/data_collector.py

(Chờ... script này chạy rất lâu. Sẽ tạo ra file data_output/raw_data_final.json)
Chạy script của Tân (Transformer):
Bash
python data_pipeline/data_cleaner.py

(Sẽ tạo ra file data_output/data_final.csv)
Chạy script của Quang (Loader):
Bash
python data_pipeline/graph_builder.py

(Sẽ tạo ra file data_output/G_full.gpickle)

Bước 2: Huấn luyện Mô hình AI (Chỉ chạy 1 lần)


Bash


python src/train.py  # (Tân sẽ tạo file này)


(Sẽ tạo ra file models/model.pkl)

Bước 3: Chạy Ứng dụng Web (Demo)


Bash


streamlit run src/app.py


Mở trình duyệt của bạn lên và truy cập http://localhost:8501.

5. 👥 Phân công & Đóng góp

Quân (Data Extractor):
Chịu trách nhiệm thiết kế và thực thi toàn bộ pipeline thu thập dữ liệu thô từ TMDb API.
Xử lý các vấn đề về giới hạn API, lỗi mạng và đảm bảo tính toàn vẹn của dữ liệu thô.
Tân (Data Transformer & AI Lead):
Chịu trách nhiệm làm sạch và chuyển đổi dữ liệu thô (JSON) sang "Golden Format" (data_final.csv).
Thiết kế và huấn luyện toàn bộ pipeline AI (Module 2), từ tạo mẫu Âm/Dương đến trích xuất đặc trưng và huấn luyện mô hình.
Quang (Data Loader & App Lead):
Chịu trách nhiệm xác thực dữ liệu (data_final.csv), nạp dữ liệu vào đồ thị NetworkX (G_full.gpickle).
Phát triển Module 1 (BFS).
Thiết kế và tích hợp toàn bộ dự án vào ứng dụng Streamlit (app.py).

