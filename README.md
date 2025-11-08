# Analytics for Data Products IDEs

This repository analyzes **tool window usage patterns** based on an event log containing `open` and `close` actions.  
The primary goal is to determine whether there's a statistically significant difference in how long the tool window stays open depending on how it was opened — **manually** or **automatically**.

---

## Project Overview

In real-world telemetry data, events are often messy — multiple opens in a row, missing closes, or orphaned events are common.  
This project implements a **robust open–close matching algorithm** and performs **statistical testing** to compare manual vs. auto usage durations.

### Objectives:
1. **Reconstruct tool usage episodes** by matching `open` and `close` events.
2. **Compute usage durations** for each complete episode.
3. **Compare duration patterns** between `manual` and `auto` open types.
4. **Determine statistical significance** using a t-test.
5. **Visualize** duration distributions with `seaborn`.

---

## Installation & Setup

### Clone the Repository and Install Dependencies
```bash
git clone https://github.com/your-username/toolwindow-duration-analysis.git
cd Analytics-for-Data-Products-IDEs
pip install pandas numpy scipy seaborn matplotlib
```
### Add Data
Data file is in the git repo but if there is any issues, delete and add the csv file in the root directory.

### Run Code
```bash
python task1.py
```

---

### Documentation
A detailed analysis summary is available in:

This document explains:

- Analytical assumptions
- Matching strategy
- Handling of messy data
- Statistical results and visual insights

---
