# 2022 FIFA World Cup 数据集适配指南

## 概述

本文档记录了将原始GAT防守影响力评估代码适配到2022年FIFA世界杯数据集的完整过程和使用说明。

## 项目结构

```
项目根目录/
├── 2022WC_Notebooks_Test/          # ✓ 测试版本notebooks（按顺序编号）
│   ├── README.md                   # 使用说明
│   ├── 0_test_convert_tracking_final.ipynb
│   ├── 1_test_run_gat_model_final.ipynb
│   ├── 2_test_visualisation_final.ipynb
│   ├── 3_test_player_eval_final.ipynb
│   └── 4_test_experiments_final.ipynb
├── 2022WC_Notebooks_General/       # ✓ 通用版本notebooks（按顺序编号）
│   ├── README.md                   # 使用说明
│   ├── 0_ConvertTracking_2022WC.ipynb
│   ├── 1_RunGATModel_2022WC.ipynb
│   ├── 2_Visualisation_2022WC.ipynb
│   ├── 3_PlayerEval_2022WC.ipynb
│   └── 4_Experiments_2022WC.ipynb
├── convert_tracking.py              # ✓ 已适配 - 追踪数据转换（核心模块）
├── create_graph.py                  # ✓ 已适配 - 图构建（修复依赖）
├── scale_graph.py                   # ✓ 已适配 - 图特征缩放
├── player_eval.py                   # ⏳ 原始版本（待更新）
├── plot_functions.py                # ✓ 绘图辅助函数
├── requirements.txt                 # ✓ 已更新 - 完整依赖包列表
├── ADAPTATION_GUIDE_2022_WC.md     # ✓ 本文档
├── RunGATModel.ipynb               # ⏳ 原始版本（EPL数据）
├── Visualisation.ipynb             # ⏳ 原始版本（EPL数据）
├── Experiments.ipynb               # ⏳ 原始版本（EPL数据）
├── defensiveGATenv/                # ✓ 已创建 - 虚拟环境
├── GNNs/                           # ✓ 神经网络模型定义
├── Data/                           # 输出目录（处理后的CSV）
└── results/                        # 模型输出目录
```

### 📁 文件夹说明

#### 2022WC_Notebooks_Test/
- **用途**: 快速测试和学习
- **数据**: 固定使用2022世界杯决赛（阿根廷 vs 法国）
- **特点**:
  - 小规模训练（5 epochs）
  - 详细注释
  - 快速验证功能
- **运行顺序**: 0 → 1 → 2 → 3 → 4

#### 2022WC_Notebooks_General/
- **用途**: 实际研究和生产环境
- **数据**: 支持任意2022世界杯比赛
- **特点**:
  - 完整训练（10-40 epochs）
  - 支持批量处理
  - 生产级质量
- **运行顺序**: 0 → 1 → 2 → 3 → 4

## 数据集信息

### 原始数据集
- **来源**: English Premier League (EPL)
- **格式**: CSV格式的metadata和rosters

### 2022世界杯数据集
- **来源**: Gradient Sports Enhanced 2022 World Cup Dataset
- **位置**: `E:\JerryWu\Master\SoccerAnalytics\OpenData\TrackingData\Gradient Sports  Enhanced 2022 World Cup Dataset`
- **比赛数量**: 64场比赛
- **数据格式**: 
  - 追踪数据: `.jsonl.bz2` (压缩的JSONL格式)
  - 元数据: `.json` (每场比赛一个独立文件)
  - 阵容数据: `.json` (每场比赛一个独立文件)

## 环境设置

### 1. 创建虚拟环境
```bash
python -m venv defensiveGATenv
```

### 2. 激活虚拟环境
```bash
# Windows
defensiveGATenv\Scripts\activate.bat

# Linux/Mac
source defensiveGATenv/bin/activate
```

### 3. 安装依赖

**重要提示**: 如果遇到路径过长错误，请先参考"故障排除"部分的"问题0: Windows长路径限制"

```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 安装所有依赖
pip install -r requirements.txt
```

**已验证的依赖包版本**（2025-11-02测试通过）:
- pandas 1.3.5
- numpy 1.21.6
- networkx 2.6.3
- scipy 1.7.3
- matplotlib 3.5.3
- mplsoccer 1.1.12
- torch 1.13.1
- torch-geometric 2.3.1
- scikit-learn 1.0.2
- jupyter 1.1.1
- ipykernel 6.16.2
- ipywidgets 8.1.5

**验证安装**:
```bash
# 检查关键包是否已安装
pip list | findstr "torch mplsoccer pandas numpy networkx scipy matplotlib scikit-learn jupyter ipykernel"
```

## 已完成的适配

### 1. convert_tracking.py ✓

#### 主要修改
1. **数据路径配置**
   - 从CSV格式改为JSON格式
   - 配置2022世界杯数据集路径

