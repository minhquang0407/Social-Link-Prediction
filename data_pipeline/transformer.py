import networkx as nx
import pandas as pd
import json
import pickle
import re
from itertools import combinations


class GraphTransformer:
    def __init__(self):
        """
        Khởi tạo đồ thị rỗng và dictionary chứa sở thích tạm thời
        """
        self.G = nx.Graph()
        self.person_interests_map = {}  # Dùng để gom sở thích: { "ID_Person": {"Football", "Music"} }
        print("GraphTransformer initialized.")

    def _load_and_flatten_json(self, raw_filepath):
        """
        Load file JSON và làm phẳng bằng json_normalize.
        Luôn trả về DataFrame (có thể rỗng).
        """
        try:
            with open(raw_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data_to_normalize = None
            if isinstance(data, dict):
                data_to_normalize = data.get('results', {}).get('bindings', [])
            elif isinstance(data, list):
                data_to_normalize = data

            if not data_to_normalize:
                return pd.DataFrame()

            # Làm phẳng JSON -> DataFrame
            df = pd.json_normalize(data_to_normalize)
            return df

        except Exception as e:
            print(f"LỖI LOAD FILE {raw_filepath}: {e}")
            return pd.DataFrame()

    def _clean_label(self, label):
        """
        Làm sạch Label:
        - Nếu label là None/NaN -> Trả về None
        - Nếu label bắt đầu bằng 'Q' theo sau là số (VD: Q42, Q12345) -> Coi là rác, trả về None.
        - Còn lại giữ nguyên.
        """
        if pd.isna(label):
            return None

        label_str = str(label).strip()

        # Regex kiểm tra pattern Q + số (VD: ^Q\d+$)
        if re.match(r'^Q\d+$', label_str):
            return None

        return label_str

    def _aggregate_interests(self, file_list):
        """
        Gom tất cả sở thích từ danh sách file vào self.person_interests_map.
        Không thêm vào đồ thị ngay, chỉ lưu vào Dict để tra cứu sau.
        Input: file_list = [("path/to/interest.json", "interest_col_name"), ...]
        """
        print("Đang tổng hợp dữ liệu sở thích (Interests)...")
        for filepath, interest_obj_col in file_list:
            df = self._load_and_flatten_json(filepath)

            # Cần cột person.value và cột chứa sở thích (VD: interest.value)
            if 'person.value' not in df.columns:
                continue

            # Tìm tên cột label của sở thích (VD: interestLabel.value)
            # Thường file SPARQL sẽ có cột: objectLabel.value hoặc tên_cụ_thểLabel.value
            # Ở đây ta sẽ tìm cột có đuôi 'Label.value' tương ứng với interest_obj_col
            label_col = f"{interest_obj_col}Label.value"

            # Nếu không tìm thấy đúng tên cột label, thử dùng 'objectLabel.value' mặc định
            if label_col not in df.columns and 'objectLabel.value' in df.columns:
                label_col = 'objectLabel.value'

            if label_col not in df.columns:
                continue

            for _, row in df.iterrows():
                p_id = row['person.value']
                # Lấy label sở thích và làm sạch
                raw_interest = row[label_col]
                clean_interest = self._clean_label(raw_interest)

                if p_id and clean_interest:
                    if p_id not in self.person_interests_map:
                        self.person_interests_map[p_id] = set()
                    self.person_interests_map[p_id].add(clean_interest)

        print(f"-> Đã tổng hợp sở thích cho {len(self.person_interests_map)} người.")

    def _add_generic_relation(self, df, target_node_type, rel_label):
        """
        Thêm quan hệ chung vào đồ thị.
        - target_node_type: Loại node đích (chỉ để log hoặc mở rộng sau này).
        - rel_label: Tên cạnh (VD: "spouse", "member of").
        - Logic: Luôn tìm cột 'person' và 'object'.
        """
        # Các cột bắt buộc cơ bản
        p_id_col = "person.value"
        p_label_col = "personLabel.value"
        obj_id_col = "object.value"  # Mặc định SPARQL nên trả về ?object
        obj_label_col = "objectLabel.value"

        # Map các cột thuộc tính bổ sung (nếu có trong file JSON)
        # Key: Tên cột trong DataFrame -> Value: Tên thuộc tính lưu vào Node
        attribute_map = {
            "personDescription.value": "description",
            "dob.value": "date_of_birth",
            "pobLabel.value": "place_of_birth",  # Lấy Label nơi sinh
            "countryLabel.value": "nationality"  # Lấy Label quốc tịch
        }

        # Kiểm tra cột cơ bản
        if p_id_col not in df.columns or obj_id_col not in df.columns:
            print(f"  [SKIP] File thiếu cột ID (person.value hoặc object.value).")
            return

        count = 0
        for _, row in df.iterrows():
            # 1. Xử lý PERSON (Node nguồn)
            p_id = row[p_id_col]
            # Ưu tiên lấy label từ dữ liệu, nếu lỗi Q-ID thì bỏ qua dòng này hoặc lấy ID làm tên tạm (tùy logic)
            # Ở đây: Nếu tên là Q-ID thì coi như không hợp lệ -> Bỏ qua label đó (Node vẫn tạo nhưng tên là ID hoặc None)
            p_name_raw = row.get(p_label_col, None)
            p_name = self._clean_label(p_name_raw)

            if not p_name:
                # Nếu không có tên đẹp, dùng ID làm tên hiển thị tạm, hoặc skip tùy bạn.
                # Ở đây tôi dùng ID làm tên để không mất node.
                p_name = str(p_id).split('/')[-1]

                # Tạo dict attributes cho Person
            person_attrs = {"name": p_name, "type": "Person"}

            # Thêm các thuộc tính bổ sung (dob, place...)
            for col_df, attr_name in attribute_map.items():
                if col_df in df.columns:
                    val = row[col_df]
                    if not pd.isna(val):
                        person_attrs[attr_name] = str(val)

            # Nếu người này có trong map sở thích, thêm vào attributes luôn
            if p_id in self.person_interests_map:
                # Chuyển set thành list để tương thích JSON/Gpickle tốt hơn
                person_attrs["interests"] = list(self.person_interests_map[p_id])
            else:
                person_attrs["interests"] = []

            # Add Node Person
            self.G.add_node(p_id, **person_attrs)

            # 2. Xử lý OBJECT (Node đích)
            obj_id = row[obj_id_col]
            obj_name_raw = row.get(obj_label_col, None)
            obj_name = self._clean_label(obj_name_raw)

            if not obj_name:
                obj_name = str(obj_id).split('/')[-1]

            # Add Node Object (Target)
            # Node đích thường ít thuộc tính hơn, chủ yếu là name và type
            self.G.add_node(obj_id, name=obj_name, type=target_node_type)

            # 3. Add Edge
            self.G.add_edge(p_id, obj_id, relationship=rel_label)
            count += 1

        print(f"  -> Đã thêm {count} cạnh '{rel_label}'.")

    def build_full_graph(self, config_list, interest_files_config=None):
        """
        Hàm chính:
        1. Tổng hợp interests (nếu có).
        2. Lặp qua config_list để xây dựng đồ thị chính.

        Input:
        - config_list: List các tuple ("filepath", "target_type", "label")
        - interest_files_config: List các tuple ("filepath", "object_prefix_in_query")
        """

        # BƯỚC 1: Xử lý sở thích trước (để có dữ liệu gán vào Node Person)
        if interest_files_config:
            self._aggregate_interests(interest_files_config)

        # BƯỚC 2: Xử lý các quan hệ chính (Vợ chồng, bạn bè, công việc...)
        print("\nBẮT ĐẦU XÂY DỰNG ĐỒ THỊ...")
        for path, target_type, rel_label in config_list:
            print(f"Đang xử lý file: {path} (Quan hệ: {rel_label})")

            df = self._load_and_flatten_json(path)

            if not df.empty:
                self._add_generic_relation(df, target_type, rel_label)
            else:
                print(f"  [WARN] File {path} rỗng hoặc lỗi.")

    def save_graph(self, output_path):
        print(f"Đang lưu đồ thị vào {output_path}...")
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(self.G, f, pickle.HIGHEST_PROTOCOL)
            print(f"Đã lưu thành công! (Nodes: {self.G.number_of_nodes()}, Edges: {self.G.number_of_edges()})")
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")

if __name__ == "__main__":
    transformer = GraphTransformer()
    # 1. Cấu hình file Sở thích (Interests)
    # Format: (đường_dẫn_file, tiền_tố_của_biến_object_trong_query)
    # Ví dụ query là: SELECT ?person ?interest ?interestLabel ... -> tiền tố là "interest" (để code tìm cột interestLabel.value)
    interest_configs = [
        ("data/raw_interests_music.json", "interest"),
        ("data/raw_interests_books.json", "book")
    ]
    # 2. Cấu hình file Quan hệ (Edges)
    # Format: (đường_dẫn_file, loại_node_đích, tên_quan_hệ)
    # Lưu ý: Trong query SPARQL của các file này, biến đích phải đặt là ?object và ?objectLabel
    relation_configs = [
        ("data/raw_data_spouse.json", "Person", "spouse"),  # Vợ/chồng
        ("data/raw_data_university.json", "University", "educated_at"),  # Trường học
        ("data/raw_data_party.json", "PoliticalParty", "member_of"),  # Đảng phái
    ]
    # 3. Chạy Pipeline
    transformer.build_full_graph(
        config_list=relation_configs,
        interest_files_config=interest_configs
    )
    # 4. Lưu
    transformer.save_graph("data/G_full.gpickle")