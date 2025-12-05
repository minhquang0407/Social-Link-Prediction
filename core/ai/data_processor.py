import torch
import numpy as np
from torch_geometric.data import HeteroData
from collections import defaultdict
from sentence_transformers import SentenceTransformer
import networkx as nx
from tqdm import tqdm


class GraphDataProcessor:
    """
    1. Tạo vector đặc trưng từ thuộc tính node.
    2. Chuyển đổi đồ thị NetworkX sang PyG HeteroData.
    """

    def __init__(self):
        print("CORE: Đang tải model Sentence-BERT...")
        # TODO: Khởi tạo SentenceTransformer với mô hình đã chọn ('paraphrase-multilingual-MiniLM-L12-v2').
        self.text_encoder = None

    def _create_node_features(self, G, node_list, ntype):
        """
        (Hàm nội bộ) Tạo ma trận đặc trưng cho một danh sách node cùng loại.
        """
        # TODO: Khởi tạo danh sách chứa các chuỗi văn bản (features) và năm sinh (nếu là 'person').
        feature_text_list = []
        years = []
        MIN_YEAR, MAX_YEAR = 1900, 2025  # Cấu hình chuẩn hóa năm sinh

        # TODO: Lặp qua node_list để thu thập thuộc tính.
        for node_id in node_list:
            node_data = G.nodes[node_id]

            # TODO: Trích xuất các thuộc tính văn bản (name, description, interests, birthplace, country).
            # TODO: Ghép các thuộc tính văn bản thành một chuỗi `full_text` duy nhất.
            # TODO: Thêm `full_text` vào `feature_text_list`.

            if ntype == 'person':
                # TODO: Lấy và chuyển đổi 'birthYear' thành số float, dùng try-except và gán giá trị mặc định.
                # TODO: Kẹp giá trị năm sinh giữa MIN_YEAR và MAX_YEAR.
                # TODO: Chuẩn hóa năm sinh về [0, 1] và thêm vào `years`.
                pass  # Logic xử lý năm sinh

        # TODO: Dùng self.text_encoder để encode `feature_text_list` thành tensor embedding.
        embeddings = None
        text_tensor = None

        if ntype == 'person':
            # TODO: Chuyển `years` thành tensor float, reshape thành cột (view(-1, 1)).
            # TODO: Nối (concatenate) `text_tensor` và `year_tensor` theo chiều ngang (dim=1) và trả về.
            return None
        else:
            # TODO: Trả về `text_tensor`.
            return None

    def process_graph_to_pyg(self, G):
        """
        Input: NetworkX Graph
        Output: (HeteroData, node_mapping, rev_node_mapping)
        """
        print("CORE: Bắt đầu chuyển đổi đồ thị sang HeteroData...")
        # TODO: Khởi tạo đối tượng PyG HeteroData.
        data = None

        ## 1. Xử lý Nodes & Features

        # TODO: Khởi tạo defaultdict để nhóm node ID theo 'type'.
        # TODO: Lặp qua G.nodes, lấy 'type' và thêm node ID vào `node_by_type`.
        # TODO: Khởi tạo node_mapping (String ID -> Int Index) và rev_node_mapping (Int Index -> String ID).
        node_mapping = {}
        rev_node_mapping = {}

        # TODO: Lặp qua từng loại node trong `node_by_type`.
        for ntype, node_list in node_by_type.items():
            # TODO: Tạo mapping/rev_mapping cho loại node hiện tại.
            # TODO: Gọi self._create_node_features để tạo đặc trưng `data[ntype].x`.
            # TODO: Gán số lượng node `data[ntype].num_nodes`.
            pass  # Logic xử lý node

        ## 2. Xử lý Edges

        # TODO: Khởi tạo defaultdict để lưu chỉ mục cạnh theo meta-path ((src_type, rel, dst_type) -> [[src_indices], [dst_indices]]).
        edges_dict = defaultdict(lambda: [[], []])
        # TODO: Khởi tạo danh sách chỉ mục cho quan hệ 'person'->'knows'->'person' (hai chiều).
        knows_src = []
        knows_dst = []

        # TODO: Lặp qua G.edges(data=True) với tqdm.
        for u, v, attr in tqdm(G.edges(data=True)):
            # TODO: Lấy loại node của nguồn (u) và đích (v) từ G.nodes.
            # TODO: Bỏ qua nếu loại node không xác định.
            # TODO: Lấy nhãn quan hệ, mặc định là 'related_to'.

            # TODO: Ánh xạ u, v String ID sang u_idx, v_idx Int Index bằng `node_mapping`.
            # TODO: Tạo `edge_key` (src_type, rel_label, dst_type).
            # TODO: Thêm u_idx, v_idx vào `edges_dict` tương ứng.

            # TODO: Nếu là 'person' -> 'person', thêm u_idx, v_idx vào `knows_src/dst`.
            pass  # Logic xử lý edge

        # TODO: Lặp qua `edges_dict` để tạo và gán `edge_index` cho PyG HeteroData.
        for (src_t, rel, dst_t), (src_list, dst_list) in edges_dict.items():
            # TODO: Tạo tensor `edge_index` cho cạnh thuận.
            # TODO: Gán `data[src_t, rel, dst_t].edge_index`.
            # TODO: Tạo cạnh ngược bằng cách đảo (flip) `edge_index` và gán `data[dst_t, f"rev_{rel}", src_t].edge_index`.
            pass  # Logic gán edge_index

        # TODO: Xử lý đặc biệt quan hệ 'knows' (person-person, hai chiều).
        if knows_src:
            # TODO: Tạo tensor cạnh thuận và nghịch cho 'knows'.
            # TODO: Nối (concatenate) hai tensor để tạo `final_edge_index`.
            # TODO: Gán `data['person', 'knows', 'person'].edge_index = final_edge_index`.
            pass  # Logic xử lý knows

        print("CORE: Chuyển đổi hoàn tất.")
        # TODO: Trả về data (HeteroData) và tuple mappings.
        return None