2. **新增函数**
   - `load_game_metadata(game_id)`: 从JSON加载元数据
   - `load_game_roster(game_id)`: 从JSON加载阵容
   - `process_game(game_id)`: 处理完整比赛
   - `get_available_games()`: 获取可用比赛列表

3. **修改的函数**
   - `get_metadata()`: 适配JSON格式
   - `_extract_game_info_from_json()`: 从JSON提取信息
   - `_split_rosters_by_team_json()`: JSON格式阵容分割
   - `_create_roster_dictionaries_json()`: JSON格式字典创建

#### 使用方法

**方法1: 直接运行**
```bash
python convert_tracking.py
```

**方法2: 在代码中使用**
```python
from convert_tracking import process_game, get_available_games

# 获取所有比赛
games = get_available_games()

# 处理单场比赛
balls_df, events_df, players_df = process_game('3812')
```

**方法3: 批量处理**
```python
from convert_tracking import process_game, get_available_games

games = get_available_games()
for game_id in games:
    try:
        process_game(game_id, save_output=True)
        print(f"✓ {game_id} 完成")
    except Exception as e:
        print(f"✗ {game_id} 失败: {e}")
```

#### 输出数据
处理后的数据保存在 `Data/<game_id>/` 目录：
- `balls_<game_id>.csv`: 球的追踪数据
- `events_<game_id>.csv`: 比赛事件数据
- `players_<game_id>.csv`: 球员追踪数据

### 2. ConvertTracking_2022WC.ipynb ✓

#### 功能
通用版本的数据转换notebook，支持批量处理多场2022世界杯比赛

**基于**: 已验证可运行的 [`test_convert_tracking_final.py`](test_convert_tracking_final.py)

#### 主要特点
1. **灵活的比赛选择**
   - 支持单场比赛处理
   - 支持多场比赛批量处理
   - 支持处理所有可用比赛

2. **完整的处理流程**
   - 查看可用比赛列表
   - 加载比赛元数据和阵容
   - 处理追踪数据
   - 计算速度和加速度
   - 生成CSV文件
   - 数据验证和统计分析

3. **输出文件**
   - `Data/{game_id}/balls_{game_id}.csv` - 球追踪数据
   - `Data/{game_id}/events_{game_id}.csv` - 事件数据
   - `Data/{game_id}/players_{game_id}.csv` - 球员追踪数据

#### 使用方法

**步骤1: 启动Jupyter Notebook**
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook ConvertTracking_2022WC.ipynb
```

**步骤2: 配置要处理的比赛**
在第2个单元格中修改 `GAME_IDS` 变量：

```python
# 方式1: 处理单场比赛
GAME_IDS = ['10517']  # 决赛

# 方式2: 处理多场比赛
GAME_IDS = ['10517', '3857', '3859']

# 方式3: 处理所有可用比赛
GAME_IDS = ct.get_available_games()
```

**步骤3: 运行所有单元格**
依次运行每个单元格，或使用 "Run All" 功能

#### 处理内容
1. 导入必要的库
2. 配置参数
3. 查看可用比赛
4. 查看示例比赛元数据
5. 批量处理比赛数据
6. 验证输出文件
7. 数据统计分析

### 3. test_convert_tracking_final.ipynb ✓

#### 功能
专门用于2022世界杯决赛的数据转换测试版本

**基于**: 已验证可运行的 [`test_convert_tracking_final.py`](test_convert_tracking_final.py)

#### 主要特点
1. **固定使用决赛数据** (Game ID: 10517)
2. **详细的测试步骤** - 8个测试单元，每步都有说明
3. **适合快速验证** - 用于测试数据转换功能
4. **学习参考** - 包含详细注释和数据质量检查

#### 测试内容
1. 导入必要的库
2. 配置参数
3. 测试元数据加载
4. 处理追踪数据
5. 验证输出文件
6. 查看数据样本
7. 数据统计分析
8. 数据质量检查

#### 使用方法

**快速测试**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook test_convert_tracking_final.ipynb
```

然后在浏览器中依次运行所有单元格

#### 与ConvertTracking_2022WC.ipynb的区别

| 特性 | test_convert_tracking_final.ipynb | ConvertTracking_2022WC.ipynb |
|------|-----------------------------------|------------------------------|
| 用途 | 快速测试和验证 | 实际数据处理 |
| 比赛选择 | 固定（决赛） | 灵活（任意比赛） |
| 处理规模 | 单场比赛 | 支持批量处理 |
| 详细程度 | 详细注释和质量检查 | 简洁高效 |
| 适用场景 | 学习、测试、调试 | 生产环境、批量处理 |

## 已适配的文件

### 4. create_graph.py ✓

#### 主要修改
1. **移除硬编码依赖**
   - 删除了 `os.chdir('Data')`
   - 删除了 `rosters = pd.read_csv('rosters_updated.csv')`
   - 直接定义位置类型列表

2. **位置编码**
   - 使用2022世界杯标准位置类型: ['D', 'F', 'GK', 'M']
   - 不再依赖外部roster文件

