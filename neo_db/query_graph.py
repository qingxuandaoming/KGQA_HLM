# -*- coding: utf-8 -*-
import os
import json
import base64
from neo_db.config import graph, CA_LIST, similar_words
from kgqa.utils import get_profile

def query(name):
    """
    Query the graph for a person and their relationships.
    """
    # Parameterized query to prevent Cypher injection
    cypher = """
    MATCH (p)-[r]->(n:Person{Name:$name}) 
    RETURN p.Name, r.relation, n.Name, p.cate, n.cate
    UNION ALL
    MATCH (p:Person {Name:$name})-[r]->(n) 
    RETURN p.Name, r.relation, n.Name, p.cate, n.cate
    """
    data = graph.run(cypher, name=name)
    data = list(data)
    return get_json_data(data)

def get_json_data(data):
    """
    Format graph data into JSON for frontend visualization.
    """
    json_data = {'data': [], "links": []}
    d = []
    
    for i in data:
        d.append(i['p.Name'] + "_" + i['p.cate'])
        d.append(i['n.Name'] + "_" + i['n.cate'])
    
    # Remove duplicates
    d = list(set(d))
    
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")
        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        # Handle potential missing keys in CA_LIST
        data_item['category'] = CA_LIST.get(j_array[1], CA_LIST.get("其他"))
        json_data['data'].append(data_item)
    
    for i in data:
        link_item = {}
        link_item['source'] = name_dict[i['p.Name']]
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data

def get_KGQA_answer(array):
    data_array = []
    if not array:
        return [{'data': [], 'links': [], 'meta': {'message': '解析失败', 'candidates': []}}, '', '']
    current_name = array[0]
    for relation_name in array[1:]:
        if '|' in relation_name:
            parts = [r for r in relation_name.split('|') if r]
            for rn in parts:
                cypher = f"MATCH (p)-[r:{rn}{{relation: $relation_val}}]->(n:Person{{Name:$name}}) RETURN p.Name, n.Name, r.relation, p.cate, n.cate"
                data = graph.run(cypher, relation_val=rn, name=current_name)
                data = list(data)
                if not data:
                    continue
                data_array.extend(data)
            continue
        cypher = f"MATCH (p)-[r:{relation_name}{{relation: $relation_val}}]->(n:Person{{Name:$name}}) RETURN p.Name, n.Name, r.relation, p.cate, n.cate"
        data = graph.run(cypher, relation_val=relation_name, name=current_name)
        data = list(data)
        if not data:
            cand = []
            c2 = """
            MATCH (p)-[r]->(n:Person{Name:$name})
            RETURN DISTINCT r.relation AS rel, type(r) AS rel_type
            LIMIT 20
            """
            for row in graph.run(c2, name=current_name):
                cand.append(row['rel'] or row['rel_type'])
            return [{'data': [], 'links': [], 'meta': {'message': f"未找到‘{current_name} 的 {relation_name}’关系", 'candidates': cand}}, '', '']
        data_array.extend(data)
        current_name = data_array[-1]['p.Name']
    
    if not data_array:
        return [{'data': [], 'links': [], 'meta': {'message': '未找到路径', 'candidates': []}}, '', '']

    final_name = data_array[-1]['p.Name']
    
    # Read image
    image_path = os.path.join("static", "images", "characters", f"{final_name}.jpg")
    b = ""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image:
            base64_data = base64.b64encode(image.read())
            b = str(base64_data).split("'")[1]
    
    return [get_json_data(data_array), get_profile(str(final_name)), b]

def get_answer_profile(name):
    """
    Get profile and image for a specific character.
    """
    image_path = os.path.join("static", "images", "characters", f"{name}.jpg")
    b = ""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image:
            base64_data = base64.b64encode(image.read())
            b = str(base64_data).split("'")[1]
            
    return [get_profile(str(name)), b]
