# ============================================================================
# FILE: create_test_experiment.py (NEW FILE - Place in root directory)
# Script to create realistic test experiments for testing
# ============================================================================

"""
This script creates test experiments with realistic data so you can test
all the visualizations and reports.

Run this script: python create_test_experiment.py
"""

from models.experiment import Experiment
from models.allele import Allele
from core.genetics import GeneticsCalculator
from core.statistics import StatisticalAnalyzer
from storage.file_storage import ExperimentStorage
import random

def create_simple_monohybrid_test():
    """
    Create a simple Ee × ee cross (classic Mendelian genetics).
    This is like testing eye color inheritance.
    """
    print("\n" + "="*60)
    print("Creating Test Experiment 1: Simple Monohybrid Cross")
    print("="*60)
    
    # Define alleles
    allele_definitions = {
        'E': Allele('E', 'Red eyes', is_dominant=True),
        'e': Allele('e', 'White eyes', is_dominant=False)
    }
    
    # Create experiment
    experiment = Experiment(
        experiment_id="TEST_001",
        name="Eye Color Inheritance - F1 Cross",
        parent1_string="Ee",
        parent2_string="ee",
        allele_definitions=allele_definitions,
        total_expected=500,
        notes="Test experiment for Mendelian genetics. Expected 1:1 ratio of red to white eyes."
    )
    
    # Calculate expected ratios
    offspring = GeneticsCalculator.generate_punnett_square(
        experiment.parent1, experiment.parent2
    )
    
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(
        offspring, experiment.allele_definitions
    )
    
    expected_counts = GeneticsCalculator.calculate_expected_counts(
        phenotype_ratios, experiment.total_expected
    )
    
    experiment.set_expected_counts(expected_counts)
    
    # Add realistic observations (with slight random variation)
    # Expected: 250 red, 250 white
    # Observed: Add realistic counting variation
    observed_counts = {
        'Red eyes': 247,  # Close to expected 250
        'White eyes': 253  # Close to expected 250
    }
    
    experiment.add_observations(observed_counts)
    
    # Run statistical analysis
    chi_result = StatisticalAnalyzer.chi_square_test(
        experiment.expected_counts,
        experiment.observed_counts
    )
    
    experiment.set_chi_square_result(chi_result)
    
    # Save
    storage = ExperimentStorage()
    storage.save_experiment(experiment)
    
    print(f"✓ Created: {experiment.name}")
    print(f"  ID: {experiment.experiment_id}")
    print(f"  Parents: {experiment.parent1} × {experiment.parent2}")
    print(f"  Expected: {experiment.expected_counts}")
    print(f"  Observed: {experiment.observed_counts}")
    print(f"  Chi-square: {chi_result['chi_square']} (Pass: {chi_result['passed']})")
    
    return experiment


def create_dihybrid_test():
    """
    Create EeWw × EeWw cross (dihybrid cross).
    Tests eye color AND wing shape inheritance.
    Expected 9:3:3:1 ratio.
    """
    print("\n" + "="*60)
    print("Creating Test Experiment 2: Dihybrid Cross")
    print("="*60)
    
    # Define alleles for TWO traits
    allele_definitions = {
        'E': Allele('E', 'Red eyes', is_dominant=True),
        'e': Allele('e', 'White eyes', is_dominant=False),
        'W': Allele('W', 'Normal wings', is_dominant=True),
        'w': Allele('w', 'Vestigial wings', is_dominant=False)
    }
    
    # Create experiment
    experiment = Experiment(
        experiment_id="TEST_002",
        name="Dihybrid Cross - Eye Color and Wing Shape",
        parent1_string="Ee Ww",
        parent2_string="Ee Ww",
        allele_definitions=allele_definitions,
        total_expected=640,
        notes="Classic dihybrid cross. Expected 9:3:3:1 ratio. This tests independent assortment."
    )
    
    # Calculate expected ratios
    offspring = GeneticsCalculator.generate_punnett_square(
        experiment.parent1, experiment.parent2
    )
    
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(
        offspring, experiment.allele_definitions
    )
    
    expected_counts = GeneticsCalculator.calculate_expected_counts(
        phenotype_ratios, experiment.total_expected
    )
    
    experiment.set_expected_counts(expected_counts)
    
    # Add realistic observations for 9:3:3:1 ratio
    # Expected: 360 red/normal, 120 red/vestigial, 120 white/normal, 40 white/vestigial
    observed_counts = {
        'Red eyes, Normal wings': 355,      # Close to 360
        'Red eyes, Vestigial wings': 118,   # Close to 120
        'White eyes, Normal wings': 125,    # Close to 120
        'White eyes, Vestigial wings': 42   # Close to 40
    }
    
    experiment.add_observations(observed_counts)
    
    # Run statistical analysis
    chi_result = StatisticalAnalyzer.chi_square_test(
        experiment.expected_counts,
        experiment.observed_counts
    )
    
    experiment.set_chi_square_result(chi_result)
    
    # Save
    storage = ExperimentStorage()
    storage.save_experiment(experiment)
    
    print(f"✓ Created: {experiment.name}")
    print(f"  ID: {experiment.experiment_id}")
    print(f"  Parents: {experiment.parent1} × {experiment.parent2}")
    print(f"  Expected: {experiment.expected_counts}")
    print(f"  Observed: {experiment.observed_counts}")
    print(f"  Chi-square: {chi_result['chi_square']} (Pass: {chi_result['passed']})")
    
    return experiment