#### 使用方法
```python
import create_graph as cg

# 创建标准化有向图
G = cg.create_normalized_graph_directed(
    players_df, balls_df, events_df, frameNum, home_team_name
)
```

### 5. RunGATModel_2022WC.ipynb ✓

#### 功能
通用版本的GAT模型训练notebook，支持任意2022世界杯比赛数据

#### 主要特点
1. **灵活的比赛选择**
   - 支持单场比赛分析
   - 支持多场比赛批量处理
   - 支持分析所有可用比赛

2. **完整的处理流程**
   - 数据加载和可视化
   - 批量图创建
   - 特征缩放
   - PyTorch Geometric数据转换
   - GAT和GNN模型训练
   - 模型预测和注意力分析
   - 模型和数据保存

3. **输出文件**
   - `results/model_reception_AT_2022WC.pth` - GAT模型
   - `results/model_reception_2022WC.pth` - 标准GNN模型
   - `results/graph_scaler_2022WC.pkl` - 特征缩放器
   - `results/scaled_graphs_2022WC.pkl` - 处理后的图数据

#### 使用方法

**步骤1: 启动Jupyter Notebook**
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook
```

**步骤2: 打开notebook**
在浏览器中打开 `RunGATModel_2022WC.ipynb`

**步骤3: 配置要分析的比赛**
在第2个单元格中修改 `GAME_IDS` 变量：

```python
# 方式1: 分析单场比赛（决赛）
GAME_IDS = ['10517']

# 方式2: 分析多场比赛
GAME_IDS = ['10517', '3857', '3859']  # 决赛、季军赛等

# 方式3: 分析所有可用比赛
GAME_IDS = ct.get_available_games()
```

**步骤4: 运行所有单元格**
依次运行每个单元格，或使用 "Run All" 功能

### 6. test_run_gat_model_final.ipynb ✓

#### 功能
专门用于2022世界杯决赛（阿根廷 vs 法国）的测试版本

#### 主要特点
1. **固定使用决赛数据** (Game ID: 10517)
2. **详细的测试步骤** - 11个测试单元，每步都有说明
3. **适合快速验证** - 用于测试功能是否正常工作
4. **学习参考** - 包含详细注释，适合学习使用

#### 测试内容
1. 导入必要的库
2. 配置参数
3. 加载元数据
4. 加载处理后的数据
5. 测试单个图的创建
6. 可视化球员位置（可选）
7. 可视化图结构（可选）
8. 创建多个图（前100个事件帧）
9. 图特征缩放
10. 转换为PyTorch Geometric格式
11. 训练GAT模型（小规模测试）
12. 测试模型预测

#### 使用方法

**快速测试**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook test_run_gat_model_final.ipynb
```

然后在浏览器中依次运行所有单元格

#### 与RunGATModel_2022WC.ipynb的区别

| 特性 | test_run_gat_model_final.ipynb | RunGATModel_2022WC.ipynb |
|------|-------------------------------|--------------------------|
| 用途 | 快速测试和验证 | 实际研究和分析 |
| 比赛选择 | 固定（决赛） | 灵活（任意比赛） |
| 训练规模 | 小规模（5 epochs） | 完整规模（10-40 epochs） |
| 详细程度 | 详细注释和说明 | 简洁高效 |
| 适用场景 | 学习、测试、调试 | 生产环境、研究分析 |

## 待适配的文件

### 7. RunGATModel.ipynb (原始版本) ⏳
**状态**: 已创建适配版本
- **RunGATModel_2022WC.ipynb** - 通用版本（推荐使用）
- **test_run_gat_model_final.ipynb** - 决赛测试版本

**原始文件说明**:
- 原始 `RunGATModel.ipynb` 是为EPL数据设计的
- 建议使用新创建的适配版本
- 如需更新原始文件，可参考 `RunGATModel_2022WC.ipynb` 的修改

### 8. Visualisation_2022WC.ipynb ✓

#### 功能
交互式可视化工具，用于分析GAT模型的预测结果和球员交互

#### 主要特点
1. **灵活的比赛选择** - 支持任意已处理的2022世界杯比赛
2. **交互式可视化** - 使用ipywidgets创建交互式控件
3. **多维度分析**
   - 防守球员影响力分析
   - 注意力权重可视化
   - 球员边连接显示
   - 接球概率预测
4. **实时更新** - 拖动球员位置实时查看影响变化

#### 主要修改
1. **数据加载适配**
   - 使用 [`ct.get_metadata()`](convert_tracking.py) 加载元数据
   - 从 `Data/{GAME_ID}/` 加载处理后的CSV文件
   - 支持动态比赛ID配置

2. **模型路径更新**
   - 使用 `results/model_final_{GAME_ID}.pth` 作为模型路径
   - 使用 `results/scaler_final_{GAME_ID}.pkl` 作为缩放器路径
   - 自动检测文件是否存在

