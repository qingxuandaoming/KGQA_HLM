# KGQA_HLM

基于知识图谱的《红楼梦》人物关系可视化与问答系统。

[![Project](https://img.shields.io/badge/project-KGQA_HLM-orange.svg)](https://github.com/chizhu/KGQA_HLM)
[![Python version](https://img.shields.io/badge/language-python3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Issues](https://img.shields.io/github/issues/chizhu/KGQA_HLM.svg)](https://github.com/chizhu/KGQA_HLM/issues)
[![License](https://img.shields.io/badge/lisence-MIT-pink.svg)](https://github.com/chizhu/KGQA_HLM)
[![License](https://img.shields.io/badge/lisence-Anti996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

~~更多信息参考历史站点：http://chizhunlp.com（现已不可用）~~

**概要**
- 使用 `Flask` 提供前端交互页面与接口。
- 使用 `Neo4j` + `py2neo` 构建与查询人物关系知识图谱。
- 使用 `jieba` 对中文问题进行分词、词性标注与实体识别，完成关系链推理问答。

**目录结构**

```text
KGQA_HLM/
├─ app.py                  # 项目入口（Flask）
├─ requirement.txt         # Python 依赖
├─ templates/              # 前端模板
│  ├─ index.html           # 欢迎页
│  ├─ search.html          # 人物关系搜索
│  ├─ all_relation.html    # 全关系展示
│  └─ KGQA.html            # 问答页面
├─ static/                 # 前端资源（CSS/JS/图片）
├─ raw_data/
│  └─ relation.txt         # 人物关系三元组
├─ neo_db/                 # 图谱构建与查询模块
│  ├─ config.py            # 图数据库连接配置
│  ├─ creat_graph.py       # 构建知识图谱
│  └─ query_graph.py       # 查询接口
├─ KGQA/
│  └─ ltp.py               # LTP 分词/词性/实体识别与问答预处理
└─ spider/                 # 人物资料与展示
   ├─ images/              # 人物图片
   └─ show_profile.py      # 资料展示
```

**环境要求**
- Python `3.10`（建议使用虚拟环境管理依赖）。
- Neo4j 图数据库（需启用 HTTP `http://localhost:7474`，建议 JDK21）。

**快速开始**

1. 创建并激活虚拟环境（Windows）：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -U pip
pip install -r requirement.txt
```

2. 配置 Neo4j 连接：编辑 `neo_db/config.py`，设置地址、用户名与密码，例如：

```python
graph = Graph(
    "http://localhost:7474",
    auth=("neo4j", "<your_password>")
)
```

3. 准备知识图谱数据并构建图谱（在项目根目录执行）：

```powershell
python neo_db/creat_graph.py
```

4. 启动 Web 服务：

```powershell
python app.py
```

浏览器访问 `http://127.0.0.1:5000/`。

**页面与接口**
- `GET /` 或 `/index`：欢迎页。
- `GET /search`：输入人物名，查看其关系网络与详情。
- `GET /KGQA`：基于关系链的自然语言问答。
- `GET /get_profile?character_name=人物名`：返回人物资料与头像。
- `GET /search_name?name=人物名`：返回人物的出入边关系数据。
- `GET /KGQA_answer?name=问题文本`：返回问答结果与路径。

**常见注意事项**
- 依赖文件名为 `requirement.txt`（非 `requirements.txt`）。
- 图谱构建脚本文件名为 `creat_graph.py`（非 `create_graph.py`）。
- 构建图谱时请在项目根目录执行，以便脚本正确定位 `raw_data/relation.txt`。
- 请确保 `spider/images/` 下存在对应人物图片，否则返回的 Base64 头像为空。

**系统流程图**

![流程](图片 1.png)

**界面示例**

![欢迎界面](1.png)
![界面](2.png)
![界面](3.png)
![界面](4.png)
![界面](5.png)
![界面](6.png)

**许可**
- MIT License；支持 Anti-996 许可倡议。
