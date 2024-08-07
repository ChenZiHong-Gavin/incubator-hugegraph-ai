# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import pickle as pkl
from copy import deepcopy
from typing import List, Dict, Any

import faiss
import numpy as np


class VectorIndex:
    """Comment"""
    def __init__(self, embed_dim: int):
        self.index = faiss.IndexFlatL2(embed_dim)
        self.properties = []

    @staticmethod
    def from_index_file(index_file: str, properties_file: str) -> "VectorIndex":
        faiss_index = faiss.read_index(index_file)
        embed_dim = faiss_index.d
        with open(properties_file, "rb") as f:
            properties = pkl.load(f)
        vector_index = VectorIndex(embed_dim)
        vector_index.index = faiss_index
        vector_index.properties = properties
        return vector_index

    def to_index_file(self, index_file: str, properties_file: str):
        faiss.write_index(self.index, index_file)
        with open(properties_file, "wb") as f:
            pkl.dump(self.properties, f)

    def add(self, vectors: List[List[float]], props: List[Any]):
        self.index.add(np.array(vectors))
        self.properties.extend(props)

    def search(self, query_vector: List[float], top_k: int) -> List[Dict[str, Any]]:
        _, indices = self.index.search(np.array([query_vector]), top_k)
        results = []
        for i in indices[0]:
            results.append(deepcopy(self.properties[i]))
        return results
