# Sewer Flow Analytical QA Framework

> An automated, reproducible QA framework for sewer flow survey data, developed as part of my MSc Dissertation.

## 🔬 Methodology: Design Science (DSM)
This project adopts a **Design Science Methodology (DSM)** to prioritises **auditability, reproducibility, and transparency** in engineering processes.

## 🏗️ System Architecture
The framework follows a modular pipeline designed for deterministic evidence-based auditing.

```mermaid
graph LR
    A[Raw .FDV / .R Files] --> B[Data Parsers]
    B --> C[Hydraulic State Engine]
    C --> D{QA Diagnostic Suite}
    D -- "Monitor-Level" --> E[completeness / dropouts / diurnal]
    D -- "System-Level" --> F[volume balance / coherence]
    E & F --> G[RAG Triage Logic]
    G --> H[Interactive Streamlit Dashboard]
```

## 🛠️ Requirements-to-Implementation Mapping
| Requirement | Implementation Anchor | Output |
|-------------|-----------------------|--------|
| Parse FDV & Rainfall | `parsers.py` | Structured DataFrames |
| Data Completeness | `calculate_completeness()` | % Acquisition KPI |
| Sensor Dropout | `detect_dropouts()` | Probe Fouling Flags |
| Diurnal Analysis | `calculate_diurnal_flatness()` | CV-based Health Flag |
| Hydraulic Coherence | `calculate_hydraulic_coherence()` | Pearson r Correlation |
| System Balance | `calculate_volume_imbalance()` | Up-Down Continuity % |
| Storm Segmentation | `segment_storms()` | Event Tables (WaPUG) |

## 🛠️ Core Features
- **Industry-Standard Parsing**: Support for FDV and Rainfall (.R) formats.
- **Multi-Level QA**: Completeness, dropout detection, diurnal flatness, and hydraulic coherence.
- **System Diagnostics**: Upstream-downstream volume balance analysis.
- **Hydrological Ingestion**: WaPUG/UDG compliant storm segmentation.

## 🧪 Experiments Conducted
The tool was validated using the Swansea dataset across 5 core experiments:
1. Missingness & Completeness
2. Upstream-Downstream Balance
3. RAG Health Classification
4. Dropout Detection
5. Rainfall Storm Segmentation
