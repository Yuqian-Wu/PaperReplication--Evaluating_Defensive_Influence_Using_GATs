# Evaluating Defensive Influence Using GATs — 2022 FIFA World Cup Adaptation

**Paper Reproduction Project**: Adapting Gregory Everett's GAPP (Graph Attention for Pass Probabilities) model from English Premier League data to the 2022 FIFA World Cup tracking dataset.

---

## 📌 Project Overview

This project is based on the IEEE DSAA 2025 paper:
> **"Evaluating Defensive Influence in Multi-Agent Systems Using Graph Attention Networks"**  
> Gregory Everett, Ryan J. Beal, Tim Matthews, Timothy J. Norman, Sarvapali D. Ramchurn (2025)

**Original Implementation**: 306 EPL matches with event and tracking data (provided by Gradient Sports)

**This Project's Contributions**:
- ✅ Full adaptation to **Gradient Sports Enhanced 2022 World Cup Dataset**
- ✅ Resolved coordinate system, data format, and half-time separation challenges
- ✅ Provided two versions of notebooks: Test and General
- ✅ Validated model effectiveness on the World Cup Final (Argentina vs France)

---

## 🎯 Model Capabilities

### 1️⃣ Pass Reception Probability Prediction
Uses Graph Attention Networks (GAT) to predict each attacking player's probability of receiving the ball at the next event by modeling game state as a graph structure.

<p align="center">
  <img src="https://github.com/user-attachments/assets/bb35bae7-c76c-467a-86f7-18816c9060cd" alt="Reception_Prediction" width="600" />
</p>

### 2️⃣ Defensive Influence Metrics
Extracts two novel defensive metrics through the GAT attention mechanism:

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/b52efd80-d383-41fd-b6ac-a4e5664f9d99" alt="DI" width="420" />
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/cd54f579-bfe9-4677-befe-a8fbd5a5afa7" alt="DP" width="420" />
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <em>Left — Defender Influence (DI): the change in an attacker's reception probability when a specific defender's attention is masked. Positive DI indicates the defender reduces the attacker's chance to receive the ball.  
      Right — Defender Performance (DP): the DI values aggregated and weighted by each attacker's xT (attacking threat). DP quantifies a defender's overall off‑ball positional value in reducing dangerous reception opportunities.</em>
    </td>
  </tr>
</table>

---

## 🚀 Quick Start

### Environment Setup
```bash
# Activate virtual environment
defensiveGATenv\Scripts\activate

# Verify dependencies
pip list | findstr "torch pandas numpy matplotlib"
```

### Choose Your Version

#### 📂 Test Version (`2022WC_Notebooks_Test/`)
**Suitable for**: First-time users, learning, environment validation  
**Features**: Fixed final match data, fast training (5 epochs), detailed Chinese annotations, 15-25 minutes total runtime

```bash
cd 2022WC_Notebooks_Test
jupyter notebook
# Run in order: 0 → 1 → 2 → 3 → 4
```

#### 📂 General Version (`2022WC_Notebooks_General/`)
**Suitable for**: Research, multi-match analysis, high-quality results  
**Features**: Any 2022 World Cup match, full training (10-40 epochs), production-ready code

```bash
cd 2022WC_Notebooks_General
jupyter notebook
# Run in order: 0 → 1 → 2 → 3 → 4
```

### Notebook Workflow

| Step | Notebook | Function | Depends On |
|:---:|----------|----------|:----------:|
| **0** | ConvertTracking | Convert raw tracking data to model input format | None |
| **1** | RunGATModel | Build graph data, train GAT model | 0 |
| **2** | Visualisation | Interactive visualization of predictions and DI/DP metrics | 0, 1 |
| **3** | PlayerEval | Compute player-level defensive metrics | 0, 1 |
| **4** | Experiments | Defensive performance comparison, attention mechanism validation, case studies | 0, 1, 3 |

⚠️ **Must run in order** — subsequent steps depend on outputs from previous steps!

---

## 📊 Version Comparison

| Feature | Test Version | General Version |
|---------|:------------:|:---------------:|
| Data Scope | Fixed (Final match) | Flexible (Any match) |
| Training Scale | Small (5 epochs) | Full (10-40 epochs) |
| Runtime | Short (15-25 min) | Long (30-60 min/match) |
| Annotation Detail | Very detailed | Concise & efficient |
| Use Case | Learning, Testing | Research, Production |
| Result Quality | Validation-grade | Publication-grade |

---

## 📁 Project Structure

