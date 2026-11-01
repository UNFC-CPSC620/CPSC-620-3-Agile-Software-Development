# Sprint 1 Test Plan & Quality Assurance Report

**Course:** CPSC-620-3 Agile Software Development  
**Group:** Group 3  
**Sprint:** Sprint 1 — NYC Airbnb Data Summary Tool  
**Role Responsibility:** Testing & Quality Assurance  

---

## 1. Quality Assurance Strategy

In accordance with Agile development practices, the testing suite ensures high code reliability, prevents regression, and verifies all acceptance criteria before merging code into the main branch.

The test strategy incorporates:
- **Unit Testing:** Testing individual functions (`load_data`, `clean_data`, `get_data_summary`) in isolation with deterministic mock data.
- **Boundary & Edge-Case Testing:** Testing extreme values (missing values, whitespace-only fields, malformed currency strings, non-positive numbers, empty files).
- **Integration Testing:** End-to-end testing of the complete data pipeline (`load -> clean -> summarize`).
- **Zero-Dependency Test Runner:** Uses Python's standard `unittest` framework so tests can be run in any standard Python environment without requiring external package installations, while remaining fully compatible with `pytest`.

---

## 2. Test Execution

### Running All Tests (Standard Library - No Installation Needed)
```bash
python -m unittest discover -s tests -v
```

### Running a Specific Test File
```bash
python -m unittest tests/test_data_cleaning.py -v
```

### Running with Pytest (If Installed)
```bash
pytest tests/ -v
```

---

## 3. Test Suite Specification & Results Matrix

| Test ID | Function Under Test | Test Case Description | Expected Result | Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | `load_data` | Load valid CSV file from disk | Returns populated `pd.DataFrame` matching file content | **PASS** |
| **TC-02** | `load_data` | Attempt to load non-existent file path | Raises `FileNotFoundError` with clear error message | **PASS** |
| **TC-03** | `load_data` | Attempt to load an empty (0 byte) file | Raises `ValueError` / parsing error | **PASS** |
| **TC-04** | `load_data` | Attempt to load CSV with header only (0 rows) | Raises `ValueError: The dataset is empty.` | **PASS** |
| **TC-05** | `clean_data` | Validate input type is `pd.DataFrame` | Raises `TypeError` when input is string, list, or None | **PASS** |
| **TC-06** | `clean_data` | Check presence of required columns | Raises `ValueError` when required columns are missing | **PASS** |
| **TC-07** | `clean_data` | Remove duplicate rows | Duplicate rows are dropped, unique records preserved | **PASS** |
| **TC-08** | `clean_data` | Strip currency symbols (`$`, `,`) and convert price to float | Price converted to float (e.g., `"$1,250.00"` -> `1250.0`) | **PASS** |
| **TC-09** | `clean_data` | Filter invalid and non-positive prices (`<= 0` or NaN) | Drops records with prices `<= 0` or non-numeric values | **PASS** |
| **TC-10** | `clean_data` | Filter invalid and non-positive `minimum_nights` (`<= 0`) | Drops records with non-positive or non-numeric nights | **PASS** |
| **TC-11** | `clean_data` | Handle missing (`NaN`/`None`) and empty string values | Drops rows with empty/whitespace strings in required fields | **PASS** |
| **TC-12** | `clean_data` | Standardize room type casing and whitespace | Standardized to Title Case ('Entire home/apt', etc.) | **PASS** |
| **TC-13** | `clean_data` | Reset DataFrame index after dropping rows | Index is sequential `[0, 1, ..., N-1]` | **PASS** |
| **TC-14** | `get_data_summary` | Summary calculation on valid cleaned DataFrame | Correct count, average price, median, and room type counts | **PASS** |
| **TC-15** | `get_data_summary` | Handle empty DataFrame | Returns 0 listings, None averages, and empty dict | **PASS** |
| **TC-16** | `get_data_summary` | Validate DataFrame input type | Raises `TypeError` on invalid types | **PASS** |
| **TC-17** | `get_data_summary` | Verify required columns for summary calculation | Raises `ValueError` when required columns are absent | **PASS** |
| **TC-18** | Integration | Full end-to-end pipeline (`load -> clean -> summarize`) | Successfully executes workflow and matches expected stats | **PASS** |

**Summary:** 18 Tests Executed, 18 Passed, 0 Failed (100% Success Rate).

---

## 4. Key Quality Assurance Checks Implemented

1. **Defensive Input Validation:** Functions reject invalid data types and missing schemas early with informative error messages.
2. **Data Immutability Protection:** `clean_data` creates an explicit copy of the incoming DataFrame to prevent side-effects on original inputs.
3. **Data Integrity Verifications:** Automated assertions ensure:
   - Zero missing values in mandatory columns (`price`, `room_type`, `neighbourhood`, `minimum_nights`).
   - Prices strictly greater than 0.
   - Minimum nights strictly greater than 0.
   - No duplicate listing records.