3. **图数据处理**
   - 支持从预缩放文件加载或现场创建
   - 使用 [`cg.create_normalized_graph_directed()`](create_graph.py) 创建图
   - 使用 [`sg.GraphFeatureScaler`](scale_graph.py) 进行特征缩放

4. **可视化增强**
   - 使用 [`visualisation.create_simple_visualization()`](visualisation.py) 创建交互界面
   - 支持防守影响力分析
   - 支持注意力权重可视化
   - 支持球员拖动功能

#### 使用方法

**步骤1: 确保数据已处理**
```bash
# 如果还没有处理数据，先运行
python convert_tracking.py
```

**步骤2: 确保模型已训练**
```bash
# 启动Jupyter并运行以下任一notebook
jupyter notebook test_run_gat_model_final.ipynb
# 或
jupyter notebook RunGATModel_2022WC.ipynb
```

**步骤3: 启动可视化**
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook Visualisation_2022WC.ipynb
```

**步骤4: 配置比赛ID**
在第2个单元格中设置要分析的比赛：
```python
GAME_ID = '10517'  # 决赛: 阿根廷 vs 法国
# 或其他比赛ID
```

**步骤5: 运行所有单元格**
依次运行每个单元格，最后会显示交互式可视化界面

#### 交互式控件说明

1. **Graph Index** - 选择要查看的帧（滑块）
2. **Defender** - 选择要分析的防守球员（下拉菜单）
3. **Show Defender Influence** - 显示防守球员对进攻球员的影响（复选框）
4. **Show Defender Performances** - 显示所有防守球员的表现值（复选框）
5. **Player** - 选择要查看边连接的球员（下拉菜单）
6. **Show Player Edges** - 显示该球员到对方的连接（复选框）
7. **Show Attention Weights** - 显示注意力权重，线条粗细表示权重大小（复选框）

#### 颜色说明
- **红色**: 进攻球员
- **蓝色**: 防守球员
- **绿色**: 被选中的防守球员
- **黑色**: 球

#### 输出示例
- 接球概率预测表格
- 注意力权重分析
- 交互式球场可视化
- 防守影响力指标

#### 与原始版本的区别

| 特性 | Visualisation.ipynb | Visualisation_2022WC.ipynb |
|------|---------------------|----------------------------|
| 数据源 | EPL数据 | 2022世界杯数据 |
| 数据加载 | 硬编码路径 | 动态路径配置 |
| 比赛选择 | 固定 | 灵活可配置 |
| 元数据加载 | CSV文件 | JSON文件（通过ct.get_metadata） |
| 模型路径 | 固定路径 | 基于比赛ID的动态路径 |
| 文档 | 英文 | 中文，详细说明 |
| 错误处理 | 基本 | 完善的文件检查和提示 |

### 9. test_visualisation_final.ipynb ✓

#### 功能
专门用于2022世界杯决赛的可视化测试版本

#### 主要特点
1. **固定使用决赛数据** (Game ID: 10517)
2. **快速测试** - 只创建前100个图（可调整）
3. **详细的测试步骤** - 10个测试单元，每步都有说明
4. **适合学习和验证** - 包含详细注释和使用提示
5. **完整的可视化流程**
   - 数据加载
   - 图创建和缩放
   - 模型加载
   - 接球概率预测测试
   - 图可视化
   - 交互式可视化工具

#### 使用方法

**快速测试**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook test_visualisation_final.ipynb
```

然后在浏览器中依次运行所有单元格

#### 测试内容

1. 导入库
2. 配置参数（决赛数据）
3. 加载xT网格和元数据
4. 加载处理后的数据
5. 创建图数据集（前100个）
6. 图特征缩放
7. 加载训练好的模型
8. 测试接球概率预测
9. 可视化示例图
10. 启动交互式可视化

#### 与Visualisation_2022WC.ipynb的区别

| 特性 | test_visualisation_final.ipynb | Visualisation_2022WC.ipynb |
|------|-------------------------------|----------------------------|
| 用途 | 快速测试和学习 | 实际研究和分析 |
| 比赛选择 | 固定（决赛） | 灵活（任意比赛） |
| 图数量 | 限制（100个） | 完整（所有事件） |
| 详细程度 | 详细注释和说明 | 简洁高效 |
| 适用场景 | 学习、测试、演示 | 生产环境、深入分析 |

### 10. Visualisation.ipynb (原始版本) ⏳
**状态**: 已创建适配版本
- **Visualisation_2022WC.ipynb** - 2022世界杯通用版本（推荐使用）
- **test_visualisation_final.ipynb** - 决赛测试版本（快速验证）

**原始文件说明**:
- 原始 `Visualisation.ipynb` 是为EPL数据设计的
- 建议使用新创建的适配版本
- 如需更新原始文件，可参考适配版本的修改

### 11. PlayerEval_2022WC.ipynb ✓

#### 功能
通用版本的球员评估notebook，支持任意2022世界杯比赛数据

#### 主要特点
1. **灵活的比赛选择**
   - 支持单场比赛分析
   - 支持分析任何已处理的比赛
   - 可配置的分析参数

