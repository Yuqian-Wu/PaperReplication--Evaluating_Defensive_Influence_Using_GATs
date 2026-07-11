# 2022世界杯Notebooks使用指南

本项目已将2022世界杯适配的notebooks重新组织，分为**测试版本**和**通用版本**两个文件夹，便于使用和管理。

## 📂 文件夹结构

```
项目根目录/
├── 2022WC_Notebooks_Test/          # 测试版本（决赛数据）
│   ├── 0_test_convert_tracking_final.ipynb
│   ├── 1_test_run_gat_model_final.ipynb
│   ├── 2_test_visualisation_final.ipynb
│   ├── 3_test_player_eval_final.ipynb
│   ├── 4_test_experiments_final.ipynb
│   └── README.md
│
└── 2022WC_Notebooks_General/       # 通用版本（任意比赛）
    ├── 0_ConvertTracking_2022WC.ipynb
    ├── 1_RunGATModel_2022WC.ipynb
    ├── 2_Visualisation_2022WC.ipynb
    ├── 3_PlayerEval_2022WC.ipynb
    ├── 4_Experiments_2022WC.ipynb
    └── README.md
```

## 🎯 选择合适的版本

### 测试版本 (2022WC_Notebooks_Test/)

**适用场景**:
- ✅ 首次使用，想快速了解工作流程
- ✅ 学习和理解代码逻辑
- ✅ 验证环境配置是否正确
- ✅ 快速测试新功能

**特点**:
- 固定使用决赛数据（阿根廷 vs 法国）
- 小规模训练（5 epochs）
- 详细的中文注释
- 运行时间短（总计约15-25分钟）

**开始使用**:
```bash
cd "2022WC_Notebooks_Test"
# 查看README.md了解详细说明
```

### 通用版本 (2022WC_Notebooks_General/)

**适用场景**:
- ✅ 实际研究和数据分析
- ✅ 分析多场比赛数据
- ✅ 需要高质量的模型结果
- ✅ 生产环境使用

**特点**:
- 支持任意2022世界杯比赛
- 完整训练（10-40 epochs）
- 支持批量处理
- 生产级代码质量

**开始使用**:
```bash
cd "2022WC_Notebooks_General"
# 查看README.md了解详细说明
```

## 🚀 快速开始

### 步骤1: 环境准备
```bash
# 激活虚拟环境
defensiveGATenv\Scripts\activate

# 验证依赖包
pip list | findstr "torch pandas numpy matplotlib"
```

### 步骤2: 选择版本
- **新手/测试**: 进入 `2022WC_Notebooks_Test/`
- **研究/生产**: 进入 `2022WC_Notebooks_General/`

### 步骤3: 启动Jupyter
```bash
jupyter notebook
```

### 步骤4: 按顺序运行
按照文件名前缀的数字顺序运行（0 → 1 → 2 → 3 → 4）

## 📊 运行顺序说明

| 步骤 | Notebook | 功能 | 依赖 |
|------|----------|------|------|
| 0️⃣ | ConvertTracking | 数据转换 | 无 |
| 1️⃣ | RunGATModel | 模型训练 | 步骤0 |
| 2️⃣ | Visualisation | 可视化分析 | 步骤0,1 |
| 3️⃣ | PlayerEval | 球员评估 | 步骤0,1 |
| 4️⃣ | Experiments | 实验分析 | 步骤0,1,3 |

⚠️ **重要**: 必须按顺序运行，后续步骤依赖前面步骤的输出！

## 🔄 版本对比

| 特性 | 测试版本 | 通用版本 |
|------|---------|---------|
| 数据范围 | 固定（决赛） | 灵活（任意比赛） |
| 训练规模 | 小（5 epochs） | 完整（10-40 epochs） |
| 运行时间 | 短（15-25分钟） | 长（30-60分钟/场） |
| 注释详细度 | 非常详细 | 简洁高效 |
| 适用场景 | 学习、测试 | 研究、生产 |
| 结果质量 | 验证用 | 发表级 |

## 📝 原始文件说明

项目根目录下的原始notebook文件（如`RunGATModel.ipynb`、`Experiments.ipynb`等）是为EPL数据设计的原始实现，已保留作为参考。

**建议**: 使用新组织的文件夹中的notebooks，它们已针对2022世界杯数据进行了完整适配。

## 📚 详细文档

- **完整适配指南**: `ADAPTATION_GUIDE_2022_WC.md`
- **测试版本说明**: `2022WC_Notebooks_Test/README.md`
- **通用版本说明**: `2022WC_Notebooks_General/README.md`

## 🆘 常见问题

### Q: 应该使用哪个版本？
A: 
- 首次使用或学习 → 测试版本
- 实际研究或分析 → 通用版本

### Q: 可以跳过某些步骤吗？
A: 不可以。每个步骤都依赖前面步骤的输出，必须按顺序运行。

### Q: 中文显示为方框？
A: Notebooks已配置中文字体支持。如仍有问题，请检查系统字体。

### Q: 原始notebooks还能用吗？
A: 原始notebooks是为EPL数据设计的，建议使用新文件夹中的适配版本。

## 🎓 学习路径建议

1. **第一次使用**: 
   - 阅读 `2022WC_Notebooks_Test/README.md`
   - 按顺序运行测试版本的所有notebooks
   - 理解每个步骤的作用

2. **深入学习**:
   - 阅读 `ADAPTATION_GUIDE_2022_WC.md`
   - 了解适配过程和技术细节
   - 尝试修改参数观察效果

3. **实际应用**:
   - 使用通用版本分析感兴趣的比赛
   - 尝试批量处理多场比赛
   - 进行深入的统计分析

## 📧 获取帮助

如有问题，请参考：
1. 各文件夹中的README.md
2. ADAPTATION_GUIDE_2022_WC.md
3. Notebooks中的详细注释

---

**最后更新**: 2025年11月8日
**版本**: v1.0