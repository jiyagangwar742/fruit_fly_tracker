# Complete Testing Guide for Fruit Fly Genetics Tracker

## Quick Start

1. **Create test data:**
   ```bash
   python create_test_experiment.py
   ```
   Type `y` when prompted.

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Follow the testing scenarios below**

---

## Test Experiments Created

The script creates 7 realistic experiments:

| ID | Name | Type | Purpose |
|----|------|------|---------|
| TEST_001 | Eye Color Inheritance | Ee × ee | Simple 1:1 ratio, good data |
| TEST_002 | Dihybrid Cross | EeWw × EeWw | Complex 9:3:3:1 ratio |
| TEST_003 | Test Cross | EeWw × eeww | 1:1:1:1 ratio for verification |
| TEST_004 | Problematic Cross | Ee × ee | BAD data - fails chi-square |
| TEST_005 | F1 Generation | Tt × Tt | Multi-gen series - 76% marker |
| TEST_006 | F2 Generation | Tt × Tt | Multi-gen series - 79% marker |
| TEST_007 | F3 Generation | TT × TT | Multi-gen series - 100% marker |

---

## Testing Scenarios

### Scenario 1: Basic Workflow ✅

**Test the complete user journey:**

1. Start application: `python main.py`
2. **[4] List all experiments**
   - ✓ Should see 7 experiments
   - ✓ TEST_001 through TEST_007
   - ✓ All show "Complete" status
   - ✓ Chi-square values displayed

3. **[3] View experiment results**
   - Select TEST_001
   - ✓ Should see experiment details
   - ✓ Expected counts: 250 / 250
   - ✓ Observed counts: 247 / 253
   - ✓ Chi-square: 0.072 PASS ✓
   - ✓ Notes displayed

4. **[5] Search experiments**
   - Search: "dihybrid"
   - ✓ Should find TEST_002

---

### Scenario 2: Basic Visualizations 📊

**Test the original 3 chart types:**

1. **Bar Chart:**
   - [6] Generate visualizations → [1]
   - Select TEST_001
   - ✓ Chart saved to exports/
   - ✓ Shows blue bars (expected) and orange bars (observed)
   - ✓ Very close values (247 vs 250, 253 vs 250)

2. **Pie Chart:**
   - [6] Generate visualizations → [2]
   - Select TEST_002
   - ✓ Chart saved to exports/
   - ✓ Shows 4 slices (all phenotype combinations)
   - ✓ Percentages shown on each slice

3. **Punnett Square:**
   - [6] Generate visualizations → [3]
   - Select TEST_001
   - ✓ 2×2 grid displayed
   - ✓ Parent genotypes labeled
   - ✓ All offspring genotypes shown (Ee, Ee, ee, ee)
   
   Try with TEST_002 (complex):
   - ✓ 4×4 grid displayed
   - ✓ 16 offspring combinations shown

---

### Scenario 3: Advanced Analysis Charts 📈

**Test the new analytical visualizations:**

1. **Deviation Plot:**
   - [6] → [5]
   - Select TEST_001
   - ✓ Shows +/- bars from zero line
   - ✓ Red eyes: -3 (red bar below zero)
   - ✓ White eyes: +3 (green bar above zero)
   - ✓ Values labeled on bars

2. **Chi-Square Contribution:**
   - [6] → [6]
   - Select TEST_004 (the failed experiment)
   - ✓ Shows which phenotypes cause high chi-square
   - ✓ Percentages shown (should be roughly 50/50 contribution)
   - ✓ Higher bars indicate problematic phenotypes

3. **Scatter Plot:**
   - [6] → [7]
   - Select TEST_002
   - ✓ Points plotted for each phenotype
   - ✓ Red diagonal line (perfect match)
   - ✓ Points close to diagonal = good data
   - ✓ Phenotype labels on each point

4. **Confidence Intervals:**
   - [6] → [8]
   - Select TEST_001
   - ✓ Blue bars with error bars (expected)
   - ✓ Orange bars (observed)
   - ✓ Observed bars within error bars = good

---

### Scenario 4: Distribution Charts 📉

**Test distribution visualizations:**

1. **Stacked Bar:**
   - [6] → [9]
   - Select TEST_002
   - ✓ Shows distribution across phenotypes

2. **Percentage Bar (Horizontal):**
   - [6] → [10]
   - Select TEST_001
   - ✓ Horizontal bars showing percentages
   - ✓ Expected vs Observed side by side
   - ✓ Both should be close to 50%