2. **完整的评估流程**
   - 防守球员影响力计算
   - 注意力权重分析
   - 距离和威胁值评估
   - 综合表现评分

3. **输出文件**
   - `results/player_eval_{GAME_ID}/{GAME_ID}_defender_performance.csv` - 详细表现数据
   - `results/player_eval_{GAME_ID}/{GAME_ID}_analysis.png` - 可视化分析图表

#### 使用方法

**步骤1: 启动Jupyter Notebook**
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook PlayerEval_2022WC.ipynb
```

**步骤2: 配置要分析的比赛**
在第2个单元格中修改 `GAME_ID` 变量：

```python
# 方式1: 分析决赛
GAME_ID = '10517'

# 方式2: 分析其他比赛
GAME_ID = '3857'  # 季军赛
```

**步骤3: 运行所有单元格**
依次运行每个单元格，或使用 "Run All" 功能

#### 分析内容
1. 导入库和配置参数
2. 加载比赛数据和元数据
3. 创建球队阵容DataFrame
4. 加载或创建缩放后的图
5. 加载训练好的模型
6. 定义分析函数
7. 批量分析所有图
8. 保存结果到CSV
9. 统计分析和排名
10. 可视化分析（可选）

### 12. test_player_eval_final.ipynb ✓

#### 功能
专门用于2022世界杯决赛的球员评估测试版本

#### 主要特点
1. **固定使用决赛数据** (Game ID: 10517)
2. **快速测试** - 只分析前50个图（可调整）
3. **详细的测试步骤** - 9个测试单元，每步都有说明
4. **适合学习和验证** - 包含详细注释和使用提示

#### 测试内容
1. 导入必要的库
2. 配置参数（决赛数据）
3. 加载数据和元数据
4. 加载图和模型
5. 定义分析函数
6. 单图测试
7. 批量分析
8. 保存结果
9. 结果分析

#### 使用方法

**快速测试**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook test_player_eval_final.ipynb
```

然后在浏览器中依次运行所有单元格

#### 与PlayerEval_2022WC.ipynb的区别

| 特性 | test_player_eval_final.ipynb | PlayerEval_2022WC.ipynb |
|------|------------------------------|-------------------------|
| 用途 | 快速测试和验证 | 实际研究和分析 |
| 比赛选择 | 固定（决赛） | 灵活（任意比赛） |
| 分析规模 | 限制（前50个图） | 完整（所有图） |
| 详细程度 | 详细注释和说明 | 简洁高效 |
| 适用场景 | 学习、测试、调试 | 生产环境、研究分析 |
| 可视化 | 基本统计 | 完整可视化图表 |

### 13. player_eval.py (原始版本) ⏳
**状态**: 已创建适配版本
- **PlayerEval_2022WC.ipynb** - 通用版本（推荐使用）
- **test_player_eval_final.ipynb** - 决赛测试版本

**原始文件说明**:
- 原始 `player_eval.py` 是为EPL数据设计的
- 建议使用新创建的notebook版本
- 如需更新原始文件，可参考notebook的修改

### 14. Experiments_2022WC.ipynb ✓

#### 功能
通用版本的实验分析notebook，用于探索性分析2022世界杯比赛中的防守表现数据

#### 主要特点
1. **灵活的比赛选择**
   - 支持单场比赛分析
   - 支持多场比赛批量分析
   - 支持分析所有可用比赛

2. **完整的分析流程**
   - 数据加载与合并
   - 网格/区域分析
   - 防守组合分析
   - 球员排名
   - 统计分析和相关性分析
   - 可视化分析

3. **输出文件**
   - `results/experiments_2022WC/results_model_df.csv` - 完整数据
   - `results/experiments_2022WC/results_model_df_unique.csv` - 唯一记录
   - `results/experiments_2022WC/defender_rankings.csv` - 球员排名
   - `results/experiments_2022WC/cb_duo_rankings.csv` - 中后卫组合排名
   - 各类可视化图表

#### 使用方法

**步骤1: 启动Jupyter Notebook**
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook Experiments_2022WC.ipynb
```

**步骤2: 配置要分析的比赛**
在第2个单元格中修改 `GAME_IDS` 变量：

```python
# 方式1: 分析单场比赛
GAME_IDS = ['10517']  # 决赛

# 方式2: 分析多场比赛
GAME_IDS = ['10517', '3857', '3859']

