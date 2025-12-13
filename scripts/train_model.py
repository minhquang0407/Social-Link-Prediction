import sys
import os
import itertools
import json
import torch
import torch.nn.functional as F
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics import roc_auc_score

# PyG Imports
from torch_geometric.loader import LinkNeighborLoader
from torch_geometric.nn import to_hetero
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData

# Project Imports
from config.settings import (
    GRAPH_PATH, MODEL_PATH, PYG_DATA_PATH, MAPPING_PATH,
    CLEAN_DATA_PATH, TRAINING_HISTORY_PATH, BATCH_SIZE
)
from infrastructure.repositories.feature_repo import PyGDataRepository
from core.ai.gnn_architecture import GraphSAGE
from core.ai.data_processor import GraphDataProcessor


# --- 1. CÁC HÀM TIỆN ÍCH XỬ LÝ DATA ---

def sanitize_hetero_data(data):
    """
    Xóa các loại cạnh rỗng để tránh lỗi khi chạy Loader.
    """
    print("🧹 Đang dọn dẹp các loại cạnh rỗng...")
    # TODO 1: Duyệt qua data.edge_types.
    # Kiểm tra xem edge_index có tồn tại hoặc có rỗng không.
    # Nếu rỗng thì xóa loại cạnh đó khỏi data (dùng del data[et]).
    pass
    return data


def get_unified_edge_index(data, src_node_type='person', dst_node_type='person'):
    """
    Gộp tất cả các loại cạnh nối giữa Person-Person lại thành một 'Siêu cạnh'
    để làm nhãn huấn luyện (Supervision Target).
    """
    print(f"🔗 Đang tổng hợp các cạnh nối giữa '{src_node_type}' và '{dst_node_type}':")
    
    # TODO 2: Duyệt qua data.edge_types.
    # 1. Chỉ lấy cạnh nối src_node_type và dst_node_type.
    # 2. Bỏ qua các cạnh nghịch đảo (bắt đầu bằng 'rev_') để tránh trùng lặp.
    # 3. Thu thập edge_index vào một list.
    
    # TODO 3: Nối (Concat) tất cả edge_index lại theo chiều ngang (dim=1).
    # TODO 4: Lọc bỏ các cạnh trùng lặp (dùng torch.unique).
    
    # Return về super_edge_index
    return torch.empty(2, 0) # Placeholder


def get_or_prepare_data():
    """Tải và chuẩn bị dữ liệu (Undirected + Sanitize)."""
    feature_repo = PyGDataRepository(PYG_DATA_PATH, MAPPING_PATH)
    data, mapping = feature_repo.load_data()

    if data is None:
        print("⚠️ Chưa có dữ liệu PyG. Vui lòng chạy ETL trước!")
        return None

    # TODO 5: Thực hiện quy trình làm sạch và chuyển đổi đồ thị:
    # 1. Gọi sanitize_hetero_data lần 1.
    # 2. Chuyển đồ thị sang vô hướng (dùng T.ToUndirected()).
    # 3. Gọi sanitize_hetero_data lần 2 (để dọn rác do ToUndirected sinh ra).

    return data


# --- 2. CÁC HÀM TRAIN & EVAL ---

def train_epoch(model, loader, optimizer, device, target_edge_type):
    """Chạy 1 epoch huấn luyện."""
    model.train()
    total_loss = 0
    total_examples = 0

    for batch in tqdm(loader, desc="Training", leave=False):
        batch = batch.to(device)

        # TODO 6: Quan trọng - Ép kiểu dữ liệu (Data Type Casting)
        # Kiểm tra batch.x_dict, nếu là Float16 thì ép về Float32 để tránh lỗi matmul.

        optimizer.zero_grad()

        # TODO 7: Forward Pass
        # 1. Đưa dữ liệu qua model để lấy z_dict (embedding).
        # 2. Lấy edge_label_index và edge_label từ batch[target_edge_type].
        
        # TODO 8: Decode (Tính điểm tương đồng)
        # Lấy embedding của node nguồn và node đích, thực hiện Dot Product.

        # TODO 9: Tính Loss và Backprop
        # Dùng binary_cross_entropy_with_logits.
        # Gọi backward() và optimizer.step().

        # Cập nhật total_loss
        pass

    return total_loss / (total_examples + 1e-9)


