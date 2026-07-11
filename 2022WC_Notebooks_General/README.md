# 2022世界杯通用版Notebooks

本文件夹包含完整功能的notebook，支持分析任意2022世界杯比赛数据，适合实际研究和生产环境使用。

## 📋 运行顺序

请按照以下顺序依次运行notebook：

### 0️⃣ 数据转换
**文件**: `0_ConvertTracking_2022WC.ipynb`
- **功能**: 批量转换追踪数据为CSV格式
- **灵活性**: 
  - 支持单场比赛
  - 支持多场比赛批量处理
  - 支持处理所有64场比赛
- **输出**: `Data/{game_id}/` 目录下的CSV文件
- **运行时间**: 每场比赛约2-5分钟

### 1️⃣ 模型训练
**文件**: `1_RunGATModel_2022WC.ipynb`
- **功能**: 训练GAT模型（完整训练，10-40 epochs）
- **依赖**: 需要先运行步骤0
- **灵活性**: 支持单场或多场比赛数据训练
- **输出**: 
  - `results/model_final_{game_id}.pth` - 训练好的模型
  - `results/scaler_final_{game_id}.pkl` - 特征缩放器
  - `results/scaled_graphs_final_{game_id}.pkl` - 缩放后的图数据
- **运行时间**: 每场比赛约10-30分钟

### 2️⃣ 可视化分析
**文件**: `2_Visualisation_2022WC.ipynb`
- **功能**: 交互式可视化工具，深入分析模型预测
- **依赖**: 需要先运行步骤0和1
- **特点**: 
  - 完整的交互式控件
  - 支持任意比赛数据
  - 实时防守影响力分析
- **输出**: 交互式可视化界面
- **运行时间**: 约2-5分钟

### 3️⃣ 球员评估
**文件**: `3_PlayerEval_2022WC.ipynb`
- **功能**: 完整的防守球员影响力评估
- **依赖**: 需要先运行步骤0和1
- **特点**: 
  - 分析所有比赛帧
  - 生成详细统计报告
  - 包含可视化图表
- **输出**: 
  - `results/player_eval_{game_id}/{game_id}_defender_performance.csv`
  - `results/player_eval_{game_id}/{game_id}_analysis.png`
- **运行时间**: 每场比赛约10-20分钟

### 4️⃣ 实验分析
**文件**: `4_Experiments_2022WC.ipynb`
- **功能**: 综合实验分析和统计建模
- **依赖**: 需要先运行步骤0、1和3
- **特点**: 
  - 支持多场比赛数据合并分析
  - 网格区域分析
  - 防守组合分析
  - 相关性分析
  - 球员排名
- **输出**: 
  - `results/experiments_2022WC/results_model_df.csv`
  - `results/experiments_2022WC/defender_rankings.csv`
  - 各类统计图表
- **运行时间**: 约5-10分钟

## 🚀 快速开始

```bash
# 1. 激活虚拟环境
defensiveGATenv\Scripts\activate

# 2. 启动Jupyter Notebook
jupyter notebook

# 3. 按顺序运行notebook（0 → 1 → 2 → 3 → 4）
```

## 🎯 使用场景

### 场景1: 分析单场比赛
```python
# 在每个notebook的配置单元格中设置
GAME_ID = '10517'  # 决赛
# 或
GAME_IDS = ['10517']
```

### 场景2: 分析多场比赛
```python
# 分析决赛、季军赛和半决赛
GAME_IDS = ['10517', '3857', '3859', '3855']
```

### 场景3: 分析所有比赛
```python
# 分析全部64场比赛
GAME_IDS = ct.get_available_games()
```

## 📊 数据要求

- **原始数据位置**: `E:\JerryWu\Master\SoccerAnalytics\OpenData\TrackingData\Gradient Sports Enhanced 2022 World Cup Dataset`
- **数据格式**: 
  - 追踪数据: `.jsonl.bz2`
  - 元数据: `.json`
  - 阵容数据: `.json`

## 💡 最佳实践

1. **首次使用**: 建议先用单场比赛测试完整流程
2. **批量处理**: 处理多场比赛时建议分批进行，避免内存问题
3. **保存中间结果**: 每个步骤的输出都会保存，可以随时从任意步骤继续
4. **模型复用**: 训练好的模型可以用于后续分析，无需重复训练

## 📝 注意事项

1. **运行顺序**: 必须按照0→1→2→3→4的顺序运行
2. **磁盘空间**: 确保有足够空间存储处理后的数据和模型
3. **内存要求**: 建议至少8GB RAM，处理多场比赛时需要更多
4. **训练时间**: 完整训练比测试版本耗时更长，但结果更准确

## 🔗 相关文件夹

- **测试版本**: `../2022WC_Notebooks_Test/` - 快速测试和学习用的决赛版本
- **原始代码**: 项目根目录 - EPL数据的原始实现

## 📚 更多信息

详细文档请参考: `../ADAPTATION_GUIDE_2022_WC.md`

## 🆘 常见问题

### Q: 中文显示为方框？
A: notebook已配置中文字体，如仍有问题请检查系统是否安装了SimHei或Microsoft YaHei字体。

### Q: 内存不足？
A: 减少同时处理的比赛数量，或关闭其他程序释放内存。

### Q: 找不到数据文件？
A: 检查`convert_tracking.py`中的数据集路径配置是否正确。

### Q: 模型训练很慢？
A: 这是正常现象，完整训练需要较长时间。可以先用测试版本验证功能。