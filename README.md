# Behavioral Deviation & Social Role Modeling  
### An ethology-to-cybersecurity inspired analysis

## Overview

This repository contains a Python-based analytical project exploring behavioral deviation and social role dynamics using ethological data from cattle observations.

The project applies systems-thinking concepts commonly used in cybersecurity and monitoring contexts (behavioral baselines, deviations, anomaly flags, directional flows, and role asymmetry) to behavioral data. The goal is not to reframe ethology as cybersecurity, but to demonstrate that the underlying analytical reasoning and modeling strategies are domain-independent.

Rather than producing a single global score or hierarchy, the project decomposes behavior into interacting systems and examines how individuals and groups redistribute behavioral energy under changing conditions.

---

## Data

The analysis is built on four datasets:

- Ethogram reference mapping observed behaviors to categories  
- Group-level scan observations used to construct behavioral baselines  
- An individual observation used as a stress-response case study  
- Directed social interaction records (actor → target)  


---

## Analytical Approach

The project follows these stages:

### Behavioral Baselines
Group-level baselines are constructed from scan observations and used as the reference frame for all downstream analyses.

Scripts:
1_build_behavior_baseline.py

### Deviation Analysis
Behavioral expression is analyzed as deviation from baseline rather than as absolute counts. Deviations are visualized using heatmaps and category-specific baseline bands to preserve context and variability.

Scripts: 
- 2_group_deviations_heatmaps.py 
- 3_N2_event_heatmap.py 
- 3_rumination_baseline_band_day3.py

### Anomaly Flagging
A lightweight anomaly layer identifies statistically rare deviations per behavioral category. Flags serve as investigation cues rather than conclusions, supporting human-in-the-loop analysis.

Scripts: 
- 4_anomaly_flags_build.py
- 4_explore_scan_anomalies.py

### Social Interaction Modeling
Directed interactions are modeled as three independent systems:

- **Agonistic** (pressure application)  
- **Appeasement** (de-escalation)  
- **Affiliative** (bonding)  

Individuals may occupy different roles across systems, allowing social structure to emerge without collapsing it into a single dominance axis.

Scripts
- 5_social_summary.py
- 6_plot_social_graphs.py
- 7_entity_role_profiles_graph.py

---

## Outputs

Key outputs include:

- Behavioral deviation heatmaps (group-level and focal individual)  
- Category-specific baseline band visualizations  
- Anomaly flag table 
- Directed interaction network graphs  
- Entity-level social role profiles across interaction systems  

Each output highlights different aspects of system behavior and complements the others.

---

## Repository Structure

The repository is organized into `data`, `docs`, `scripts`, and `outputs` directories. Scripts are modular and reflect analytical stages rather than a single linear pipeline.

```text

├── data/
│   ├── directed_social_interactions.csv
│   ├── ethogram_reference.csv
│   ├── group_scan_observations.csv
│   └── N2_individual_observation.csv
├── docs/
│   ├── figures
│   └── DISCUSSION.md/
│
├── outputs/
│   ├── anomalies_flags/ 
│   ├── baselines/
│   ├── group_scans/
│   └── social_roles/
│
├── scripts/
    ├── utils/
│   ├── 1_build_behavior_baseline.py
│   ├── 2_group_deviations_heatmaps.py
│   ├── 3_group_rumination_baseline_band_day3.py
│   ├── 3_N2_event_heatmap.py
│   ├── 4_anomaly_flags_build.py
│   ├── 4_explore_scan_anomalies.py
│   ├── 5_social_summary.py
│   ├── 6_plot_social_graphs.py
│   ├── 7_entity_role_profiles_graph.py
│   ├── exploratory_compare_behavior_across_days.py
│   └── exploratory_vlimits.py
└── README.md
```
Exploratory scripts and intermediate outputs are intentionally retained for transparency and may retain original labels.

---

## Tools

- Python  
- pandas, numpy  
- matplotlib  
- networkx  

---

## Conceptual Context

A detailed conceptual framework, interpretive discussion, and domain-transfer analysis are provided in `DISCUSSION.md`. That document focuses on *why* the analytical choices were made and how different lenses reveal distinct aspects of social organization.

---

## Limitations

- Observational data reflect a specific context and population  
- Behavioral coding is manual and observer-dependent  
- N2 individual observation are event-driven rather than time-uniform  
- Human intervention introduces non-natural stressors
