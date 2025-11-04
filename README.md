# Phân tích Mạng xã hội Người nổi tiếng & Dự đoán Mối liên kết

**Dự án Khóa luận Tốt nghiệp của Nhóm 3:**
* **Quân:** Extractor
* **Tân:** Transformer / AI Lead
* **Quang:** Loader / App Lead



---

## 1. 📜 Giới thiệu Dự án (Project Manifesto)

Dự án này là một ứng dụng Khoa học Dữ liệu End-to-End, thực hiện việc xây dựng và phân tích mạng lưới liên kết xã hội của những người nổi tiếng dựa trên dữ liệu từ **The Movie Database (TMDb)**.

Dự án giải quyết hai mục tiêu chính:

1.  **Module 1: Phân tích "Sáu Bậc Xa cách" (Mô tả)**
    * Xây dựng một đồ thị mạng lưới khổng lồ từ dữ liệu phim ảnh.
    * Triển khai thuật toán **Tìm kiếm theo Chiều rộng (BFS)** để tìm và trực quan hóa đường đi ngắn nhất (số "bậc" xa cách) giữa hai diễn viên bất kỳ.

2.  **Module 2: Dự đoán Mối liên kết (Dự đoán)**
    * Sử dụng dữ liệu lịch sử (`release_year`) để "dạy" mô hình AI.
    * Xây dựng mô hình **Machine Learning (Random Forest)** để dự đoán xác suất hai diễn viên *chưa từng* hợp tác sẽ hợp tác với nhau trong tương lai, dựa trên các đặc trưng cấu trúc đồ thị (như Adamic-Adar, Jaccard...).

## 2. 🛠️ Ngăn xếp Công nghệ (Tech Stack)

Đây là các công cụ và thư viện chính được sử dụng trong dự án:

* **Ngôn ngữ:** Python 3.9+
* **Thu thập Dữ liệu (ETL):** `requests` (TMDb API), `Pandas`
* **Phân tích & Xử lý Đồ thị:** `NetworkX`
* **Huấn luyện AI/ML:** `Scikit-learn`
* **Ứng dụng Web (Demo):** `Streamlit`
* **Trực quan hóa Đồ thị:** `Pyvis`
* **Quản lý Mã nguồn:** `Git` & `GitHub`



## 3. 🏗️ Kiến trúc Dự án

Dự án được chia thành 3 phần chính, tương ứng với 3 thành viên:

1.  **Pipeline Dữ liệu (ETL):**
    * `data_pipeline/data_collector.py` (Quân): Lấy dữ liệu thô từ API.
    * `data_pipeline/data_cleaner.py` (Tân): Làm sạch và chuyển đổi sang "Golden Format".
    * `data_pipeline/graph_builder.py` (Quang): Nạp CSV, xây dựng và lưu đồ thị `G_full.gpickle`.
2.  **Logic Ứng dụng:**
    * `src/module_1_bfs.py` (Quang): Chứa logic tìm đường đi ngắn nhất.
    * `src/ai_utils.py` (Tân): Chứa logic tạo bộ dữ liệu AI, trích xuất đặc trưng và dự đoán.
3.  **Giao diện Người dùng:**
    * `src/app.py` (Quang): Ứng dụng Streamlit để tích hợp và demo cả 2 module.

## 4. 🚀 Hướng dẫn Cài đặt & Chạy (Setup & Run)

Đây là các bước để chạy dự án này trên máy của bạn.

### A. Yêu cầu Tiên quyết
* Python 3.9+
* Git
* Một API Key từ [TMDb](https://www.themoviedb.org/)

### B. Cài đặt

1.  **Clone (Tải về) kho chứa:**
    ```bash
    git clone https://[URL-CUA-BAN]/Social-Link-Prediction.git
    cd Social-Link-Prediction
    ```

2.  **Tạo môi trường ảo (Khuyến nghị):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Trên Windows: .\.venv\Scripts\activate
    ```

3.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Thiết lập API Key (Quan trọng):**
    * Tạo một file tên là `.env` ở thư mục gốc.
    * Thêm vào file đó 1 dòng:
        ```
        TMDB_API_KEY="KEY_CUA_BAN_DAT_VAO_DAY"
        ```
    *(File `.env` này đã được `.gitignore` phớt lờ để bảo mật)*

### C. Chạy Dự án

#### Bước 1: Chạy Pipeline Dữ liệu (Chỉ chạy 1 lần)
*(Lưu ý: Bước này sẽ mất vài giờ để lấy dữ liệu và xây dựng đồ thị)*

1.  **Chạy script của Quân (Extractor):**
    ```bash
    python data_pipeline/data_collector.py
    ```
    *(Chờ... script này chạy rất lâu. Sẽ tạo ra file `data_output/raw_data_final.json`)*

2.  **Chạy script của Tân (Transformer):**
    ```bash
    python data_pipeline/data_cleaner.py
    ```
    *(Sẽ tạo ra file `data_output/data_final.csv`)*

3.  **Chạy script của Quang (Loader):**
    ```bash
    python data_pipeline/graph_builder.py
    ```
    *(Sẽ tạo ra file `data_output/G_full.gpickle`)*

#### Bước 2: Huấn luyện Mô hình AI (Chỉ chạy 1 lần)

*(Giả sử Tân tạo file train.py ở thư mục gốc)*
```bash
python train.py
