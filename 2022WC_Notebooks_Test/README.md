# 2022世界杯决赛测试版Notebooks

本文件夹包含用于快速测试和验证的notebook，所有notebook都固定使用2022世界杯决赛数据（阿根廷 vs 法国，Game ID: 10517）。

## 📋 运行顺序

请按照以下顺序依次运行notebook：

### 0️⃣ 数据转换
**文件**: `0_test_convert_tracking_final.ipynb`
- **功能**: 将原始追踪数据转换为可用的CSV格式
- **输出**: `Data/10517/` 目录下的三个CSV文件
- **运行时间**: 约2-5分钟

### 1️⃣ 模型训练
**文件**: `1_test_run_gat_model_final.ipynb`
- **功能**: 训练GAT模型（小规模测试，5 epochs）
- **依赖**: 需要先运行步骤0
- **输出**: 
  - `results/model_final_10517.pth` - 训练好的模型
  - `results/scaler_final_10517.pkl` - 特征缩放器
  - `results/scaled_graphs_final_10517.pkl` - 缩放后的图数据
- **运行时间**: 约5-10分钟

### 2️⃣ 可视化分析
**文件**: `2_test_visualisation_final.ipynb`
- **功能**: 交互式可视化工具，分析模型预测和球员交互
- **依赖**: 需要先运行步骤0和1
- **输出**: 交互式可视化界面
- **运行时间**: 约2-3分钟

### 3️⃣ 球员评估
**文件**: `3_test_player_eval_final.ipynb`
- **功能**: 评估防守球员的影响力（前50个图）
- **依赖**: 需要先运行步骤0和1
- **输出**: `results/player_eval_10517/10517_defender_performance.csv`
- **运行时间**: 约3-5分钟

### 4️⃣ 实验分析
**文件**: `4_test_experiments_final.ipynb`
- **功能**: 探索性数据分析和统计分析
- **依赖**: 需要先运行步骤0、1和3
- **输出**: 各类统计图表和分析结果
- **运行时间**: 约1-2分钟

## 🚀 快速开始

```bash
# 1. 激活虚拟环境
defensiveGATenv\Scripts\activate

# 2. 启动Jupyter Notebook
jupyter notebook

# 3. 按顺序运行notebook（0 → 1 → 2 → 3 → 4）
```

## 📝 注意事项

1. **必须按顺序运行**: 后续步骤依赖前面步骤的输出
2. **固定数据**: 所有notebook使用决赛数据，适合快速测试
3. **小规模训练**: 模型训练使用较少的epochs，仅用于验证功能
4. **学习用途**: 包含详细注释，适合学习和理解工作流程

## 🔗 相关文件夹

- **通用版本**: `../2022WC_Notebooks_General/` - 支持任意比赛数据的完整版本
- **原始代码**: 项目根目录 - EPL数据的原始实现

## 📚 更多信息

详细文档请参考: `../ADAPTATION_GUIDE_2022_WC.md`