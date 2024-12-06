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
from typing import Dict, Any, Optional

from hugegraph_llm.config import huge_settings
from pyhugegraph.client import PyHugeClient


class SchemaManager:
    def __init__(self, graph_name: str):
        self.graph_name = graph_name
        self.client = PyHugeClient(
            huge_settings.graph_ip,
            huge_settings.graph_port,
            self.graph_name,
            huge_settings.graph_user,
            huge_settings.graph_pwd,
            huge_settings.graph_space,
        )
        self.schema = self.client.schema()

    def run(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if context is None:
            context = {}
        schema = self.schema.getSchema()
        if not schema["vertexlabels"] and not schema["edgelabels"]:
            raise Exception(f"Can not get {self.graph_name}'s schema from HugeGraph!")

        context.update({"schema": schema})
        return context
