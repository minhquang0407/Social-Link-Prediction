import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql" #đường dẫn dến wikidata


def run_simple_query(query):

    #Khởi tạo, kết nối đến endpoint
    sparql = SPARQLWrapper(WIKIDATA_ENDPOINT)

    #Gán query
    sparql.setQuery(query)

    #Set returnFormat JSON
    sparql.setReturnFormat(JSON)

    try:
        print("Đang thực thi truy vấn SPARQL...")
        #Thực thi và chuyển đổi kết quả
        results = sparql.query().convert()
        print("Truy vấn thành công.")
        #Trả về kết quả đã parse (dạng dictionary)
        return results
    except Exception as e:
        print(f"Lỗi khi thực thi truy vấn: {e}", file=sys.stderr)
        print(f"Chi tiết: {e.args}", file=sys.stderr)
        return None  #Trả về None nếu có lỗi


def get_v0_1_data_spouse():

    query = """
    SELECT ?person ?personLabel ?spouse ?spouseLabel
    WHERE 
    {
        ?person wdt:P26 ?spouse.

        # Lấy nhãn (tên) của ?person và ?spouse
        SERVICE wikibase:label { 
            bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,vi". 
        }
    }
    LIMIT 100
    """

    print("Bắt đầu lấy dữ liệu vợ/chồng...")
    #Gọi run_simple_query
    raw_data = run_simple_query(query)

    #Lưu file raw_data_v0.1_spouse.json
    if raw_data:
        output_filename = "raw_data_v0.1_spouse.json"
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                # Dùng json.dump để lưu dict vào file
                # ensure_ascii=False để lưu đúng tiếng Việt
                # indent=4 để file JSON đẹp, dễ đọc
                json.dump(raw_data, f, ensure_ascii=False, indent=4)
            print(f"Đã lưu dữ liệu thành công vào file: {output_filename}")
        except IOError as e:
            print(f"Lỗi khi lưu file: {e}", file=sys.stderr)
    else:
        print("Không nhận được dữ liệu, sẽ không lưu file.")


if __name__ == "__main__":
    get_v0_1_data_spouse()