def create_testcross_experiment():
    """
    Create a testcross: EeWw × eeww
    This helps identify genotypes - useful for your CRISPR work!
    """
    print("\n" + "="*60)
    print("Creating Test Experiment 3: Test Cross")
    print("="*60)
    
    # Define alleles
    allele_definitions = {
        'E': Allele('E', 'Red eyes', is_dominant=True),
        'e': Allele('e', 'White eyes', is_dominant=False),
        'W': Allele('W', 'Normal wings', is_dominant=True),
        'w': Allele('w', 'Vestigial wings', is_dominant=False)
    }
    
    # Create experiment
    experiment = Experiment(
        experiment_id="TEST_003",
        name="Test Cross - Genotype Verification",
        parent1_string="Ee Ww",
        parent2_string="ee ww",
        allele_definitions=allele_definitions,
        total_expected=400,
        notes="Testcross to verify parent genotype. Expected 1:1:1:1 ratio. Similar to CRISPR marker verification."
    )
    
    # Calculate expected ratios
    offspring = GeneticsCalculator.generate_punnett_square(
        experiment.parent1, experiment.parent2
    )
    
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(
        offspring, experiment.allele_definitions
    )
    
    expected_counts = GeneticsCalculator.calculate_expected_counts(
        phenotype_ratios, experiment.total_expected
    )
    
    experiment.set_expected_counts(expected_counts)
    
    # Add realistic observations for 1:1:1:1 ratio
    # Expected: 100 each
    observed_counts = {
        'Red eyes, Normal wings': 98,
        'Red eyes, Vestigial wings': 103,
        'White eyes, Normal wings': 102,
        'White eyes, Vestigial wings': 97
    }
    
    experiment.add_observations(observed_counts)
    
    # Run statistical analysis
    chi_result = StatisticalAnalyzer.chi_square_test(
        experiment.expected_counts,
        experiment.observed_counts
    )
    
    experiment.set_chi_square_result(chi_result)
    
    # Save
    storage = ExperimentStorage()
    storage.save_experiment(experiment)
    
    print(f"✓ Created: {experiment.name}")
    print(f"  ID: {experiment.experiment_id}")
    print(f"  Parents: {experiment.parent1} × {experiment.parent2}")
    print(f"  Expected: {experiment.expected_counts}")
    print(f"  Observed: {experiment.observed_counts}")
    print(f"  Chi-square: {chi_result['chi_square']} (Pass: {chi_result['passed']})")
    
    return experiment


