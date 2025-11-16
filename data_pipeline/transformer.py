import networkx as nx
import pandas as pd
import pickle
import json
from itertools import combinations

class GraphTransformer:
    def __init__(self):
        """
        Khởi tạo một đồ thị rỗng
        """
        self.G = nx.Graph()

    def _load_and_flatten_json(self, raw_filepath):
        """
        (Logic 'load_sparql_result' - v4 - Sửa lỗi 'unhashable type')
        Đọc file JSON và *luôn luôn* dùng json_normalize để làm phẳng,
        lấy ra các cột .value.
        """
        try:
            with open(raw_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data_to_normalize = None

            # TRƯỜNG HỢP 1: File là dictionary (chuẩn SPARQL)
            if isinstance(data, dict):
                data_to_normalize = data.get('results', {}).get('bindings', [])
                if not data_to_normalize:
                    print(f"THÔNG BÁO: File {raw_filepath} (dạng dict) hợp lệ, nhưng 'bindings' rỗng.")
                    return pd.DataFrame()

            # TRƯỜNG HỢP 2: File là list (dạng đã "phẳng" sẵn)
            elif isinstance(data, list):
                data_to_normalize = data
                if not data_to_normalize:
                    print(f"THÔNG BÁO: File {raw_filepath} (dạng list) hợp lệ, nhưng list rỗng.")
                    return pd.DataFrame()

            # TRƯỜNG HỢP 3: Dạng không xác định
            else:
                print(f"CẢNH BÁO: File {raw_filepath} có định dạng không hỗ trợ.")
                return pd.DataFrame()

            # **LUÔN LUÔN DÙNG JSON_NORMALIZE**
            # Đây là bước mấu chốt:
            # Nó sẽ biến data [ { "person": {"value": "id1"}, ... } ]
            # thành DataFrame có cột "person.value"
            print(f"THÔNG BÁO: Đang dùng pd.json_normalize cho file {raw_filepath}...")
            return pd.json_normalize(data_to_normalize)

        except FileNotFoundError:
            print(f"LỖI FILE NOT FOUND: Không tìm thấy file tại đường dẫn: {raw_filepath}")
            return pd.DataFrame()
        except json.JSONDecodeError:
            print(f"LỖI JSON DECODE: File {raw_filepath} không phải là file JSON hợp lệ.")
            return pd.DataFrame()
        except Exception as e:
            print(f"LỖI KHÔNG XÁC ĐỊNH khi đọc file {raw_filepath}: {e}")
            return pd.DataFrame()

    def _add_1_to_1_edges(self, df, relationship_label):
        """
        (Logic xử lý "vợ/chồng" 1-1)
        *** ĐÃ SỬA: Quay lại dùng đuôi .value ***
        """
        person_id_col = "person.value"
        person_label_col = "personLabel.value"
        related_id_col = f"{relationship_label}.value"
        related_label_col = f"{relationship_label}Label.value"

        required_cols = [person_id_col, person_label_col, related_id_col, related_label_col]
        if not all(col in df.columns for col in required_cols):
            print(f"Cảnh báo: Bỏ qua quan hệ 1-1 '{relationship_label}'. Thiếu cột. Yêu cầu: {required_cols}. Tìm thấy: {df.columns.tolist()}")
            return

        for _, row in df.iterrows():
            try:
                # person_id giờ sẽ là string (ví dụ "http://.../Q123"), không còn là dict
                person_id = row[person_id_col]
                person_name = row[person_label_col]
                related_id = row[related_id_col]
                related_name = row[related_label_col]

                if pd.isna(person_id) or pd.isna(related_id):
                    continue

                self.G.add_node(person_id, name=str(person_name))
                self.G.add_node(related_id, name=str(related_name))
                self.G.add_edge(person_id, related_id, relationship=relationship_label)
            except (KeyError, TypeError, ValueError):
                continue

    def _add_N_to_N_edges(self, df, hub_column, relationship_label):
        """
        (Logic "groupby" (N-N) xử lý "cùng trường", "cùng đảng phái"...)
        *** ĐÃ SỬA: Quay lại dùng đuôi .value ***
        """
        person_id_col = "person.value"
        person_label_col = "personLabel.value"

        # hub_column (ví dụ "school.value") được truyền vào
        required_cols = [person_id_col, person_label_col, hub_column]
        if not all(col in df.columns for col in required_cols):
            print(f"Cảnh báo: Bỏ qua quan hệ N-N '{relationship_label}'. Thiếu cột. Yêu cầu: {required_cols}. Tìm thấy: {df.columns.tolist()}")
            return

        # 1. Thêm tất cả các node trước
        for _, row in df.iterrows():
            try:
                person_id = row[person_id_col] # Lấy string ID
                person_name = row[person_label_col] # Lấy string Tên
                if not pd.isna(person_id):
                    # Thêm node với ID (string, hashable)
                    self.G.add_node(person_id, name=str(person_name))
            except (KeyError, TypeError, ValueError):
                continue

        # 2. Groupby theo "hub"
        # Các giá trị trong hub_column giờ là string (ví dụ "http://.../Q456"), hashable
        grouped = df.dropna(subset=[hub_column, person_id_col]).groupby(hub_column)

        for _, group in grouped:
            people_ids = group[person_id_col].unique()

            if len(people_ids) > 1:
                for person_a, person_b in combinations(people_ids, 2):
                    self.G.add_edge(person_a, person_b, relationship=relationship_label)

    def build_full_graph(self, raw_files_config):
        """
        (Hàm chính)
        Xây dựng đồ thị G_full từ một danh sách các file config.
        """
        print(f"Bắt đầu xây dựng đồ thị G_full từ {len(raw_files_config)} file...")
        self.G = nx.Graph()

        for config in raw_files_config:
            try:
                print(f"Đang xử lý: {config['path']} (Loại: {config['type']}, Nhãn: {config['label']})")

                df = self._load_and_flatten_json(config["path"])

                if df.empty:
                    print(f"Cảnh báo: DataFrame rỗng sau khi tải file {config['path']}. Bỏ qua.")
                    continue

                if config["type"] == "1-1":
                    self._add_1_to_1_edges(df, config["label"])

                elif config["type"] == "N-N":
                    self._add_N_to_N_edges(df, config["hub_col"], config["label"])

            except FileNotFoundError:
                print(f"Cảnh báo: Không tìm thấy file {config['path']}. Bỏ qua.")
            except KeyError as e:
                print(f"Cảnh báo: Lỗi cấu hình (thiếu key {e}) cho file {config['path']}. Bỏ qua.")
            except Exception as e:
                print(f"Cảnh báo: Lỗi không xác định khi xử lý {config['path']}: {e}. Bỏ qua.")

        print("---")
        print(f"Hoàn thành xây dựng đồ thị G_full.")
        print(f"Tổng số Node: {self.G.number_of_nodes()}")
        print(f"Tổng số Cạnh: {self.G.number_of_edges()}")
        return self.G

    def save_graph(self, output_path):
        """
        (Hàm lưu file .gpickle)
        """
        print(f"Đang lưu đồ thị vào {output_path}...")
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(self.G, f, pickle.HIGHEST_PROTOCOL)
            print(f"Đã lưu đồ thị thành công. (Nodes: {self.G.number_of_nodes()}, Edges: {self.G.number_of_edges()})")
        except Exception as e:
            print(f"Lỗi khi lưu đồ thị: {e}")


if __name__ == "__main__":

    # 1. Định nghĩa các file thô (sản phẩm của Quân)

    # *** PHẦN ĐÃ CHỈNH SỬA ***
    # Trỏ chính xác đến tên cột "hub" mà json_normalize sẽ tạo ra
    # (Dựa trên lỗi, file JSON của bạn có cột 'school')
    files_config = [
        {
            "path": "raw_data_edu_P69.json", # <-- Trỏ tới file của bạn
            "type": "N-N",
            "label": "school",
            "hub_col": "school.value"        # <-- ĐÃ SỬA: Quay lại dùng .value
        },
        # Thêm các file khác (vợ/chồng, đảng phái) vào đây
    ]

    # 2. Khởi tạo và xây dựng đồ thị
    transformer = GraphTransformer()
    G_full = transformer.build_full_graph(files_config)

    # 3. Lưu sản phẩm G_full.gpickle
    if G_full.number_of_nodes() > 0:
        transformer.save_graph("G_full.gpickle")
    else:
        print("Không thể lưu đồ thị vì đồ thị rỗng. Vui lòng kiểm tra lại các file JSON đầu vào.")