```
Project Root/
├── 2022WC_Notebooks_Test/          # Test version notebooks (Final match)
├── 2022WC_Notebooks_General/       # General version notebooks (Any match)
├── GNNs/                           # Trained model files
├── Data/                           # Data files (prepare yourself)
├── results/                        # Output results (plots, metrics)
├── convert_tracking.py             # Data conversion module (adapted for 2022WC)
├── create_graph.py                 # Graph construction module (adapted for 2022WC)
├── plot_functions.py               # Plotting utilities
├── scale_graph.py                  # Graph normalization utilities
├── visualisation.py                # Visualization module
├── xT_grid.csv                     # Expected threat value grid
├── ADAPTATION_GUIDE_2022_WC.md     # Complete adaptation documentation
└── requirements.txt                # Python dependencies
```

---

## 🔬 Model Architecture

<img width="12925" height="4340" alt="ModelDiagram" src="https://github.com/user-attachments/assets/aadf973e-09ea-41cd-9e22-5ca0f8a32ccf" />

### Architecture Details
- **Graph construction**: Fully connected, directed graph with a special ball node (V = players ∪ {ball})
- **Node features**: Position, velocity, acceleration, distances to goals, distance/angle to ball, on-attacking-team/on‑ball flags
- **Edge features**: Relative distances, edge angle, difference in node angles to the ball, same‑team flag
- **GAT specifics**: 2 GAT layers, 16 attention heads, skip connection + concatenation to encoders

### Training Hyperparameters
- Batch size: 64 | Epochs: 200 (original) / 5-40 (this project)
- Node hidden size: 32 | Edge hidden size: 16
- Loss: Binary cross‑entropy (attacking players masked to compute loss only where relevant)
- Optimizer: Adam, initial LR = 0.003

---

## 📚 Data Description

### Original Dataset (EPL)
English Premier League events and tracking data provided by Gradient Sports (306 matches, ~359,040 on‑ball events).

### This Project's Data (2022 FIFA World Cup)
**Gradient Sports Enhanced 2022 World Cup Dataset**
- Contains complete player and ball tracking data
- Coordinate system: Center origin (0,0), X-axis along length, Y-axis along width
- Data files must be prepared separately (see `ADAPTATION_GUIDE_2022_WC.md`)

---

## 🎓 Learning Path

1. **Getting Started**: Read `2022WC_Notebooks_Test/README.md` → Run test version notebooks
2. **Deep Dive**: Read `ADAPTATION_GUIDE_2022_WC.md` → Understand adaptation details
3. **Application**: Use general version to analyze matches of interest → Batch process multiple matches

---

## 💡 Potential Use Cases

- **Post‑match tactical analysis**: Visualize event‑by‑event DI/DP to identify moments where defender positioning prevented high‑threat receptions
- **Scouting & recruitment**: Rank and compare defenders by normalized season DP to identify players who consistently limit high‑xT receivers
- **Player development & coaching**: Provide targeted feedback on off‑ball positioning (which attacker matchups a defender influences most)
- **Match preparation / opposition scouting**: Identify attackers a defender is particularly effective (or weak) against and adapt marking strategies
- **Research & transfer to other domains**: Framework generalizes to other multi‑agent systems (e.g., security games or other team sports) where agent influence can be framed via attention

---

## 📖 Citation & Contact

If you use this work, please cite the original paper:

```bibtex
@inproceedings{everett2025evaluating,
  title     = {Evaluating Defensive Influence in Multi-Agent Systems Using Graph Attention Networks},
  author    = {Everett, Gregory and Beal, Ryan J. and Matthews, Tim and Norman, Timothy J. and Ramchurn, Sarvapali D.},
  booktitle = {2025 IEEE 12th International Conference on Data Science and Advanced Analytics},
  year      = {2025}
}
```

**Original Author Contact**: gae1g17@soton.ac.uk  
**Dataset Inquiries**: https://www.gradientsports.com/

---

## 🆘 FAQ

### Q: Which version should I use?
A: First-time use or learning → **Test Version** | Actual research or analysis → **General Version**

### Q: Can I skip some steps?
A: **No**. Each step depends on outputs from previous steps and must be run in order.

### Q: What are the main differences from the original code?
A: See `ADAPTATION_GUIDE_2022_WC.md`, including:
- Coordinate system transformation (center origin → bottom-left origin)
- Half-time separation logic (based on game time instead of team ID)
- Data loading format (Parquet → CSV + timestamp alignment)
- xT grid interpolation (bilinear interpolation matching new coordinate system)

### Q: Chinese characters display as boxes?
A: Notebooks are configured with Chinese font support (SimHei/Microsoft YaHei). If issues persist, check system fonts.

---

**Project Version**: v1.0  
**Last Updated**: November 2025  
**Adapted by**: Jerry Wu
