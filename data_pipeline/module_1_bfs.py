import networkx as nx
import pickle

def load_graph(graph_path):
    print(f"Đang tải đồ thị từ {graph_path}.")

    try:
        with open(graph_path, "rb") as f:
            graph = pickle.load(f)
            print("Tải đồ thị thành công!")
            return graph
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {graph_path}.")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc file pickle: {e}.")
        return None


def get_person_id(graph,name):
    for node_id, data in graph.nodes(data=True):
        cur_name = data.get('name','').lower()
        if cur_name == name.lower():
            return node_id
    return None

def find_path(graph,name_a,name_b):
    id_a = get_person_id(graph,name_a)
    id_b = get_person_id(graph,name_b)
    if id_a == id_b: return "LỖI: Bạn đã nhập cùng một người."
    if id_a is None:
        return f"Không tìm thấy '{id_a}'.", None
    if id_b is None:
        return f"Không tìm thấy '{id_a}'.", None

    try:
        path_ids = nx.shortest_path(graph,source=id_a, target=id_b)
        path_names = [graph.nodes[id]['name'] for id in path_ids]
        return path_names, path_ids
    except nx.NetworkXNoPath:
        return f"Không tìm thấy liên kết giữa '{name_a}' và '{name_b}'.", None
    except Exception as e:
        return f"Lỗi không xác định:{e}", None


