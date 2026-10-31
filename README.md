# NYC Airbnb Data Summary Tool

**Course:** CPSC-620-3 Agile Software Development  
**Group:** Group 3  


---

## 1. Project Overview

The **NYC Airbnb Data Summary Tool** is a modular Python-based application designed to ingest, clean, validate, and summarize the New York City Airbnb listings dataset (`Airbnb_NYC.csv`). The project follows **Agile Software Development** principles using feature branching, collaborative pull requests, test-driven validation, and comprehensive documentation.

---

## 2. Sprint Goal

Develop a robust Python tool that automatically cleans and processes raw NYC Airbnb listing data, handles missing and noisy data, produces descriptive summary statistics, and provides verified quality assurance through automated unit tests.

---

## 3. Team Members & Responsibilities

| Team Member | Role | Contribution |
| :--- | :--- | :--- |
| **Baljeet Kaur** | QA & Testing Engineer | Automated unit & integration test suite (`tests/test_data_cleaning.py`), `TESTING.md` report, `README.md`, `requirements.txt` |
| **Iheanacho, Precious** | Developer | Data pipeline development and implementation |
| **Martins Ronqui Miyajima, Paula** | Data Analyst | Exploratory Data Analysis, outlier detection, visualizations (`Paula Task - NYC_Airbnb_Data_Analysis_Sprint1.ipynb`) |
| **Zhu, Yaqun** | Developer | Pipeline architecture, data ingestion, cleaning logic, and summary generation (`src/data_cleaning.py`) |

---

## 4. Project Structure

```text
CPSC-620-3-Agile-Software-Development/
├── data/
│   └── Airbnb_NYC.csv                       # Raw NYC Airbnb dataset
├── src/
│   └── data_cleaning.py                     # Data ingestion, cleaning & summarization pipeline
├── tests/
│   ├── __init__.py                          # Test package marker
│   └── test_data_cleaning.py                # Unit and integration test suite (18 test cases)
├── Paula Task - NYC_Airbnb_Data_Analysis_Sprint1.ipynb  # EDA & outlier analysis notebook
├── .gitignore                               # Git ignore rules
├── README.md                                # Project documentation
├── requirements.txt                         # Project dependencies
└── TESTING.md                               # QA test plan and verification report
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.9 or higher
- `git`

### Step 1 — Clone the Repository
```bash
git clone https://github.com/<your-org-or-username>/CPSC-620-3-Agile-Software-Development.git
cd CPSC-620-3-Agile-Software-Development
```

### Step 2 — Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. How to Run

### Run the Data Cleaning & Summarization Pipeline
```bash
python src/data_cleaning.py
```

### Run the Automated Test Suite
No extra installations needed — uses Python's built-in `unittest`:
```bash
python -m unittest discover -s tests -v
```

Or with `pytest` if installed:
```bash
pytest tests/ -v
```

### Open the Jupyter Analysis Notebook
```bash
jupyter notebook "Paula Task - NYC_Airbnb_Data_Analysis_Sprint1.ipynb"
```

---

## 7. Sprint 1 — Results

Running the pipeline on `Airbnb_NYC.csv` produces the following verified output:

| Metric | Value |
| :--- | :--- |
| Original Listings | 42,336 |
| Cleaned Listings | 41,749 |
| Removed Records | 587 |
| Average Price | $153.88 |
| Median Price | $107.00 |
| Entire home/apt | 21,709 |
| Private room | 19,055 |
| Shared room | 985 |

---

## 8. Testing & Quality Assurance

The test suite (`tests/test_data_cleaning.py`) contains **18 automated tests** — all passing:

- **`load_data`** — Valid file loading, missing file (`FileNotFoundError`), empty file (`ValueError`).
- **`clean_data`** — Schema validation, deduplication, currency string parsing, positive value enforcement, missing value removal, room type standardization, and index reset.
- **`get_data_summary`** — Metric accuracy, empty DataFrame handling, type and schema validation.
- **Integration** — Full end-to-end pipeline from raw CSV to final summary.

For the complete test case matrix and QA report, see [TESTING.md](TESTING.md).

---

## 9. Agile Workflow

- Each team member works on a **separate feature branch**.
- Changes are merged to `main` only after **peer review via Pull Request**.
- **Definition of Done:** Code is modular, all tests pass, and documentation is up to date.