def create_failed_experiment():
    """
    Create an experiment where chi-square FAILS.
    This tests your error detection visualizations.
    """
    print("\n" + "="*60)
    print("Creating Test Experiment 4: Failed Experiment (High Chi-Square)")
    print("="*60)
    
    # Define alleles
    allele_definitions = {
        'E': Allele('E', 'Red eyes', is_dominant=True),
        'e': Allele('e', 'White eyes', is_dominant=False)
    }
    
    # Create experiment
    experiment = Experiment(
        experiment_id="TEST_004",
        name="Problematic Cross - Selection Bias Detected",
        parent1_string="Ee",
        parent2_string="ee",
        allele_definitions=allele_definitions,
        total_expected=500,
        notes="This experiment shows selection bias - white-eyed flies may have been easier to spot and count. Chi-square should fail."
    )
    
    # Calculate expected ratios
    offspring = GeneticsCalculator.generate_punnett_square(
        experiment.parent1, experiment.parent2
    )
    
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(
        offspring, experiment.allele_definitions
    )
    
    expected_counts = GeneticsCalculator.calculate_expected_counts(
        phenotype_ratios, experiment.total_expected
    )
    
    experiment.set_expected_counts(expected_counts)
    
    # Add BAD observations - way off from expected
    # Expected: 250 red, 250 white
    # Observed: Heavily biased toward white (simulating counting bias)
    observed_counts = {
        'Red eyes': 180,    # Much less than 250
        'White eyes': 320   # Much more than 250
    }
    
    experiment.add_observations(observed_counts)
    
    # Run statistical analysis
    chi_result = StatisticalAnalyzer.chi_square_test(
        experiment.expected_counts,
        experiment.observed_counts
    )
    
    experiment.set_chi_square_result(chi_result)
    
    # Save
    storage = ExperimentStorage()
    storage.save_experiment(experiment)
    
    print(f"✓ Created: {experiment.name}")
    print(f"  ID: {experiment.experiment_id}")
    print(f"  Parents: {experiment.parent1} × {experiment.parent2}")
    print(f"  Expected: {experiment.expected_counts}")
    print(f"  Observed: {experiment.observed_counts}")
    print(f"  Chi-square: {chi_result['chi_square']} (Pass: {chi_result['passed']})")
    print(f"  ⚠️ This experiment should show FAILED chi-square test!")
    
    return experiment


def create_generation_series():
    """
    Create a series of experiments simulating F1, F2, F3 generations.
    Perfect for testing multi-generation visualizations!
    """
    print("\n" + "="*60)
    print("Creating Test Experiments 5-7: Multi-Generation Series")
    print("="*60)
    
    experiments = []
    
    # Define alleles
    allele_definitions = {
        'T': Allele('T', 'CRISPR Marker Present', is_dominant=True),
        't': Allele('t', 'No Marker', is_dominant=False)
    }
    
    # F1 Generation: Tt × Tt
    exp1 = Experiment(
        experiment_id="TEST_005",
        name="F1 Generation - CRISPR Marker Breeding",
        parent1_string="Tt",
        parent2_string="Tt",
        allele_definitions=allele_definitions,
        total_expected=400,
        notes="F1 generation. Starting to select for homozygous TT flies."
    )
    
    offspring = GeneticsCalculator.generate_punnett_square(exp1.parent1, exp1.parent2)
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(offspring, allele_definitions)
    expected_counts = GeneticsCalculator.calculate_expected_counts(phenotype_ratios, 400)
    exp1.set_expected_counts(expected_counts)
    
    # F1 observations: 3:1 ratio
    exp1.add_observations({
        'CRISPR Marker Present': 305,  # ~75%
        'No Marker': 95                # ~25%
    })
    
    chi_result = StatisticalAnalyzer.chi_square_test(exp1.expected_counts, exp1.observed_counts)
    exp1.set_chi_square_result(chi_result)
    
    storage = ExperimentStorage()
    storage.save_experiment(exp1)
    experiments.append(exp1)
    
    print(f"✓ Created F1: {exp1.name}")
    print(f"  Marker frequency: 76.2%")
    
    # F2 Generation: Selected TT and Tt flies crossed
    # Simulating increased marker frequency
    exp2 = Experiment(
        experiment_id="TEST_006",
        name="F2 Generation - Selecting for TT",
        parent1_string="Tt",
        parent2_string="Tt",
        allele_definitions=allele_definitions,
        total_expected=400,
        notes="F2 generation. Selected flies with markers from F1. Marker frequency increasing."
    )
    
    offspring = GeneticsCalculator.generate_punnett_square(exp2.parent1, exp2.parent2)
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(offspring, allele_definitions)
    expected_counts = GeneticsCalculator.calculate_expected_counts(phenotype_ratios, 400)
    exp2.set_expected_counts(expected_counts)
    
    # F2 observations: Still 3:1 but simulating selection working
    exp2.add_observations({
        'CRISPR Marker Present': 315,  # ~79% (slightly higher)
        'No Marker': 85                # ~21%
    })
    
    chi_result = StatisticalAnalyzer.chi_square_test(exp2.expected_counts, exp2.observed_counts)
    exp2.set_chi_square_result(chi_result)
    
    storage.save_experiment(exp2)
    experiments.append(exp2)
    
    print(f"✓ Created F2: {exp2.name}")
    print(f"  Marker frequency: 78.8%")
    
    # F3 Generation: Crossed confirmed TT flies
    exp3 = Experiment(
        experiment_id="TEST_007",
        name="F3 Generation - Confirmed TT Line",
        parent1_string="TT",
        parent2_string="TT",
        allele_definitions=allele_definitions,
        total_expected=400,
        notes="F3 generation. Successfully isolated TT flies. All offspring should have marker."
    )
    
    offspring = GeneticsCalculator.generate_punnett_square(exp3.parent1, exp3.parent2)
    phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(offspring, allele_definitions)
    expected_counts = GeneticsCalculator.calculate_expected_counts(phenotype_ratios, 400)
    exp3.set_expected_counts(expected_counts)
    
    # F3 observations: 100% have marker (success!)
    exp3.add_observations({
        'CRISPR Marker Present': 400,  # 100%!
    })
    
    chi_result = StatisticalAnalyzer.chi_square_test(exp3.expected_counts, exp3.observed_counts)
    exp3.set_chi_square_result(chi_result)
    
    storage.save_experiment(exp3)
    experiments.append(exp3)
    
    print(f"✓ Created F3: {exp3.name}")
    print(f"  Marker frequency: 100% - Success! Pure TT line established!")
    
    return experiments