@torch.no_grad()
def evaluate(model, loader, device, target_edge_type):
    """Đánh giá mô hình."""
    model.eval()
    preds = []
    ground_truths = []

    for batch in tqdm(loader, desc="Evaluating", leave=False):
        batch = batch.to(device)

        # TODO 10: Ép kiểu dữ liệu về Float32 (tương tự train_epoch).

        # TODO 11: Forward Pass và Decode
        # Tương tự train_epoch, nhưng KHÔNG tính loss, KHÔNG backprop.
        # Lưu ý: Kết quả output cần qua hàm .sigmoid() để về xác suất [0, 1].

        # Append kết quả vào preds và ground_truths
        pass

    # TODO 12: Tính ROC AUC Score dùng sklearn
    return 0.0 # Placeholder


# --- 3. CHIẾN LƯỢC CHẠY ---

def train_one_config(data, config, device, final_mode=False):
    """Huấn luyện với 1 cấu hình cụ thể."""
    hidden_dim = config['hidden_dim']
    lr = config['lr']
    epochs = config['epochs']

    # --- CHUẨN BỊ DỮ LIỆU ---
    # TODO 13: Gọi hàm get_unified_edge_index để tạo 'Siêu cạnh' cho việc training.
    target_edge_type = ('person', 'super_link', 'person')

    # TODO 14: Chia dữ liệu (Split Train/Val)
    # Nếu final_mode=True: Dùng toàn bộ siêu cạnh để train.
    # Nếu final_mode=False: Chia 80% train, 20% val (dùng torch.randperm).

    # TODO 15: Khởi tạo LinkNeighborLoader
    # - Train Loader: shuffle=True, neg_sampling_ratio=1.0
    # - Val Loader (nếu có): shuffle=False, neg_sampling_ratio=1.0
    # Lưu ý: edge_label_index trỏ vào phần data đã split ở trên.

    # --- KHỞI TẠO MODEL ---
    # TODO 16: Khởi tạo GraphSAGE và convert sang Hetero (to_hetero).
    # Input dim lấy từ data['person'].x.shape[1].
    model = None 
    optimizer = None

    history = {"epoch": [], "loss": [], "val_auc": []}
    best_val_auc = 0
    best_model_state = None

    print(f"\n🚀 Bắt đầu train (Hidden={hidden_dim}, LR={lr})...")

    # --- TRAINING LOOP ---
    for epoch in range(1, epochs + 1):
        # TODO 17: Gọi train_epoch
        loss = 0 # Placeholder
        
        # Log history
        history["epoch"].append(epoch)
        history["loss"].append(float(loss))

        log_msg = f"Epoch {epoch:03d} | Loss: {loss:.4f}"

        # TODO 18: Nếu có val_loader, gọi evaluate
        # Cập nhật best_val_auc và best_model_state nếu kết quả tốt hơn.
        
        print(log_msg)

    # Xử lý final mode
    if final_mode:
        best_model_state = model.state_dict() if model else None
        # Lưu history ra file JSON
        pass

    return best_val_auc, best_model_state


def run_grid_search():
    """Chạy Grid Search và Final Training."""
    data = get_or_prepare_data()
    if data is None: return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️ Running on: {device}")

    # Grid Search Configs
    param_grid = {
        'hidden_dim': [64, 128],
        'lr': [0.01],
        'epochs': [10]
    }
    
    # Tạo combinations từ param_grid
    keys, values = zip(*param_grid.items())
    combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

    best_auc = 0
    best_params = None

    # TODO 19: Grid Search Loop
    # Duyệt qua các config trong combinations.
    # Gọi train_one_config với final_mode=False.
    # So sánh và lưu lại config tốt nhất (best_auc).

    print(f"\n🥇 Best Params: {best_params} (AUC: {best_auc:.4f})")
    
    # TODO 20: Final Training
    # Cập nhật epochs lên cao hơn (ví dụ 50).
    # Gọi train_one_config với final_mode=True dùng best_params.
    # Lưu model (torch.save) vào MODEL_PATH.

if __name__ == "__main__":
    run_grid_search()
