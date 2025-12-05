import torch
from core.interfaces import ILinkPredictor
from torch_geometric.loader import NeighborLoader
from tqdm import tqdm


class Predictor(ILinkPredictor):
    """
    Lớp dùng để tính toán và cache vector nhúng (Z) của tất cả các node ('person'),
    sau đó thực hiện tìm kiếm node tương đồng (Link Prediction).
    """

    def compute_all_embeddings(self, model, data, device, batch_size=128):
        """
        Chạy model 1 lần để lấy vector của TẤT CẢ các node.
        Hàm này dùng để cache vector Z.
        """
        model.eval()

        # TODO: Khởi tạo NeighborLoader với tham số:
        #       - data: Dữ liệu đồ thị.
        #       - num_neighbors=[10, 5]: Lấy mẫu 10 neighbor hop 1 và 5 neighbor hop 2.
        #       - input_nodes=('person', None): Chỉ lấy mẫu các node 'person' làm node nguồn.
        #       - shuffle = false: vì dự đoán không cần trộn.

        all_embeddings = []

        with torch.no_grad():
            # TODO: Lặp qua loader để lấy từng batch.
            for batch in tqdm(loader, desc="Computing Embeddings"):
                pass
                # TODO: Di chuyển batch sang thiết bị (device).
                # TODO: Chạy mô hình (model) trên batch để lấy embeddings dictionary (z_dict).
                # TODO: Lấy kích thước thực tế của tập node nguồn ('person') trong batch.
                # TODO: Lấy embeddings Z của các node nguồn ('person') từ z_dict và giới hạn theo batch_size_actual.
                # TODO: Lưu trữ embeddings của batch hiện tại về CPU.

        # TODO: Nối tất cả các tensor embeddings đã thu thập lại thành một Tensor lớn.
        # TODO: Trả về bộ vector tất cả.
        return None

    def predict_top_k_similar(self, target_vec, all_vectors, top_k=5):
        """
        Tìm top K node có độ tương đồng cao nhất với target_vec từ all_vectors.
        Sử dụng k=top_k + 1 để loại bỏ node nguồn khỏi kết quả.
        """
        # TODO: Chuyển đầu vào (nếu chưa phải là Tensor) thành torch.Tensor.
        # TODO: Đảm bảo target_vec nằm trên cùng thiết bị với all_vectors.
        # TODO: Tính toán điểm tương đồng (scores) bằng phép nhân ma trận (Dot Product).
        # TODO: Tìm top K+1 điểm và chỉ số tương ứng.
        # TODO: Trả về top kết quả, và top chỉ số tương ứng.
        return None

    def predict_link_score(self, vec_a, vec_b) -> float:
        """
        Tính toán điểm liên kết (link score) giữa hai vector và chuyển thành xác suất.
        """
        # TODO: Chuyển đầu vào (nếu chưa phải là Tensor) thành torch.Tensor.
        # TODO: Tính toán điểm liên kết bằng Tích vô hướng (Dot Product).
        # TODO: Áp dụng hàm Sigmoid để chuyển score thành xác suất liên kết [0, 1].
        # TODO: Trả về xác suất liên kết đã tính.
        return None

