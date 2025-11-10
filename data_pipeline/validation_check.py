import networkx as nx
import pickle
import random
from contextlib import redirect_stdout

from module_1_bfs import load_graph, get_person_id, find_path
def run_validation(graph, report):

    # Dùng "redirect_stdout" để TẤT CẢ lệnh print
    # đều tự động được ghi vào file txt.
    with open(report, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):

            print("--- BẮT ĐẦU BÁO CÁO VALIDATION ---")
            print(f"File đồ thị đang kiểm tra: {graph}\n")

            G =load_graph(graph)

            if G is None:
                print("--- KẾT THÚC BÁO CÁO (LỖI NGHIÊM TRỌNG) ---")
                return
            #Test thống kê
            print("--- 1. Thống kê Cơ bản ---")
            print(f"Tổng số Nút: {G.number_of_nodes()}")
            print(f"Tổng số Cạnh: {G.number_of_edges()}")
            if G.number_of_nodes() == 0:
                print("LỖI: Đồ thị rỗng.")
                return
            #Test thuộc tính
            print("\n--- 2. Kiểm tra Thuộc tính Node (ID & Tên) ---")

            null_id_count = 0
            null_name_count = 0

            # Kiểm tra xem 'None' có phải là 1 node không
            if None in G.nodes:
                null_id_count = 1

            for node_id, data in G.nodes(data=True):
                person_name = data.get('name')
                if person_name is None or person_name == "" or person_name.lower() == "none":
                    null_name_count += 1

            print(f"Kiểm tra ID bị null (None): {null_id_count} trường hợp.")
            if null_id_count > 0:
                print("-> FAILED: Có Node ID bị null. (Kiểm tra `person_id` và `spouse_id`)")

            print(f"Kiểm tra Tên (person_name) bị null/rỗng: {null_name_count} trường hợp.")
            if null_name_count > 0:
                print("-> FAILED: Có Node 'name' bị null. (Kiểm tra `personLabel` và `spouseLabel`)")

            print("\nKiểm tra mẫu Tên (lỗi font?):")
            for node_id, data in G.nodes(data=True):
                print(f"  - ID: {node_id}, Name: {data.get('name')}")

            # Test 3: Kiểm tra Cạnh (Relationship)
            print("\n--- 3. Kiểm tra Thuộc tính Cạnh (Relationship) ---")
            if G.number_of_edges() > 0:

                edge_labels = nx.get_edge_attributes(G, 'relationship')

                if not edge_labels:
                    print(
                        "FAILED: Không tìm thấy thuộc tính 'relationship' trên bất kỳ cạnh nào. (Báo Tân kiểm tra `G.add_edge`)")
                else:
                    all_relationships = list(edge_labels.values())

                    unique_relationships = set(all_relationships)

                    print(f"Đã tìm thấy {len(all_relationships)} nhãn cạnh.")
                    print(f"Các loại 'relationship' khác nhau được tạo ra ({len(unique_relationships)} loại):")
                    print(f"  {unique_relationships}")

                    if len(unique_relationships) == 0:
                        print("FAILED: Đồ thị có cạnh nhưng không có nhãn 'relationship'.")
                    else:
                        print("PASSED: Đã tìm thấy các loại 'relationship'.")
                    if G.number_of_edges() > 0:
                        edges = G.edges(data=True)
                        for u, v, data in edges:
                            if 'relationship' in data:

                                print(f"PASSED: Cạnh ({u}, {v}) có 'relationship' = {data['relationship']}")
                            else:
                                print(f"FAILED: Cạnh ({u}, {v}) BỊ THIẾU thuộc tính 'relationship'.")
                    else:
                        print("CẢNH BÁO: Không có cạnh nào để kiểm tra.")
            else:
                print("CẢNH BÁO: Không có cạnh nào để kiểm tra.")

            print("\n--- 4. Kiểm tra Logic Module 1 (BFS) ---")
            test_bfs(G,"Michelle Obama","Barack Obama")
            test_bfs(G,"Michelle Obama","Abraham Lincoln")

            print("\n--- KẾT THÚC BÁO CÁO VALIDATION ---")
def test_bfs(G,test_name_a,test_name_b):

    id_a_test = get_person_id(G, test_name_a)
    id_b_test = get_person_id(G, test_name_b)

    if id_a_test and id_b_test:
        print(f"Đang test tìm đường: {test_name_a} -> {test_name_b}")
        path_names, path_ids = find_path(G, test_name_a, test_name_b)
        print(f"Kết quả BFS: {" -> ".join(path_names) if isinstance(path_names, list) else path_names}")
        if isinstance(path_names, list) or isinstance(path_names, str):
            print("PASSED: Logic BFS hoạt động.")
        else:
            print("FAILED: Logic BFS thất bại.")
    else:
        print("FAILED: Không tìm thấy 2 tên test trong đồ thị.")




# --- Điểm bắt đầu chạy script ---
if __name__ == "__main__":
    GRAPH = "G_v0.1.gpickle"
    REPORT = "validation_v0.1.txt"

    run_validation(GRAPH, REPORT)

    print(f"Đã chạy xong validation. Mở file '{REPORT}' để xem kết quả.")