def main():
    """
    Main function to create all test experiments.
    """
    print("\n" + "="*60)
    print("FRUIT FLY GENETICS TRACKER - TEST DATA GENERATOR")
    print("="*60)
    print("\nThis script will create 7 test experiments:")
    print("1. Simple monohybrid cross (Ee × ee)")
    print("2. Dihybrid cross (EeWw × EeWw)")
    print("3. Test cross (EeWw × eeww)")
    print("4. Failed experiment (high chi-square)")
    print("5-7. Multi-generation series (F1, F2, F3)")
    print("\nThese will let you test all visualizations and reports!")
    
    response = input("\nCreate test experiments? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled.")
        return
    
    # Create all test experiments
    exp1 = create_simple_monohybrid_test()
    exp2 = create_dihybrid_test()
    exp3 = create_testcross_experiment()
    exp4 = create_failed_experiment()
    exp_series = create_generation_series()
    
    print("\n" + "="*60)
    print("✓ ALL TEST EXPERIMENTS CREATED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📊 Now you can test:")
    print("\n1. VIEW EXPERIMENTS:")
    print("   - Run main.py → [4] List all experiments")
    print("   - You should see 7 experiments")
    
    print("\n2. TEST BASIC VISUALIZATIONS:")
    print("   - [6] Generate visualizations → [1] Bar chart (use TEST_001)")
    print("   - [6] Generate visualizations → [2] Pie chart (use TEST_002)")
    print("   - [6] Generate visualizations → [3] Punnett Square (use any)")
    
    print("\n3. TEST ADVANCED VISUALIZATIONS:")
    print("   - [6] → [5] Deviation plot (use TEST_001 - good data)")
    print("   - [6] → [6] Chi-square contribution (use TEST_004 - failed test)")
    print("   - [6] → [16] Summary dashboard (use TEST_002 - complex cross)")
    
    print("\n4. TEST MULTI-EXPERIMENT VISUALIZATIONS:")
    print("   - [6] → [14] Multi-generation line graph")
    print("     Select experiments 5, 6, 7 (TEST_005, TEST_006, TEST_007)")
    print("     Track: 'CRISPR Marker Present'")
    print("     You should see marker frequency go from 76% → 79% → 100%")
    
    print("\n5. TEST PDF EXPORT:")
    print("   - [7] Export to PDF → Select any experiment")
    print("   - Check exports/ folder for PDF with all charts")
    
    print("\n6. TEST 'GENERATE ALL':")
    print("   - [6] → [18] Generate ALL charts")
    print("   - Select TEST_002 (dihybrid cross)")
    print("   - This creates 12+ charts at once!")
    
    print("\n📁 All experiments saved in: data/experiments/")
    print("📁 All charts will be saved in: exports/")
    
    print("\n" + "="*60)
    print("🎉 READY TO TEST! Run: python main.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()