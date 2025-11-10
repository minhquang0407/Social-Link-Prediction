class WikidataExtractor:
    def __init__(self, user_agent):
        # Khởi tạo SPARQLWrapper
        self.sparql = SPARQLWrapper(...) 
        self.sparql.setReturnFormat(JSON)

    def _run_paginated_query(self, base_query, output_filename):
        pass

    def fetch_all_relationships(self, relationship_queries, output_dir):
        pass