# 方式3: 分析所有可用比赛
GAME_IDS = ct.get_available_games()
```

**步骤3: 运行所有单元格**
依次运行每个单元格，或使用 "Run All" 功能

#### 分析内容
1. 导入库和配置
2. 创建球员位置映射
3. 加载球员评估结果
4. 数据预处理
5. 保存合并后的数据
6. 防守球员表现排名
7. 按位置分析
8. 防守组合分析
9. 相关性分析
10. 散点图分析

### 15. test_experiments_final.ipynb ✓

#### 功能
专门用于2022世界杯决赛的实验分析测试版本

#### 主要特点
1. **固定使用决赛数据** (Game ID: 10517)
2. **详细的测试步骤** - 13个测试单元，每步都有说明
3. **适合学习和验证** - 包含详细注释和使用提示
4. **完整的分析流程**
   - 数据加载和基本统计
   - 网格/区域分析
   - 防守组合分析
   - 球员表现评估
   - 统计分析和可视化

#### 测试内容
1. 导入库和配置
2. 配置参数（决赛数据）
3. 加载元数据和比赛数据
4. 创建球员位置映射
5. 加载球员评估结果
6. 加载事件数据
7. 基本统计分析
8. 网格区域分析
9. 防守球员表现排名
10. 按位置分析
11. 防守组合分析（中后卫配对）
12. 距离与影响力关系分析
13. xT网格分析（可选）

#### 使用方法

**快速测试**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 启动Jupyter
jupyter notebook test_experiments_final.ipynb
```

然后在浏览器中依次运行所有单元格

#### 与Experiments_2022WC.ipynb的区别

| 特性 | test_experiments_final.ipynb | Experiments_2022WC.ipynb |
|------|------------------------------|--------------------------|
| 用途 | 快速测试和学习 | 实际研究和分析 |
| 比赛选择 | 固定（决赛） | 灵活（任意比赛） |
| 分析深度 | 基础分析 | 完整分析 |
| 详细程度 | 详细注释和说明 | 简洁高效 |
| 适用场景 | 学习、测试、演示 | 生产环境、深入研究 |

### 16. Experiments.ipynb (原始版本) ⏳
**状态**: 已创建适配版本
- **Experiments_2022WC.ipynb** - 2022世界杯通用版本（推荐使用）
- **test_experiments_final.ipynb** - 决赛测试版本（快速验证）

**原始文件说明**:
- 原始 `Experiments.ipynb` 是为EPL数据设计的
- 建议使用新创建的适配版本
- 如需更新原始文件，可参考适配版本的修改

## 常见问题和解决方案

### 问题1: GraphFeatureScaler没有inverse_transform方法
**错误信息**: `AttributeError: 'GraphFeatureScaler' object has no attribute 'inverse_transform'`

**原因**: `GraphFeatureScaler`使用`StandardScaler`，需要通过`position_scaler.inverse_transform()`访问

**解决方案**:
```python
# 错误的写法
x, y = scaler.inverse_transform([[features[0], features[1]]])[0]

# 正确的写法
if hasattr(scaler, 'position_scaler'):
    x, y = scaler.position_scaler.inverse_transform([[features[0], features[1]]])[0]
else:
    x, y = scaler.inverse_transform([[features[0], features[1]]])[0]
```

### 问题2: mask_node_name参数类型错误
**错误信息**: `ValueError: ['Player Name'] is not in list`

**原因**: 模型的forward方法期望`mask_node_name`是字符串，但传递了列表

**解决方案**:
```python
# 错误的写法
probs, _ = model(..., mask_node_name=[defender], ...)

# 正确的写法
probs, _ = model(..., mask_node_name=defender, ...)
```

### 问题3: xT网格索引越界
**错误信息**: `IndexError: single positional indexer is out-of-bounds`

**原因**: `get_pitch_value`函数中行列索引顺序错误

**解决方案**:
```python
# 错误的写法
return data.iloc[col_index, row_index]

# 正确的写法
return data.iloc[row_index, col_index]
```

## 数据格式说明

### 坐标系统
- 标准球场尺寸: 105m × 68m
- X轴调整: +52.5米
- Y轴调整: +34米
- 原点位于球场中心

### 时间信息
- 采样率: 29.97 fps
- `frameNum`: 帧编号
- `period`: 比赛阶段（1=上半场，2=下半场）
- `periodElapsedTime`: 阶段内经过的时间（秒）

### 球员数据
- `playerName`: 球员昵称
- `jerseyNum`: 球衣号码
- `playerPos`: 位置类型（GK, D, M, F）
- `x, y`: 球员坐标
- `velocity_*`: 速度分量
- `acceleration_*`: 加速度分量

### 事件数据
- `eventType`: 事件类型
- `possessionEventType`: 控球事件类型
- `possession_sequence`: 控球序列编号

## 示例比赛

### 小组赛
- `3812`: 塞内加尔 vs 荷兰
- `3813`: 英格兰 vs 伊朗
- `3814`: 美国 vs 威尔士

### 淘汰赛
- `3857`: 克罗地亚 vs 摩洛哥 (季军赛)
- `3859`: 阿根廷 vs 法国 (决赛)

## 适配流程

对于每个待适配的文件，建议按以下步骤进行：

1. **分析原始代码**
   - 识别数据加载部分
   - 识别依赖CSV格式的代码
   - 识别硬编码的路径

2. **修改数据加载**
   - 使用 `convert_tracking.py` 中的函数
   - 或直接从 `Data/<game_id>/` 加载处理后的CSV

