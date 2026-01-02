# Fruit Fly Genetics Tracker - Developer Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Module Documentation](#module-documentation)
4. [Data Flow](#data-flow)
5. [Storage Format](#storage-format)
6. [Extending the System](#extending-the-system)
7. [Testing Guidelines](#testing-guidelines)
8. [Troubleshooting](#troubleshooting)

---

## Project Overview

### Purpose
A command-line application for tracking and analyzing fruit fly genetic crosses in research settings. Automates Punnett square generation, phenotype prediction, and statistical validation of experimental results.

### Target Users
- Genetics researchers conducting fruit fly experiments
- Students learning Mendelian genetics
- Lab technicians tracking multiple breeding experiments

### Key Features
- Automated genetic cross calculations
- Chi-square statistical testing
- Data visualization (bar charts, pie charts)
- Persistent experiment storage
- Search and filtering capabilities

### Technology Stack
- **Language**: Python 3.8+
- **Core Libraries**:
  - `scipy` - Statistical analysis
  - `matplotlib` - Visualization
  - `itertools` - Combinatorial genetics calculations
- **Storage**: JSON file-based persistence

---

## Architecture

### Design Pattern
The application follows a **Model-View-Controller (MVC)** pattern adapted for CLI:

```
┌─────────────────────────────────────────────────────┐
│                   CLI Interface                      │
│              (menu.py, display.py)                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                  Core Logic                          │
│         (genetics.py, statistics.py)                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                Data Models                           │
│    (experiment.py, genotype.py, allele.py)          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Storage Layer                           │
│            (file_storage.py)                         │
└─────────────────────────────────────────────────────┘
```

### Directory Structure
```
fruit_fly_tracker/
├── main.py                 # Entry point
├── config.py              # Configuration settings
├── cli/
│   ├── menu.py           # Menu system and navigation
│   └── display.py        # Output formatting utilities
├── models/
│   ├── experiment.py     # Experiment data model
│   ├── genotype.py       # Genotype representation
│   └── allele.py         # Allele representation
├── core/
│   ├── genetics.py       # Genetic calculations
│   └── statistics.py     # Statistical analysis
├── storage/
│   └── file_storage.py   # Data persistence
├── visualization/
│   └── charts.py         # Chart generation
├── data/
│   └── experiments/      # Stored experiment JSON files
└── exports/              # Generated visualizations
```

---

## Module Documentation

### 1. models/allele.py

**Purpose**: Represents a single genetic variant (allele) for a trait.

**Class: `Allele`**

```python
Allele(symbol: str, description: str, is_dominant: bool)
```

**Attributes**:
- `symbol` (str): Single letter representing the allele (e.g., 'E' or 'e')
- `description` (str): Phenotype this allele produces (e.g., "Red eyes")
- `is_dominant` (bool): Whether this allele is dominant

**Methods**:
- `to_dict()`: Serializes allele to dictionary for storage
- `from_dict(data)`: Class method to reconstruct allele from dictionary

**Example**:
```python
red_allele = Allele(
    symbol='E',
    description='Red eyes',
    is_dominant=True
)
```

---

### 2. models/genotype.py

**Purpose**: Represents the complete genetic makeup of an organism for one or more traits.

**Class: `Genotype`**

```python
Genotype(genotype_string: str, allele_definitions: dict)
```

**Attributes**:
- `genotype_string` (str): String representation like "Ee Ww"
- `allele_definitions` (dict): Maps allele symbols to Allele objects
- `alleles` (dict): Parsed structure mapping traits to allele pairs

**Methods**:
- `get_gametes()`: Returns list of all possible gametes this genotype can produce
- `_parse_genotype()`: Internal method to parse genotype string
- `to_dict()` / `from_dict(data)`: Serialization methods

**Key Algorithm - Gamete Generation**:
```python
# For genotype "Ee Ww"
# Traits: [('E','e'), ('W','w')]
# Gametes: ["EW", "Ew", "eW", "ew"]

# Uses itertools.product for combinatorics
from itertools import product
allele_choices = [['E','e'], ['W','w']]
gametes = [''.join(combo) for combo in product(*allele_choices)]
```

**Example**:
```python
genotype = Genotype("Ee Ww", allele_definitions)
gametes = genotype.get_gametes()
# Returns: ["EW", "Ew", "eW", "ew"]
```

---

### 3. models/experiment.py

**Purpose**: Represents a complete genetics experiment with all associated data.

**Class: `Experiment`**

**Attributes**:
- `experiment_id` (str): Unique identifier (e.g., "EXP_001")
- `name` (str): Human-readable experiment name
- `date_created` (datetime): Timestamp of creation
- `date_modified` (datetime): Last modification timestamp
- `parent1` (Genotype): First parent's genotype
- `parent2` (Genotype): Second parent's genotype
- `allele_definitions` (dict): Maps symbols to Allele objects
- `expected_counts` (dict): Predicted phenotype counts
- `observed_counts` (dict or None): Actual observed counts
- `total_expected` (int): Total offspring expected to count
- `notes` (str): User notes
- `chi_square_result` (dict or None): Statistical test results

**State Transitions**:
```
Created → Expected Ratios Calculated → Observations Added → Analysis Complete
```

**Methods**:
- `set_expected_counts(expected_counts)`: Store calculated predictions
- `add_observations(observed_counts)`: Record actual experimental data
- `set_chi_square_result(result)`: Store statistical test results
- `is_complete()`: Check if observations have been recorded
- `get_status()`: Return "Complete" or "Pending"
- `to_dict()` / `from_dict(data)`: Serialization

**Example**:
```python
experiment = Experiment(
    experiment_id="EXP_001",
    name="Eye Color Cross",
    parent1_string="Ee",
    parent2_string="ee",
    allele_definitions=alleles,
    total_expected=500
)
```

---

### 4. core/genetics.py

**Purpose**: Implements core genetic calculations including Punnett squares and phenotype determination.

**Class: `GeneticsCalculator`**

**Key Methods**:

#### `generate_punnett_square(parent1, parent2)`
Generates all possible offspring genotypes from a cross.

**Algorithm**:
1. Get all gametes from parent 1
2. Get all gametes from parent 2
3. Combine each gamete from parent 1 with each from parent 2
4. Return list of offspring genotypes

**Time Complexity**: O(4^n) where n is number of traits

**Example**:
```python
# Cross: Ee × ee
# Parent 1 gametes: ["E", "e"]
# Parent 2 gametes: ["e", "e"]
# Offspring: ["Ee", "Ee", "ee", "ee"]

offspring = GeneticsCalculator.generate_punnett_square(parent1, parent2)
```

#### `calculate_phenotype_ratios(offspring_genotypes, allele_definitions)`
Converts genotypes to observable phenotypes using dominance rules.

**Algorithm**:
1. For each offspring genotype
2. For each trait in the genotype
3. Apply dominance rules to determine visible phenotype
4. Count occurrences of each phenotype combination
5. Calculate ratios

**Example**:
```python
# Genotypes: ["Ee", "Ee", "ee", "ee"]
# With E dominant (red), e recessive (white)
# Phenotypes: {"Red eyes": 2, "White eyes": 2}
# Ratios: {"Red eyes": 0.5, "White eyes": 0.5}
```

#### `_genotype_to_phenotype(genotype_string, allele_definitions)`
Internal method implementing dominance logic.

**Dominance Rules**:
1. If at least one dominant allele present → express dominant phenotype
2. If both alleles recessive → express recessive phenotype
3. For multiple traits → apply rule independently to each trait

---

### 5. core/statistics.py

**Purpose**: Performs chi-square goodness-of-fit testing on experimental results.

**Class: `StatisticalAnalyzer`**

**Key Method**: `chi_square_test(expected_counts, observed_counts, alpha)`

**Chi-Square Formula**:
```
χ² = Σ [(Observed - Expected)² / Expected]
```

**Algorithm**:
1. Calculate chi-square statistic
2. Determine degrees of freedom (n - 1)
3. Find critical value from chi-square distribution
4. Compare statistic to critical value
5. Generate interpretation

**Parameters**:
- `expected_counts`: Dictionary of phenotype → expected count
- `observed_counts`: Dictionary of phenotype → observed count
- `alpha`: Significance level (default: 0.05 from config)

**Returns**:
```python
{
    "chi_square": float,           # Test statistic
    "p_value": float,              # Probability value
    "degrees_freedom": int,        # df = n - 1
    "critical_value": float,       # From chi² table
    "alpha": float,                # Significance level
    "passed": bool,                # True if χ² < critical
    "interpretation": str          # Human-readable result
}
```

**Example**:
```python
result = StatisticalAnalyzer.chi_square_test(
    expected_counts={"Red": 250, "White": 250},
    observed_counts={"Red": 247, "White": 253}
)
# Returns: chi_square=0.072, p_value=0.788, passed=True
```

**Statistical Interpretation**:
- **Passed (χ² < critical)**: Observed data matches expected ratios within random variation
- **Failed (χ² ≥ critical)**: Significant deviation suggests:
  - Counting error
  - Selection bias
  - Different genetic mechanism
  - Non-random mortality

---

### 6. storage/file_storage.py

**Purpose**: Handles persistence of experiments to/from JSON files.

**Class: `ExperimentStorage`**

**Storage Strategy**:
- One JSON file per experiment
- Filename format: `{experiment_id}.json`
- Location: `data/experiments/` directory
- Human-readable JSON for easy debugging

**Methods**:

#### `save_experiment(experiment)`
Serializes experiment to JSON file.

**Process**:
1. Convert experiment to dictionary via `experiment.to_dict()`
2. Write to file with pretty-printing (indent=2)
3. Return filepath

#### `load_experiment(experiment_id)`
Deserializes experiment from JSON file.

**Process**:
1. Construct filepath from experiment_id
2. Check file exists
3. Load JSON
4. Reconstruct experiment via `Experiment.from_dict()`
5. Return experiment object or None

#### `list_all_experiments()`
Returns list of all experiment IDs.

#### `load_all_experiments()`
Loads all experiments into memory.

**Performance**: O(n) where n is number of experiments. For large datasets, consider pagination.

#### `search_experiments(query, field)`
Searches experiments by field value.

**Supported Fields**: Any experiment attribute (name, notes, etc.)

**Example JSON Structure**:
```json
{
  "experiment_id": "EXP_001",
  "name": "Eye Color Cross",
  "date_created": "2026-01-15T10:30:00",
  "date_modified": "2026-01-15T14:20:00",
  "parent1": {
    "genotype_string": "Ee",
    "alleles": {"trait_1": ["E", "e"]}
  },
  "parent2": {
    "genotype_string": "ee",
    "alleles": {"trait_1": ["e", "e"]}
  },
  "allele_definitions": {
    "E": {
      "symbol": "E",
      "description": "Red eyes",
      "is_dominant": true
    },
    "e": {
      "symbol": "e",
      "description": "White eyes",
      "is_dominant": false
    }
  },
  "total_expected": 500,
  "expected_counts": {
    "Red eyes": 250.0,
    "White eyes": 250.0
  },
  "observed_counts": {
    "Red eyes": 247,
    "White eyes": 253
  },
  "notes": "F2 generation test",
  "chi_square_result": {
    "chi_square": 0.072,
    "p_value": 0.788,
    "passed": true
  }
}
```

---

### 7. visualization/charts.py

**Purpose**: Generates publication-quality visualizations of experiment results.

**Class: `ChartGenerator`**

**Configuration** (from config.py):
- Default DPI: 300 (publication quality)
- Default size: (10, 6) inches
- Backend: Agg (non-interactive, for server environments)

**Methods**:

#### `create_bar_chart(experiment, output_path)`
Creates side-by-side bar chart comparing expected vs observed.

**Visual Elements**:
- X-axis: Phenotypes
- Y-axis: Count
- Blue bars: Expected counts
- Coral bars: Observed counts
- Legend, title, axis labels

**File Format**: PNG

#### `create_pie_chart(experiment, output_path)`
Creates pie chart showing phenotype distribution.

**Visual Elements**:
- Percentage labels
- Auto-arranged slices
- Color-coded segments

**Usage**:
```python
chart_path = ChartGenerator.create_bar_chart(experiment)
# Saves to: exports/EXP_001_bar_chart.png
```

---

### 8. cli/menu.py

**Purpose**: Implements command-line interface menu system and user interaction.

**Class: `MenuSystem`**

**Design Pattern**: State machine with menu-driven navigation

**Main Loop**:
```python
while running:
    display_menu()
    choice = get_user_input()
    execute_action(choice)
```

**Key Methods**:

#### `start()`
Initializes system and starts main menu loop.

#### `show_main_menu()`
Displays main menu and routes user choice to appropriate handler.

**Menu Options**:
1. Create new experiment → `create_experiment()`
2. Add observations → `add_observations()`
3. View results → `view_results()`
4. List all → `list_experiments()`
5. Search → `search_experiments()`
6. Visualize → `generate_charts()`
7. Delete → `delete_experiment()`

#### `create_experiment()`
Interactive workflow for creating new experiment.

**Steps**:
1. Get experiment name
2. Get parent genotypes
3. Define alleles interactively
4. Get expected count
5. Calculate predictions
6. Save experiment

#### `add_observations()`
Interactive workflow for recording experimental results.

**Steps**:
1. Select experiment
2. Display expected counts
3. Collect observed counts
4. Validate total
5. Run chi-square test
6. Display results
7. Save

#### `_select_experiment()`
Helper method to display experiment list and get user selection.

**Returns**: Selected Experiment object or None

---

### 9. cli/display.py

**Purpose**: Provides formatting utilities for consistent CLI output.

**Class: `Display`**

**Static Methods**:

#### `header(text)`
Displays section header with decorative lines.
```
============================================================
                    EXPERIMENT RESULTS
============================================================
```

#### `section(text)`
Displays subsection header with underline.
```
STATISTICAL ANALYSIS
--------------------
```

#### `table(headers, rows)`
Displays data in aligned column format.

**Algorithm**:
1. Calculate maximum width for each column
2. Print headers with padding
3. Print separator line
4. Print each row with aligned columns

#### `success(text)`, `error(text)`, `info(text)`
Displays messages with appropriate symbols (✓, ✗, ℹ).

---

## Data Flow

### Complete Workflow: Creating and Analyzing an Experiment

```
1. USER CREATES EXPERIMENT
   ├─> MenuSystem.create_experiment()
   ├─> Collect user input (name, parents, alleles)
   ├─> Create Experiment object
   ├─> Create Genotype objects for parents
   └─> Save to storage
       │
       ▼
2. CALCULATE PREDICTIONS
   ├─> GeneticsCalculator.generate_punnett_square()
   │   ├─> parent1.get_gametes()
   │   ├─> parent2.get_gametes()
   │   └─> Combine all gamete pairs
   ├─> GeneticsCalculator.calculate_phenotype_ratios()
   │   ├─> Apply dominance rules
   │   └─> Count phenotype occurrences
   ├─> GeneticsCalculator.calculate_expected_counts()
   └─> experiment.set_expected_counts()
       │
       ▼
3. USER PERFORMS LAB WORK
   (External to system - actual fly counting)
       │
       ▼
4. USER ADDS OBSERVATIONS
   ├─> MenuSystem.add_observations()
   ├─> Select experiment
   ├─> Display expected counts
   ├─> Collect observed counts
   └─> experiment.add_observations()
       │
       ▼
5. STATISTICAL ANALYSIS
   ├─> StatisticalAnalyzer.chi_square_test()
   │   ├─> Calculate χ² statistic
   │   ├─> Determine p-value
   │   └─> Compare to critical value
   ├─> experiment.set_chi_square_result()
   └─> Display results to user
       │
       ▼
6. VISUALIZATION (Optional)
   ├─> ChartGenerator.create_bar_chart()
   ├─> ChartGenerator.create_pie_chart()
   └─> Save to exports directory
       │
       ▼
7. PERSISTENT STORAGE
   └─> ExperimentStorage.save_experiment()
       └─> Write JSON to data/experiments/
```

---

## Storage Format

### File Organization
```
data/
└── experiments/
    ├── EXP_001.json
    ├── EXP_002.json
    └── EXP_003.json

exports/
├── EXP_001_bar_chart.png
├── EXP_001_pie_chart.png
└── ...
```

### JSON Schema

**Top Level**:
- `experiment_id`: String, unique identifier
- `name`: String, experiment name
- `date_created`: ISO 8601 timestamp
- `date_modified`: ISO 8601 timestamp
- `parent1`: Genotype object (see below)
- `parent2`: Genotype object
- `allele_definitions`: Object mapping symbols to Allele objects
- `total_expected`: Integer
- `expected_counts`: Object mapping phenotypes to floats
- `observed_counts`: Object mapping phenotypes to integers (nullable)
- `notes`: String
- `chi_square_result`: Object (nullable)

**Genotype Object**:
```json
{
  "genotype_string": "Ee Ww",
  "alleles": {
    "trait_1": ["E", "e"],
    "trait_2": ["W", "w"]
  }
}
```

**Allele Object**:
```json
{
  "symbol": "E",
  "description": "Red eyes",
  "is_dominant": true
}
```

**Chi-Square Result Object**:
```json
{
  "chi_square": 0.072,
  "p_value": 0.788,
  "degrees_freedom": 1,
  "critical_value": 3.841,
  "alpha": 0.05,
  "passed": true,
  "interpretation": "Your data matches expected ratios..."
}
```

---

## Extending the System

### Adding New Features

#### 1. Adding a New Statistical Test

**Step 1**: Add method to `StatisticalAnalyzer`
```python
@staticmethod
def g_test(expected_counts, observed_counts):
    """G-test as alternative to chi-square."""
    # Implementation
    pass
```

**Step 2**: Update `Experiment` model to store result
```python
self.g_test_result = None

def set_g_test_result(self, result):
    self.g_test_result = result
```

**Step 3**: Add menu option in `MenuSystem`
```python
def run_g_test(self):
    # Interactive workflow
    pass
```

#### 2. Adding Linkage Analysis

**Step 1**: Create new module `core/linkage.py`
```python
class LinkageAnalyzer:
    @staticmethod
    def detect_linkage(experiment):
        """Detect if genes are linked based on deviation from 9:3:3:1."""
        pass
    
    @staticmethod
    def calculate_recombination_frequency(observed_ratios):
        """Calculate map distance between linked genes."""
        pass
```

**Step 2**: Integrate into menu system

**Step 3**: Add linkage result to Experiment model

#### 3. Adding Database Support

**Option A**: SQLite (recommended for single user)
```python
class SQLiteStorage(ExperimentStorage):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        # CREATE TABLE statements
        pass
```

**Option B**: PostgreSQL (for multi-user)
```python
class PostgreSQLStorage(ExperimentStorage):
    # Use psycopg2 or SQLAlchemy
    pass
```

#### 4. Adding Export Formats

**Add to `visualization/` module**:
```python
class ReportGenerator:
    @staticmethod
    def generate_pdf_report(experiment):
        """Generate comprehensive PDF report."""
        # Use ReportLab or similar
        pass
    
    @staticmethod
    def export_to_csv(experiments):
        """Export multiple experiments to CSV."""
        pass
```

---

## Testing Guidelines

### Unit Testing Structure

```python
# tests/test_genetics.py
import unittest
from core.genetics import GeneticsCalculator
from models.genotype import Genotype
from models.allele import Allele

class TestGeneticsCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.alleles = {
            'E': Allele('E', 'Red', True),
            'e': Allele('e', 'White', False)
        }
    
    def test_monohybrid_cross(self):
        """Test simple Ee × ee cross."""
        parent1 = Genotype("Ee", self.alleles)
        parent2 = Genotype("ee", self.alleles)
        
        offspring = GeneticsCalculator.generate_punnett_square(
            parent1, parent2
        )
        
        self.assertEqual(len(offspring), 4)
        self.assertEqual(offspring.count("Ee"), 2)
        self.assertEqual(offspring.count("ee"), 2)
    
    def test_dihybrid_cross(self):
        """Test EeWw × EeWw cross."""
        # Test 9:3:3:1 ratio
        pass
```

### Test Categories

1. **Unit Tests**
   - Test individual methods in isolation
   - Mock external dependencies
   - Fast execution

2. **Integration Tests**
   - Test workflows (create → observe → analyze)
   - Use temporary file storage
   - Verify data persistence

3. **Statistical Tests**
   - Verify chi-square calculations
   - Test edge cases (zero counts, perfect ratios)
   - Compare to known statistical tables

4. **CLI Tests**
   - Simulate user input
   - Verify menu navigation
   - Test error handling

### Running Tests
```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_genetics.py

# Run with coverage
coverage run -m unittest discover tests/
coverage report
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'scipy'
**Solution**: Install dependencies
```bash
pip install scipy matplotlib
```

#### 2. File Permission Error when saving experiments
**Solution**: Check directory permissions
```bash
chmod 755 data/experiments/
```

#### 3. Chi-square test returns NaN
**Cause**: Zero expected counts
**Solution**: Validate expected counts before testing
```python
if any(count == 0 for count in expected_counts.values()):
    raise ValueError("Expected counts cannot be zero")
```

#### 4. Matplotlib backend issues
**Symptom**: "Cannot connect to X server"
**Solution**: Use Agg backend (already configured)
```python
import matplotlib
matplotlib.use('Agg')
```

#### 5. JSON Decode Error when loading experiment
**Cause**: Corrupted JSON file
**Solution**: Implement validation
```python
try:
    with open(filepath, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError:
    # Log error, skip file, or attempt recovery
    pass
```

---

## Performance Considerations

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Generate Punnett Square | O(4^n) | n = number of traits |
| Calculate Phenotypes | O(4^n) | Same as above |
| Chi-square Test | O(k) | k = number of phenotypes |
| Save Experiment | O(1) | Single file write |
| Load All Experiments | O(m) | m = number of experiments |
| Search Experiments | O(m) | Linear search |

### Optimization Strategies

1. **For Large Crosses (4+ traits)**:
   - Implement probabilistic sampling instead of full Punnett square
   - Use mathematical ratios directly when possible

2. **For Many Experiments**:
   - Implement database indexing
   - Add pagination to list views
   - Cache frequently accessed experiments

3. **For Visualization**:
   - Generate charts asynchronously
   - Cache generated images
   - Use lower DPI for previews

---

## Security Considerations

### Input Validation

**Always validate**:
- Genotype strings (only letters, correct format)
- Numeric inputs (positive integers)
- File paths (prevent directory traversal)

**Example**:
```python
def validate_genotype_string(s):
    if not re.match(r'^[A-Za-z]{2}(\s[A-Za-z]{2})*$', s):
        raise ValueError("Invalid genotype format")
```


---

---