3. **Allele Frequency Pie:**
   - [6] → [11]
   - Select TEST_002
   - ✓ Shows proportion of E, e, W, w alleles
   - ✓ Percentages sum to 100%

4. **Heatmap:**
   - [6] → [12]
   - Select TEST_002
   - ✓ Color intensity shows frequency
   - ✓ Numbers displayed in cells

---

### Scenario 5: Multi-Experiment Charts 🔄

**Test comparing multiple experiments:**

1. **Comparison Table:**
   - [6] → [13]
   - When prompted, type: `5,6,7` (TEST_005, TEST_006, TEST_007)
   - ✓ Table image shows all 3 experiments
   - ✓ Dates, parents, chi-square values shown
   - ✓ Saved as experiments_comparison.png

2. **Multi-Generation Line Graph:**
   - [6] → [14]
   - Select experiments: `5,6,7`
   - Trait to track: `CRISPR Marker Present`
   - ✓ Line graph shows 3 generations
   - ✓ Frequency increases: ~76% → ~79% → 100%
   - ✓ Clear upward trend visible
   - ✓ This simulates your MARC research progress!

3. **Generation Comparison:**
   - [6] → [15]
   - Select: `5,6,7`
   - ✓ Grouped bar chart
   - ✓ Shows both phenotypes across all generations
   - ✓ "CRISPR Marker Present" increasing
   - ✓ "No Marker" decreasing

---

### Scenario 6: Special Charts ⭐

**Test special visualization types:**

1. **Summary Dashboard:**
   - [6] → [16]
   - Select TEST_002
   - ✓ 4-panel layout:
     - Top-left: Bar chart
     - Top-right: Pie chart
     - Bottom-left: Deviation plot
     - Bottom-right: Statistical summary
   - ✓ Professional layout for presentations

2. **Cumulative Count:**
   - [6] → [17]
   - Select TEST_001
   - ✓ Lines show running totals
   - ✓ Expected lines (dashed)
   - ✓ Observed lines (solid)

---

### Scenario 7: Generate ALL Charts 🎨

**Test batch generation:**

1. [6] → [18] Generate ALL charts
2. Select TEST_002 (dihybrid cross)
3. ✓ System generates 12+ charts:
   - ✓ Punnett Square
   - ✓ Bar chart
   - ✓ Pie chart
   - ✓ Deviation plot
   - ✓ Scatter plot
   - ✓ Confidence intervals
   - ✓ Stacked bar
   - ✓ Percentage bar
   - ✓ Allele frequency
   - ✓ Heatmap
   - ✓ Dashboard
   - ✓ Cumulative count
   - ✓ Chi-square contribution

4. Check exports/ folder:
   - ✓ All files present with TEST_002 prefix
   - ✓ File sizes reasonable (not empty)

---

### Scenario 8: PDF Export 📄

**Test PDF report generation:**

1. **Simple Experiment PDF:**
   - [7] Export to PDF
   - Select TEST_001
   - ✓ PDF created in exports/
   - ✓ Open PDF and verify:
     - Title and experiment name
     - Experiment details table
     - Allele definitions table
     - Expected ratios table
     - Punnett Square image
     - Observed results table
     - Statistical analysis section
     - Bar chart
     - Pie chart
     - Notes section
     - Footer with date/time

2. **Complex Experiment PDF:**
   - [7] Export to PDF
   - Select TEST_002 (dihybrid)
   - ✓ Check Punnett Square is 4×4 grid
   - ✓ Check all 4 phenotypes in tables
   - ✓ Charts show 4 categories

3. **Failed Experiment PDF:**
   - [7] Export to PDF
   - Select TEST_004
   - ✓ Chi-square section shows "FAIL ✗"
   - ✓ Interpretation mentions deviation
   - ✓ Charts clearly show imbalance

---

### Scenario 9: Edge Cases 🧪

**Test error handling:**

1. **View Incomplete Experiment:**
   - Create new experiment without observations
   - Try to view results
   - ✓ Shows "No observations recorded yet"

2. **Generate Charts Without Observations:**
   - Try [6] → [1] (bar chart) on incomplete experiment
   - ✓ Error: "Experiment must have observations"

3. **Punnett Square (Always Works):**
   - Try [6] → [3] on ANY experiment
   - ✓ Works even without observations