3. **测试验证**
   - 使用示例比赛测试
   - 验证输出结果
   - 检查可视化效果

4. **文档更新**
   - 在本文档中记录修改
   - 更新使用说明

### 问题0: Windows长路径限制导致ipykernel安装失败
**错误信息**:
- "This error might have occurred since this system does not have Windows Long Path support enabled"
- `[Errno 2] No such file or directory`

**原因**: Windows默认路径长度限制为260字符，项目路径过长导致安装失败

**解决方案**:
1. **启用Windows长路径支持**（需要管理员权限）
   ```bash
   # 方法1: 使用注册表文件（推荐）
   # 双击项目根目录下的 enable_long_paths.reg 文件
   # 或手动创建该文件，内容如下：
   ```
   
   ```reg
   Windows Registry Editor Version 5.00
   [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem]
   "LongPathsEnabled"=dword:00000001
   ```
   
   ```bash
   # 方法2: 使用PowerShell（需要管理员权限）
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

2. **重启计算机**（必须！注册表修改需要重启才能生效）

3. **安装依赖包**
   ```bash
   # 激活虚拟环境
   defensiveGATenv\Scripts\activate
   
   # 安装所有依赖
   pip install -r requirements.txt
   ```

4. **在VS Code中配置kernel**
   - 重新加载窗口（Ctrl+Shift+P -> "Reload Window"）
   - 打开notebook
   - 点击右上角选择kernel
   - 选择 "defensiveGATenv (Python 3.7.9)"

**替代方案**（如果不想修改注册表）:
- 将项目移动到路径较短的位置，如 `C:\Projects\GAT\`
- 或使用符号链接: `mklink /D "C:\GAT" "<长路径>"` (需要管理员权限)

### 问题0.1: 缺少mplsoccer模块
**错误信息**: "ModuleNotFoundError: No module named 'mplsoccer'"

**解决方案**:
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 安装所有依赖（包括mplsoccer）
pip install -r requirements.txt
```

**验证安装**:
```bash
# 检查已安装的关键包
pip list | findstr "torch mplsoccer pandas numpy networkx scipy matplotlib scikit-learn jupyter ipykernel"
```

预期输出应包含：
- ipykernel 6.16.2
- jupyter 1.1.1
- matplotlib 3.5.3
- mplsoccer 1.1.12
- networkx 2.6.3
- numpy 1.21.6
- pandas 1.3.5
- scikit-learn 1.0.2
- scipy 1.7.3
- torch 1.13.1
- torch-geometric 2.3.1

## 故障排除

### 问题1: Jupyter Notebook中无法导入项目模块
**错误信息**: `ModuleNotFoundError: No module named 'convert_tracking'`

**原因**:
- Notebook文件位于子目录（如`2022WC_Notebooks_Test/`）中
- Python无法找到父目录中的项目模块
- `sys.path`中没有包含项目根目录

**解决方案**:
在notebook的第一个代码单元格中，导入模块之前添加以下代码：

```python
import sys
import os

# 添加父目录到Python路径（用于导入项目模块）
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    print(f"✓ 已添加父目录到Python路径: {parent_dir}")

# 然后再导入项目模块
import convert_tracking as ct
import plot_functions as pf
# ... 其他导入
```

**已修复的文件**:
- ✓ `2022WC_Notebooks_Test/0_test_convert_tracking_final.ipynb`
- ✓ `2022WC_Notebooks_Test/1_test_run_gat_model_final.ipynb`
- ✓ `2022WC_Notebooks_Test/2_test_visualisation_final.ipynb`
- ✓ `2022WC_Notebooks_Test/3_test_player_eval_final.ipynb`
- ✓ `2022WC_Notebooks_Test/4_test_experiments_final.ipynb`

**注意**:
- 通用版本notebooks（`2022WC_Notebooks_General/`）位于项目根目录，不需要此修复
- 如果创建新的子目录notebook，记得添加路径修复代码

### 问题2: 找不到数据文件
**解决方案**:
- 检查数据集路径是否正确
- 确认比赛ID存在
- 检查文件权限

### 问题3: 内存不足
**解决方案**:
- 一次只处理一场比赛
- 关闭其他程序
- 增加虚拟内存

### 问题4: 处理速度慢
**解决方案**:
- 正常现象，每场比赛需要几分钟
- 可以使用多进程并行处理
- 考虑使用更快的存储设备

### 问题5: 依赖包冲突
**解决方案**:
- 使用虚拟环境隔离
- 检查Python版本兼容性
- 更新requirements.txt

## 开发计划

