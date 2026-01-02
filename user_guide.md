# Fruit Fly Genetics Tracker - Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Workflow](#basic-workflow)
3. [Creating Your First Experiment](#creating-your-first-experiment)
4. [Adding Observations](#adding-observations)
5. [Viewing Results](#viewing-results)
6. [Managing Multiple Experiments](#managing-multiple-experiments)
7. [Generating Visualizations](#generating-visualizations)
8. [Understanding Statistical Results](#understanding-statistical-results)
9. [Common Use Cases](#common-use-cases)
10. [Frequently Asked Questions](#frequently-asked-questions)
11. [Troubleshooting](#troubleshooting)

---

## Getting Started

### What is This Tool?

The Fruit Fly Genetics Tracker helps you:
- **Predict** what offspring you'll get from genetic crosses
- **Record** your actual experimental observations
- **Analyze** whether your results match genetic theory
- **Visualize** your data with professional charts
- **Track** multiple experiments over time

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: ~50 MB for software + space for your data
- **Required Software**: Python with pip package manager

### Installation

#### Step 1: Install Python
If you don't have Python installed:
- **Windows/Mac**: Download from [python.org](https://python.org)
- **Linux**: Usually pre-installed, or use `sudo apt install python3`

Check your installation:
```bash
python --version
# Should show: Python 3.8 or higher
```

#### Step 2: Install Required Libraries
```bash
pip install scipy matplotlib
```

#### Step 3: Download the Program
Place all program files in a folder, for example:
```
/Users/jiya/fruit_fly_tracker/
```

#### Step 4: Run the Program
```bash
cd /Users/jiya/fruit_fly_tracker/
python main.py
```

You should see:
```
============================================================
        FRUIT FLY GENETICS TRACKER v1.0
              By Jiya Gangwar
============================================================

Loading experiments... Found 0 experiments.

MAIN MENU:
[1] Create new experiment
[2] Add observation data
...
```

---

## Basic Workflow

### The Complete Process

```
┌─────────────────────────────────────────────────────────┐
│ 1. PLAN YOUR CROSS                                      │
│    - Decide which parents to breed                      │
│    - Note their genotypes                               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. CREATE EXPERIMENT IN TRACKER                         │
│    - Enter experiment name                              │
│    - Enter parent genotypes                             │
│    - Define what each allele means                      │
│    - Get automatic predictions                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. PERFORM ACTUAL LAB WORK                              │
│    - Breed the flies                                    │
│    - Wait for offspring                                 │
│    - Count phenotypes under microscope                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. ENTER YOUR OBSERVATIONS                              │
│    - Select your experiment                             │
│    - Enter actual counts                                │
│    - Get automatic statistical analysis                 │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 5. REVIEW RESULTS                                       │
│    - View statistical test results                      │
│    - Generate charts for reports                        │
│    - Add notes about your findings                      │
└─────────────────────────────────────────────────────────┘
```

---

## Creating Your First Experiment

### Example: Simple Eye Color Cross

Let's create an experiment testing eye color inheritance.

#### What You Need Before Starting
- Parent genotypes (e.g., "Ee" and "ee")
- Knowledge of what each allele represents
- Estimate of how many flies you'll count

#### Step-by-Step Instructions

**1. Start the program and select option 1:**
```
Enter your choice: 1
```

**2. Name your experiment:**
```
Experiment name: Eye_Color_Test_F2
```
*Tip: Use descriptive names that include what you're testing and which generation.*

**3. Enter parent genotypes:**
```
Parent 1 genotype: Ee
Parent 2 genotype: ee
```

**Format Guidelines:**
- Use capital letters for dominant alleles (E, W, B)
- Use lowercase for recessive alleles (e, w, b)
- Separate multiple traits with spaces: "Ee Ww" for two traits
- Each gene needs exactly 2 alleles: ✓ "Ee" ✗ "E" ✗ "Eee"

**4. Define what each allele means:**
```
Gene 1 (from 'Ee'):
  E = Red eyes
  e = White eyes

Are these definitions correct? (y/n): y
```

**5. Enter expected count:**
```
How many offspring do you expect to count? 500
```
*Tip: Enter a realistic number based on your experimental capacity.*

**6. Review the predictions:**
```
═══════════════════════════════════════════════
CALCULATING EXPECTED RATIOS...
═══════════════════════════════════════════════

Punnett Square Generated:

        e       e
    ┌───────┬───────┐
  E │  Ee   │  Ee   │
    ├───────┼───────┤
  e │  ee   │  ee   │
    └───────┴───────┘

EXPECTED PHENOTYPE RATIOS:
  • Red eyes: 50% (2/4)
  • White eyes: 50% (2/4)

EXPECTED COUNTS (out of 500):
  • Red eyes: 250 flies
  • White eyes: 250 flies

✓ Experiment "Eye_Color_Test_F2" created successfully!
  Experiment ID: EXP_001
```

**7. Add optional notes:**
```
Notes (optional, press Enter to skip): F2 generation, testing Mendelian inheritance
```

**Done!** Your experiment is now saved and ready for observations.

---

## Adding Observations

After you've counted your actual flies, enter the data:

### Step-by-Step Instructions

**1. Select option 2 from main menu:**
```
Enter your choice: 2
```

**2. Select your experiment:**
```
Available experiments:
[1] ✓ Eye_Color_Test_F2 (EXP_001) - 2026-01-15

Select experiment number: 1
```

**3. Review expected counts:**
```
Loading experiment: Eye_Color_Test_F2
Expected counts:
  • Red eyes: 250 flies
  • White eyes: 250 flies
```

**4. Enter your actual counts:**
```
ENTER OBSERVED COUNTS:
Red eyes: 247
White eyes: 253

Total counted: 500 flies
Match expected total? ✓
```

**Important**: 
- Total observed should match total expected
- Count carefully under the microscope
- Exclude flies with damaged or unclear phenotypes

**5. Confirm your data:**
```
Would you like to save this? (y/n): y
```

**6. Automatic analysis runs:**
```
═══════════════════════════════════════════════
RUNNING CHI-SQUARE ANALYSIS...
═══════════════════════════════════════════════

Chi-square value: 0.072
P-value: 0.788

RESULT: ✓ PASS
Your observed data matches expected ratios.

✓ Observations saved successfully!
```

---

## Viewing Results

### Detailed Results View

**1. Select option 3 from main menu:**
```
Enter your choice: 3
```

**2. Select your experiment:**
```
Select experiment number: 1
```

**3. View complete report:**
```
══════════════════════════════════════════════
EXPERIMENT DETAILS
══════════════════════════════════════════════

ID: EXP_001
Name: Eye_Color_Test_F2
Created: 2026-01-15 10:30
Status: Complete
Parents: Ee × ee

EXPECTED RATIOS
┌─────────────┬──────────┬────────────┐
│ Phenotype   │ Expected │ Percentage │
├─────────────┼──────────┼────────────┤
│ Red eyes    │   250.0  │   50.0%    │
│ White eyes  │   250.0  │   50.0%    │
└─────────────┴──────────┴────────────┘

OBSERVED COUNTS
┌─────────────┬──────────┬──────────┬────────────┐
│ Phenotype   │ Expected │ Observed │ Difference │
├─────────────┼──────────┼──────────┼────────────┤
│ Red eyes    │   250.0  │   247    │   -3.0     │
│ White eyes  │   250.0  │   253    │   +3.0     │
└─────────────┴──────────┴──────────┴────────────┘

STATISTICAL ANALYSIS
────────────────────
Chi-square value: 0.072
P-value: 0.788
Result: ✓ PASS

Interpretation: Your data matches expected ratios.
The observed variation is within normal random chance.
```

---

## Managing Multiple Experiments

### Listing All Experiments

**Select option 4 from main menu:**
```
Enter your choice: 4
```

**View all experiments:**
```
══════════════════════════════════════════════
ALL EXPERIMENTS
══════════════════════════════════════════════

Total experiments: 5
Completed: 3  |  In Progress: 2

┌────┬────────────────────────┬────────────┬──────────┬──────────┐
│ ID │ Name                   │ Date       │ Status   │ Chi²     │
├────┼────────────────────────┼────────────┼──────────┼──────────┤
│ 05 │ CRISPR_Marker_Check    │ 2026-01-18 │ Progress │ ---      │
│ 04 │ Wing_Shape_Analysis    │ 2026-01-17 │ Complete │ 1.24 ✓   │
│ 03 │ Double_Mutant_Test     │ 2026-01-16 │ Complete │ 12.4 ✗   │
│ 02 │ Body_Color_Cross       │ 2026-01-15 │ Complete │ 0.45 ✓   │
│ 01 │ Eye_Color_Test_F2      │ 2026-01-15 │ Progress │ ---      │
└────┴────────────────────────┴────────────┴──────────┴──────────┘

✓ = Passed chi-square test
✗ = Failed chi-square test (investigate!)
```

### Searching for Experiments

**Select option 5 from main menu:**
```
Enter your choice: 5
```

**Search by name:**
```
Enter search term: wing

Found 2 matching experiment(s):
  ✓ Wing_Shape_Analysis (EXP_004)
  ⏳ Wing_Mutant_Test_F3 (EXP_008)
```

---

## Generating Visualizations

### Creating Charts for Your Reports

**1. Select option 6 from main menu:**
```
Enter your choice: 6
```

**2. Select experiment:**
```
Select experiment number: 1
```

**3. Choose chart type:**
```
Select chart type:
[1] Bar chart (Expected vs Observed)
[2] Pie chart (Phenotype distribution)
[3] Both

Enter choice: 3
```

**4. Charts are generated:**
```
Generating visualizations...
✓ Bar chart saved: exports/EXP_001_bar_chart.png
✓ Pie chart saved: exports/EXP_001_pie_chart.png

Charts saved successfully!
```

### Understanding the Charts

#### Bar Chart
- **Blue bars**: What you expected based on genetics
- **Orange bars**: What you actually observed
- **Close bars**: Good match, genetics worked as predicted
- **Different bars**: Possible experimental error or different mechanism

#### Pie Chart
- Shows percentage breakdown of your population
- Useful for presentations
- Clear visual of trait distribution

### Using Charts in Reports

**For Lab Reports:**
1. Find charts in `exports/` folder
2. Insert into your document
3. Reference in text: "As shown in Figure 1..."

**For Presentations:**
1. Import PNG files into PowerPoint/Keynote
2. Add caption explaining the cross
3. Discuss chi-square results

---

## Understanding Statistical Results

### What is Chi-Square Testing?

Chi-square tests answer the question: **"Is my data close enough to predictions, or did something unusual happen?"**

### Reading the Results

#### Successful Result (Pass)
```
Chi-square value: 0.072
P-value: 0.788
Result: ✓ PASS
```

**What this means:**
- Your observed data matches expected ratios
- Differences are due to normal random variation
- Your genetic hypothesis is supported
- Experiment was successful

#### Failed Result (Investigate)
```
Chi-square value: 12.4
P-value: 0.002
Result: ✗ FAIL
```

**What this means:**
- Significant deviation from expected ratios
- Something unusual occurred
- **Possible causes:**
  - Counting error (recount your flies)
  - Selection bias (some phenotypes easier to spot)
  - Wrong genetic model (maybe genes are linked)
  - Flies died non-randomly
  - Experimental contamination

### What to Do When You Fail

**Don't panic!** Failed chi-square tests are learning opportunities.

**Step 1: Check your counting**
- Recount the flies carefully
- Check if any were miscategorized
- Verify total count

**Step 2: Review your predictions**
- Are your parent genotypes correct?
- Did you define dominance correctly?
- Could genes be linked (on same chromosome)?

**Step 3: Consider biological factors**
- Did some phenotypes have survival disadvantage?
- Was temperature/humidity abnormal?
- Any contamination in your stocks?

**Step 4: Discuss with advisor**
- Explain your results
- Discuss alternative hypotheses
- Plan follow-up experiments

### Statistical Terms Explained

- **Chi-square value (χ²)**: How far your data is from predictions
  - Low values (< 3.84): Good match
  - High values (> 3.84): Poor match

- **P-value**: Probability your results are due to chance
  - High p-value (> 0.05): Likely just random variation
  - Low p-value (< 0.05): Something systematic is different

- **Degrees of freedom**: Number of phenotype categories minus 1
  - For 2 phenotypes: df = 1
  - For 4 phenotypes: df = 3

- **Alpha (α)**: Strictness of the test (usually 0.05 = 95% confidence)

---

## Common Use Cases

### Use Case 1: Simple Monohybrid Cross

**Scenario**: Testing whether eye color follows Mendelian inheritance

**Parents**: Ee (red eyes) × ee (white eyes)

**Expected Results**: 1:1 ratio (50% red, 50% white)

**In the program:**
```
Parent 1: Ee
Parent 2: ee
Expected: 250 red, 250 white (out of 500)
```

**When to use:** Testing single trait inheritance

---

### Use Case 2: Dihybrid Cross

**Scenario**: Testing two traits simultaneously (eye color and wing shape)

**Parents**: EeWw × EeWw

**Expected Results**: 9:3:3:1 ratio
- 9/16 red eyes, normal wings
- 3/16 red eyes, vestigial wings
- 3/16 white eyes, normal wings
- 1/16 white eyes, vestigial wings

**In the program:**
```
Parent 1: Ee Ww
Parent 2: Ee Ww
Expected: 225, 75, 75, 25 (out of 400)
```

**When to use:** Testing independent assortment of two genes

---

### Use Case 3: Test Cross

**Scenario**: Determining if a fly with dominant phenotype is homozygous or heterozygous

**Parents**: E? (unknown genotype) × ee (tester)

**Strategy**:
1. If unknown is EE: All offspring will be Ee (100% red)
2. If unknown is Ee: Offspring will be 50% Ee, 50% ee

**In the program:**
```
# Hypothesis 1: Unknown is EE
Parent 1: EE
Parent 2: ee
Expected: 100% red

# Hypothesis 2: Unknown is Ee
Parent 1: Ee
Parent 2: ee
Expected: 50% red, 50% white
```

**After experiment**: Compare which prediction matches your data

---

### Use Case 4: CRISPR Marker Verification

**Scenario**: Confirming flies have desired CRISPR modifications

**Parents**: T?B? × TT BB

**Goal**: Identify flies that are TT BB (homozygous for both markers)

**Strategy**:
1. Cross suspected flies with known homozygotes
2. If all offspring show dominant traits → parent was homozygous
3. If offspring are mixed → parent was heterozygous

---


### Before Creating Experiments

**✓ Plan ahead**
- Know your parent genotypes
- Understand expected ratios
- Have allele definitions ready

**✓ Use clear names**
- Include trait being tested
- Include generation (F1, F2, F3)
- Include date or trial number
- Good: "Eye_Color_F2_Trial3_Jan15"
- Bad: "Experiment1"

**✓ Estimate realistically**
- Count enough flies for statistical power (minimum ~100)
- Don't overestimate your capacity
- More flies = more reliable results

### During Lab Work

**✓ Count carefully**
- Use good lighting
- Take breaks to avoid eye strain
- Double-check ambiguous phenotypes
- Keep track as you count

**✓ Exclude damaged flies**
- Don't count flies with unclear phenotypes
- Note exclusions in your notes
- Be consistent across all counts

**✓ Record conditions**
- Temperature
- Humidity
- Any unusual observations
- Add as notes in the experiment

### After Analysis

**✓ Understand your results**
- Don't just accept pass/fail
- Look at the actual numbers
- Consider biological implications

**✓ Document everything**
- Use the notes field extensively
- Explain any anomalies
- Record follow-up plans

**✓ Save visualizations**
- Generate charts for all complete experiments
- Keep for lab reports and presentations
- Charts are saved in `exports/` folder

### Organization Tips

**✓ Consistent naming convention**
```
Cross_#_TraitName_Generation_Date
Example: Cross_7_EyeColor_F2_Jan15
```

**✓ Regular backups**
- Copy `data/experiments/` folder regularly
- Keep backup on external drive or cloud
- Your data is in JSON files - easy to backup

**✓ Progressive numbering**
- Let the program auto-generate IDs (EXP_001, etc.)
- Keep experiments in chronological order
- Don't delete old experiments

---

## Frequently Asked Questions

### General Questions

**Q: Do I need to be online to use this?**
A: No, the program works completely offline on your computer.

**Q: Can I use this on multiple computers?**
A: Yes, just copy the entire program folder and your data will come with it.

**Q: How many experiments can I track?**
A: Unlimited. Each experiment is a small JSON file (~2-5 KB).

**Q: Can multiple people use this?**
A: The current version is single-user. For multi-user, database version would be needed.

### Creating Experiments

**Q: What if I have more than 2 traits?**
A: Enter genotypes like "Ee Ww Bb" (3 traits). Separate each gene pair with a space.

**Q: Can I use different letters for alleles?**
A: Yes! Any letter works. Capital = dominant, lowercase = recessive.

**Q: What if I made a mistake in the genotype?**
A: Delete the experiment (option 7) and create a new one. Or manually edit the JSON file.

**Q: My cross produces unequal ratios (not 3:1 or 9:3:3:1). Is that okay?**
A: Yes! The program handles any ratio. Just enter the correct genotypes.

### Adding Observations

**Q: My total observed doesn't match expected. Is that a problem?**
A: Yes, totals should match. If you counted more/fewer flies, recreate the experiment with correct expected count.

**Q: Can I update observations after saving?**
A: Yes, select "Add observations" again and choose to overwrite existing data.

**Q: What if I have zero flies of a certain phenotype?**
A: That's okay, enter 0. The statistical test still works (though a fail is likely).

### Results and Statistics

**Q: My chi-square test failed. Is my experiment ruined?**
A: No! Failures are informative. Review the "What to Do When You Fail" section above.

**Q: What's a "good" chi-square value?**
A: For 2 phenotypes: Less than 3.84. For 4 phenotypes: Less than 7.81.

**Q: Can I change the significance level (alpha)?**
A: Currently set to 0.05 (95% confidence). To change, edit `config.py`.

### Visualizations

**Q: Where are my charts saved?**
A: In the `exports/` folder inside your program directory.

**Q: Can I change chart colors or style?**
A: Yes, edit `visualization/charts.py` and modify the plotting code.

**Q: Charts won't generate. What's wrong?**
A: Make sure matplotlib is installed: `pip install matplotlib`

### Data Management

**Q: Where is my data stored?**
A: In `data/experiments/` as JSON files. One file per experiment.

**Q: Can I edit data manually?**
A: Yes! The JSON files are human-readable. Use a text editor carefully.

**Q: How do I backup my data?**
A: Copy the entire `data/` folder to a safe location.

**Q: Can I export to Excel?**
A: Not currently built-in, but JSON files can be imported into Excel.

---

## Troubleshooting

### Program Won't Start

**Problem**: "python: command not found"
**Solution**: Python isn't installed or not in PATH. Reinstall Python and check "Add to PATH" option.

**Problem**: "No module named 'scipy'"
**Solution**: Install required libraries: `pip install scipy matplotlib`

**Problem**: "Permission denied" when running
**Solution**: On Mac/Linux, make file executable: `chmod +x main.py`

### Creating Experiments

**Problem**: "Invalid genotype format"
**Solution**: 
- Each gene must have exactly 2 alleles: "Ee" not "E"
- Separate genes with spaces: "Ee Ww" not "EeWw"
- Only use letters: "Ee" not "E1"

**Problem**: Program crashes when defining alleles
**Solution**: Press Enter after each definition. Don't leave descriptions blank.

### Adding Observations

**Problem**: Can't find my experiment in the list
**Solution**: 
- Check if you created it (option 4 to list all)
- Make sure you're in the right directory
- Use search function (option 5)

**Problem**: "Totals don't match" error
**Solution**: Sum of observed counts must equal expected total. Recount or adjust expected total.

### Statistical Analysis

**Problem**: Chi-square is "inf" or "NaN"
**Solution**: You have zero in expected counts. This shouldn't happen with proper setup. Check your genotypes.

**Problem**: Every experiment fails chi-square
**Solution**: 
- Verify your counting method
- Check phenotype definitions
- Review dominance rules

### Visualizations

**Problem**: "Matplotlib backend error"
**Solution**: Already handled by `matplotlib.use('Agg')` in code.

**Problem**: Charts are blank or malformed
**Solution**: 
- Ensure observations are entered
- Try recreating the chart
- Check if file was partially saved

**Problem**: Can't open generated charts
**Solution**: 
- Navigate to `exports/` folder manually
- Open .png files with any image viewer
- On Mac: `open exports/EXP_001_bar_chart.png`

### Data Issues

**Problem**: Lost all my data!
**Solution**: 
- Check `data/experiments/` folder
- Look for .json files
- Restore from backup if available

**Problem**: Corrupted experiment file
**Solution**: 
- Try opening the .json file in a text editor
- Fix any syntax errors
- Or delete and recreate experiment

**Problem**: Duplicate experiment IDs
**Solution**: Shouldn't happen. If it does, manually rename one file.

### Getting Help

**If problems persist:**
1. Check error message carefully
2. Review relevant section in this guide
3. Try a simpler example to isolate issue
4. Consult with your research advisor
5. Report bug to developer (include error message)

---

## Quick Reference Card

### Common Commands

| Action | Menu Option |
|--------|-------------|
| Create experiment | 1 |
| Add observations | 2 |
| View results | 3 |
| List all | 4 |
| Search | 5 |
| Make charts | 6 |
| Delete | 7 |
| Quit | 0 |

### Genotype Format

| Format | Meaning |
|--------|---------|
| `Ee` | One trait, heterozygous |
| `EE` | One trait, homozygous dominant |
| `ee` | One trait, homozygous recessive |
| `Ee Ww` | Two traits |
| `Ee Ww Bb` | Three traits |

### Statistical Interpretation

| Chi² Value | Interpretation |
|------------|----------------|
| < 3.84 (2 phenotypes) | Good match ✓ |
| > 3.84 (2 phenotypes) | Significant deviation ✗ |
| < 7.81 (4 phenotypes) | Good match ✓ |
| > 7.81 (4 phenotypes) | Significant deviation ✗ |

### File Locations

| What | Where |
|------|-------|
| Experiments | `data/experiments/` |
| Charts | `exports/` |
| Program | Main folder |



## Example Session

Here's a complete example from start to finish:

```
$ python main.py

============================================================
        FRUIT FLY GENETICS TRACKER v1.0
============================================================

MAIN MENU:
[1] Create new experiment
...

Enter your choice: 1

--- CREATE NEW EXPERIMENT ---

Experiment name: Eye_Color_Test
Parent 1 genotype: Ee
Parent 2 genotype: ee

Define alleles:
E = Red eyes
e = White eyes

Expected count: 500

✓ Experiment created!
Expected:
  Red eyes: 250
  White eyes: 250

Press Enter to return...

[Back at main menu]

Enter your choice: 2

--- ADD OBSERVATIONS ---

Select experiment: 1

Enter observed counts:
Red eyes: 247
White eyes: 253

Chi-square: 0.072
P-value: 0.788
Result: PASS ✓

✓ Saved successfully!

[Back at main menu]

Enter your choice: 6

--- GENERATE CHARTS ---

Select experiment: 1
Chart type: 3 (Both)

✓ Bar chart saved
✓ Pie chart saved

[Back at main menu]

Enter your choice: 0

Goodbye!