4. **Invalid Menu Choices:**
   - Type "99" in any menu
   - ✓ Error message displayed
   - ✓ Returns to menu (doesn't crash)

---

### Scenario 10: Data Persistence 💾

**Test that data survives restart:**

1. Exit application (choice [0])
2. Restart: `python main.py`
3. [4] List all experiments
4. ✓ All 7 TEST experiments still there
5. [3] View TEST_001
6. ✓ All data intact (observations, chi-square, notes)
7. Check data/experiments/ folder:
   - ✓ 7 JSON files present
   - ✓ Open one in text editor
   - ✓ Readable JSON structure

---

## Expected Results Summary

### ✅ Successful Tests Should Show:

**TEST_001 (Simple cross):**
- Chi-square: 0.072 (PASS)
- Deviation: ±3 flies
- Very close to expected 1:1 ratio

**TEST_002 (Dihybrid):**
- Chi-square: ~0.5-1.0 (PASS)
- 9:3:3:1 ratio approximately followed
- 4 distinct phenotype groups

**TEST_003 (Testcross):**
- Chi-square: ~0.5 (PASS)
- 1:1:1:1 ratio (4 equal groups)

**TEST_004 (Failed):**
- Chi-square: ~31 (FAIL) ❌
- Clearly shows in deviation plot
- Red eyes much lower, white eyes much higher
- This is EXPECTED - shows error detection works!

**TEST_005, 006, 007 (Multi-gen):**
- Progressive increase in marker frequency
- Line graph shows clear upward trend
- F3 reaches 100% marker presence

### 📊 Chart Files Created:

After running all tests, your exports/ folder should have:
- ~50+ PNG image files
- ~7 PDF files
- All clearly named with experiment IDs
- File sizes: 50KB - 500KB each

---

## Common Issues & Solutions

### Issue: Import errors when running create_test_experiment.py
**Solution:** Make sure you're in the project root directory:
```bash
cd fruit_fly_tracker
python create_test_experiment.py
```

### Issue: "No module named 'models'"
**Solution:** Check your folder structure matches the design:
```
fruit_fly_tracker/
├── create_test_experiment.py  ← new file here
├── main.py
├── models/
├── core/
└── ...
```

### Issue: Charts not opening automatically
**Solution:** Charts are saved to exports/ folder. Open them manually:
- macOS: `open exports/TEST_001_bar_chart.png`
- Windows: `start exports/TEST_001_bar_chart.png`
- Linux: `xdg-open exports/TEST_001_bar_chart.png`

### Issue: PDF missing charts
**Solution:** Generate charts BEFORE creating PDF:
1. [6] Generate visualizations → [18] ALL charts
2. Then [7] Export to PDF

### Issue: Multi-generation graph shows error
**Solution:** Make sure you select experiments 5, 6, 7 in order
- Type exactly: `5,6,7`
- Trait name exactly: `CRISPR Marker Present`

---

## Performance Benchmarks

**Expected Timings:**

| Operation | Time |
|-----------|------|
| Create 7 test experiments | 1-2 seconds |
| Generate single chart | 0.5-1 second |
| Generate all 12 charts | 5-8 seconds |
| Create PDF report | 2-3 seconds |
| Load experiment list | <0.1 seconds |

If operations take significantly longer, check:
- Disk space available
- No other programs using exports/ folder
- Computer has sufficient RAM

---

## Clean Up After Testing

To start fresh:

```bash
# Remove test experiments
rm data/experiments/TEST_*.json

# Remove generated charts
rm exports/TEST_*.*

# Keep real experiments
# (They won't have TEST_ prefix)
```

---

## Next Steps

After successful testing:

1. ✅ **Create your real experiments** using the CLI
2. ✅ **Use visualization options** for your MARC research
3. ✅ **Generate PDFs** for your Stanford presentation
4. ✅ **Track multi-generation progress** with line graphs

**For your Stanford presentation, use:**
- Summary Dashboard [16] - Professional 4-panel overview
- Multi-Generation Line Graph [14] - Shows progress over time
- Punnett Square [3] - Clear genetic cross diagrams
- PDF Export [7] - Complete professional report

---

## Questions to Verify Understanding

After testing, you should be able to answer:

1. ✓ How do I create a new experiment?
2. ✓ How do I add observations to an existing experiment?
3. ✓ What does a passing chi-square test look like?
4. ✓ How can I compare multiple experiments?
5. ✓ How do I generate a PDF report?
6. ✓ Which charts show deviation from expected most clearly?
7. ✓ How do I track a trait across generations?

If you can't answer these, review the relevant scenarios above!

---

**🎉 Happy Testing!**

You now have a complete, working genetics analysis system with 15+ visualization types and professional PDF reports!