- [x] 适配 convert_tracking.py
- [x] 修复 create_graph.py 依赖问题
- [x] 创建 RunGATModel_2022WC.ipynb（通用版本）
- [x] 创建 test_run_gat_model_final.ipynb（决赛测试版本）
- [x] 更新 requirements.txt（完整依赖列表）
- [x] 完成核心功能验证
- [x] 解决Windows长路径限制问题
- [x] 完成依赖包安装和验证
- [x] 适配 Visualisation.ipynb（创建Visualisation_2022WC.ipynb和test_visualisation_final.ipynb）
- [x] 创建 ConvertTracking_2022WC.ipynb（数据转换通用版本）
- [x] 创建 test_convert_tracking_final.ipynb（数据转换决赛测试版本）
- [x] 适配 player_eval.py（创建PlayerEval_2022WC.ipynb和test_player_eval_final.ipynb）
- [x] 适配 Experiments.ipynb（创建Experiments_2022WC.ipynb和test_experiments_final.ipynb）
- [ ] 完成所有测试notebook的完整测试
- [ ] 性能优化
- [ ] 文档完善

## 版本历史

### v0.1 (2025-10-31)
- ✓ 完成 convert_tracking.py 适配
- ✓ 创建虚拟环境
- ✓ 创建初始requirements.txt
- ✓ 创建适配指南文档

### v0.2 (2025-11-01)
- ✓ 修复 create_graph.py 依赖问题
- ✓ 创建 RunGATModel_2022WC.ipynb（通用版本）
- ✓ 创建 test_run_gat_model_final.ipynb（决赛测试版本）
- ✓ 更新 requirements.txt（添加完整依赖）
- ✓ 完成核心功能验证
- ✓ 更新适配指南文档

### v0.3 (2025-11-02 上午)
- ✓ 解决Windows长路径限制问题
- ✓ 成功安装ipykernel和所有依赖包
- ✓ 验证所有关键包版本
- ✓ 更新故障排除文档
- ✓ 添加详细的安装验证步骤

### v0.4 (2025-11-02 下午)
- ✓ 适配 Visualisation.ipynb
- ✓ 创建 Visualisation_2022WC.ipynb（可视化通用版本）
- ✓ 创建 test_visualisation_final.ipynb（可视化决赛测试版本）
- ✓ 创建 ConvertTracking_2022WC.ipynb（数据转换通用版本）
- ✓ 创建 test_convert_tracking_final.ipynb（数据转换决赛测试版本）
- ✓ 添加交互式可视化功能说明
- ✓ 完善使用文档和示例
- ✓ 更新适配指南

### v0.5 (2025-11-02 晚上)
- ✓ 适配 player_eval.py
- ✓ 创建 PlayerEval_2022WC.ipynb（球员评估通用版本）
- ✓ 创建 test_player_eval_final.ipynb（球员评估决赛测试版本）
- ✓ 实现防守球员影响力分析功能
- ✓ 添加批量分析和结果导出
- ✓ 添加可视化分析图表
- ✓ 更新适配指南文档

### v0.6 (2025-11-02 深夜)
- ✓ 适配 Experiments.ipynb
- ✓ 创建 Experiments_2022WC.ipynb（实验分析通用版本）
- ✓ 创建 test_experiments_final.ipynb（实验分析决赛测试版本）
- ✓ 实现数据合并和统计分析功能
- ✓ 添加网格区域分析
- ✓ 添加防守组合分析
- ✓ 添加相关性分析和可视化
- ✓ 更新适配指南文档

### v0.7 (2025-11-28)
- ✓ 修复所有测试notebook的模块导入问题
- ✓ 添加Python路径修复代码到所有子目录notebooks
- ✓ 更新故障排除文档（问题1: Jupyter Notebook中无法导入项目模块）
- ✓ 验证修复方案适用于所有5个测试notebooks
- ✓ 更新适配指南文档

### 待发布
- 完成所有测试notebook的完整测试
- 完整测试
- 性能优化

## 参考资料

- 原始论文: "Evaluating Defensive Influence in Multi-Agent Systems Using Graph Attention Networks"
- 数据提供商: Gradient Sports (https://www.gradientsports.com/)
- 原始代码仓库: [[GitHub链接](https://github.com/GregSoton/EvaluatingDefensiveInfluenceUsingGATs)]

## 联系方式

如有问题或建议，请联系项目维护者。

---
**最后更新**: 2025年11月2日 深夜
**适配状态**: 基本完成 (12/12 完成)

**核心功能**: ✓ 已完成并验证
**环境配置**: ✓ 已完成（包括Windows长路径支持）
**依赖安装**: ✓ 已完成并验证
**数据转换工具**: ✓ 已完成（ConvertTracking_2022WC.ipynb, test_convert_tracking_final.ipynb）
**模型训练工具**: ✓ 已完成（RunGATModel_2022WC.ipynb, test_run_gat_model_final.ipynb）
**可视化工具**: ✓ 已完成（Visualisation_2022WC.ipynb, test_visualisation_final.ipynb）
**球员评估工具**: ✓ 已完成（PlayerEval_2022WC.ipynb, test_player_eval_final.ipynb）
**实验分析工具**: ✓ 已完成（Experiments_2022WC.ipynb, test_experiments_final.ipynb）
**待完成**: 完整测试验证