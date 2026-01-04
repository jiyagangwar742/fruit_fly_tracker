# ============================================================================
# FILE: cli/menu.py
# CLI menu system and user interaction
# ============================================================================

from visualization.punnett_square import PunnettSquareVisualizer
from reports.reports import PDFReportGenerator
from cli.display import Display
from models.experiment import Experiment
from models.allele import Allele
from core.genetics import GeneticsCalculator
from core.statistics import StatisticalAnalyzer
from storage.file_storage import ExperimentStorage
from visualization.charts import ChartGenerator
from visualization.advanced_charts import AdvancedChartGenerator
from visualization.generation_tracker import GenerationTracker


import config


class MenuSystem:
    """Handles CLI menu navigation and user input."""
    
    def __init__(self):
        self.storage = ExperimentStorage()
        self.running = True
    
    def start(self):
        """Start the main menu loop."""
        Display.header(f"{config.APP_NAME} v{config.APP_VERSION}")
        print(f"Loading experiments... Found {len(self.storage.list_all_experiments())} experiments.\n")
        
        while self.running:
            self.show_main_menu()
    
    def show_main_menu(self):
        """Display and handle main menu."""
        print("\nMAIN MENU:")
        print("[1] Create new experiment")
        print("[2] Add observation data")
        print("[3] View experiment results")
        print("[4] List all experiments")
        print("[5] Search experiments")
        print("[6] Generate visualizations")
        print("[7] Export to PDF")              # NEW OPTION
        print("[8] Delete experiment")          # CHANGED from [7]
        print("[0] Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            self.create_experiment()
        elif choice == "2":
            self.add_observations()
        elif choice == "3":
            self.view_results()
        elif choice == "4":
            self.list_experiments()
        elif choice == "5":
            self.search_experiments()
        elif choice == "6":
            self.generate_charts()
        elif choice == "7":                     # NEW
            self.export_to_pdf()                # NEW
        elif choice == "8":                     # CHANGED from "7"
            self.delete_experiment()
        elif choice == "0":
            self.running = False
            print("\nGoodbye!")
        else:
            Display.error("Invalid choice. Please try again.")

    
    def create_experiment(self):
        """Create a new experiment."""
        Display.header("CREATE NEW EXPERIMENT")
        
        # Get experiment details
        name = input("Experiment name: ").strip()
        if not name:
            Display.error("Name cannot be empty.")
            return
        
        # Generate unique ID
        existing_ids = self.storage.list_all_experiments()
        exp_num = len(existing_ids) + 1
        experiment_id = f"EXP_{exp_num:03d}"
        
        # Get parent genotypes
        print("\nEnter parent genotypes (e.g., 'Ee' or 'Ee Ww' for multiple traits):")
        parent1_str = input("Parent 1 genotype: ").strip()
        parent2_str = input("Parent 2 genotype: ").strip()
        
        if not parent1_str or not parent2_str:
            Display.error("Parent genotypes cannot be empty.")
            return
        
        # Define alleles
        print("\nDefine alleles:")
        allele_definitions = self._define_alleles(parent1_str)
        
        # Get expected count
        try:
            total_expected = int(input("\nHow many offspring do you expect to count? "))
        except ValueError:
            Display.error("Please enter a valid number.")
            return
        
        # Optional notes
        notes = input("Notes (optional, press Enter to skip): ").strip()
        
        # Create experiment
        try:
            experiment = Experiment(
                experiment_id=experiment_id,
                name=name,
                parent1_string=parent1_str,
                parent2_string=parent2_str,
                allele_definitions=allele_definitions,
                total_expected=total_expected,
                notes=notes
            )
            
            # Calculate expected ratios
            self._calculate_expected_ratios(experiment)
            
            # Save
            self.storage.save_experiment(experiment)
            
            Display.success(f"Experiment '{name}' created with ID: {experiment_id}")
            self._show_expected_ratios(experiment)
            
        except Exception as e:
            Display.error(f"Failed to create experiment: {str(e)}")
    
    def _define_alleles(self, genotype_string):
        """Helper to define alleles interactively."""
        gene_pairs = genotype_string.split()
        allele_definitions = {}
        
        for i, pair in enumerate(gene_pairs):
            print(f"\nGene {i+1} (from '{pair}'):")
            
            # Get unique alleles
            alleles = set(pair)
            
            for allele_symbol in sorted(alleles, key=lambda x: (x.lower(), x.islower())):
                description = input(f"  {allele_symbol} = ").strip()
                is_dominant = allele_symbol.isupper()
                
                allele_definitions[allele_symbol] = Allele(
                    symbol=allele_symbol,
                    description=description,
                    is_dominant=is_dominant
                )
        
        return allele_definitions
    
    def _calculate_expected_ratios(self, experiment):
        """Calculate and set expected ratios for an experiment."""
        # Generate offspring
        offspring = GeneticsCalculator.generate_punnett_square(
            experiment.parent1, experiment.parent2
        )
        
        # Calculate phenotype ratios
        phenotype_ratios = GeneticsCalculator.calculate_phenotype_ratios(
            offspring, experiment.allele_definitions
        )
        
        # Calculate expected counts
        expected_counts = GeneticsCalculator.calculate_expected_counts(
            phenotype_ratios, experiment.total_expected
        )
        
        experiment.set_expected_counts(expected_counts)
    
    def _show_expected_ratios(self, experiment):
        """Display expected ratios."""
        Display.section("EXPECTED RATIOS")
        
        headers = ["Phenotype", "Expected Count", "Percentage"]
        rows = []
        
        for phenotype, count in experiment.expected_counts.items():
            percentage = (count / experiment.total_expected) * 100
            rows.append([phenotype, f"{count:.1f}", f"{percentage:.1f}%"])
        
        Display.table(headers, rows)
    
    def add_observations(self):
        """Add observations to an existing experiment."""
        Display.header("ADD OBSERVATIONS")
        
        # Select experiment
        experiment = self._select_experiment()
        if not experiment:
            return
        
        if experiment.is_complete():
            print(f"\nThis experiment already has observations.")
            overwrite = input("Overwrite existing data? (y/n): ").strip().lower()
            if overwrite != 'y':
                return
        
        # Show expected counts
        print(f"\nExperiment: {experiment.name}")
        self._show_expected_ratios(experiment)
        
        # Get observed counts
        print("\nEnter observed counts:")
        observed_counts = {}
        
        for phenotype in experiment.expected_counts.keys():
            while True:
                try:
                    count = int(input(f"  {phenotype}: "))
                    observed_counts[phenotype] = count
                    break
                except ValueError:
                    Display.error("Please enter a valid number.")
        
        # Verify total
        total_observed = sum(observed_counts.values())
        print(f"\nTotal observed: {total_observed}")
        
        confirm = input("Save these observations? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        # Save observations
        experiment.add_observations(observed_counts)
        
        # Run statistical analysis
        self._run_statistical_analysis(experiment)
        
        # Save experiment
        self.storage.save_experiment(experiment)
        
        Display.success("Observations saved and analyzed!")
        
        # Show results
        self._display_statistical_results(experiment)
    
    def _select_experiment(self):
        """Helper to select an experiment from list."""
        experiments = self.storage.load_all_experiments()
        
        if not experiments:
            Display.error("No experiments found. Create one first!")
            return None
        
        # Sort by date (newest first)
        experiments.sort(key=lambda x: x.date_created, reverse=True)
        
        print("\nAvailable experiments:")
        for i, exp in enumerate(experiments, 1):
            status = "✓" if exp.is_complete() else "⏳"
            print(f"[{i}] {status} {exp.name} ({exp.experiment_id}) - {exp.date_created.strftime('%Y-%m-%d')}")
        
        while True:
            try:
                choice = int(input("\nSelect experiment number: "))
                if 1 <= choice <= len(experiments):
                    return experiments[choice - 1]
                else:
                    Display.error("Invalid selection.")
            except ValueError:
                Display.error("Please enter a number.")
 
    def _select_multiple_experiments(self):
        """Helper to select multiple experiments from list."""
        experiments = self.storage.load_all_experiments()
        
        if not experiments:
            Display.error("No experiments found.")
            return None
        
        # Sort by date
        experiments.sort(key=lambda x: x.date_created)
        
        print("\nAvailable experiments:")
        for i, exp in enumerate(experiments, 1):
            status = "✓" if exp.is_complete() else "⏳"
            print(f"[{i}] {status} {exp.name} ({exp.experiment_id}) - {exp.date_created.strftime('%Y-%m-%d')}")
        
        print("\nEnter experiment numbers separated by commas (e.g., 1,2,3)")
        selection = input("or 'all' for all experiments: ").strip().lower()
        
        if selection == 'all':
            return experiments
        
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            selected = []
            for idx in indices:
                if 1 <= idx <= len(experiments):
                    selected.append(experiments[idx - 1])
                else:
                    Display.error(f"Invalid experiment number: {idx}")
            
            return selected if selected else None
        
        except ValueError:
            Display.error("Invalid input format.")
            return None

    def _run_statistical_analysis(self, experiment):
        """Run chi-square test on experiment."""
        result = StatisticalAnalyzer.chi_square_test(
            experiment.expected_counts,
            experiment.observed_counts
        )
        experiment.set_chi_square_result(result)
    
    def _display_statistical_results(self, experiment):
        """Display statistical test results."""
        if not experiment.chi_square_result:
            return
        
        Display.section("STATISTICAL ANALYSIS")
        
        result = experiment.chi_square_result
        print(f"Chi-square value: {result['chi_square']}")
        print(f"P-value: {result['p_value']}")
        print(f"Degrees of freedom: {result['degrees_freedom']}")
        print(f"Critical value (α={result['alpha']}): {result['critical_value']}")
        
        if result['passed']:
            Display.success("PASS - Data matches expected ratios")
        else:
            Display.error("FAIL - Significant deviation from expected")
        
        print(f"\n{result['interpretation']}")
    
    def view_results(self):
        """View detailed results for an experiment."""
        Display.header("VIEW EXPERIMENT RESULTS")
        
        experiment = self._select_experiment()
        if not experiment:
            return
        
        # Show basic info
        Display.section("EXPERIMENT DETAILS")
        print(f"ID: {experiment.experiment_id}")
        print(f"Name: {experiment.name}")
        print(f"Created: {experiment.date_created.strftime('%Y-%m-%d %H:%M')}")
        print(f"Status: {experiment.get_status()}")
        print(f"Parents: {experiment.parent1} × {experiment.parent2}")
        
        # Show expected ratios
        self._show_expected_ratios(experiment)
        
        # Show observations if available
        if experiment.is_complete():
            Display.section("OBSERVED COUNTS")
            headers = ["Phenotype", "Expected", "Observed", "Difference"]
            rows = []
            
            for phenotype in experiment.expected_counts.keys():
                expected = experiment.expected_counts[phenotype]
                observed = experiment.observed_counts[phenotype]
                diff = observed - expected
                rows.append([phenotype, f"{expected:.1f}", observed, f"{diff:+.1f}"])
            
            Display.table(headers, rows)
            
            # Show statistical results
            self._display_statistical_results(experiment)
        else:
            print("\nNo observations recorded yet.")
        
        # Show notes
        if experiment.notes:
            Display.section("NOTES")
            print(experiment.notes)
    
    def list_experiments(self):
        """List all experiments."""
        Display.header("ALL EXPERIMENTS")
        
        experiments = self.storage.load_all_experiments()
        
        if not experiments:
            print("No experiments found.")
            return
        
        # Sort by date (newest first)
        experiments.sort(key=lambda x: x.date_created, reverse=True)
        
        headers = ["ID", "Name", "Date", "Status", "Chi²"]
        rows = []
        
        for exp in experiments:
            chi_square = "---"
            if exp.chi_square_result:
                chi_val = exp.chi_square_result['chi_square']
                passed = "✓" if exp.chi_square_result['passed'] else "✗"
                chi_square = f"{chi_val} {passed}"
            
            rows.append([
                exp.experiment_id,
                exp.name,
                exp.date_created.strftime('%Y-%m-%d'),
                exp.get_status(),
                chi_square
            ])
        
        Display.table(headers, rows)
    
    def search_experiments(self):
        """Search experiments by name."""
        Display.header("SEARCH EXPERIMENTS")
        
        query = input("Enter search term: ").strip()
        if not query:
            return
        
        matches = self.storage.search_experiments(query, field="name")
        
        if not matches:
            print(f"No experiments found matching '{query}'")
            return
        
        print(f"\nFound {len(matches)} matching experiment(s):")
        for exp in matches:
            status = "✓" if exp.is_complete() else "⏳"
            print(f"  {status} {exp.name} ({exp.experiment_id})")
    
    def generate_charts(self):
        """Generate visualizations for an experiment."""
        Display.header("GENERATE VISUALIZATIONS")
        
        print("\nSelect visualization type:")
        print("\n--- Basic Charts ---")
        print("[1] Bar chart (Expected vs Observed)")
        print("[2] Pie chart (Phenotype distribution)")
        print("[3] Punnett Square diagram")
        print("[4] All basic charts")
        
        print("\n--- Analysis Charts ---")
        print("[5] Deviation plot (Shows how far off expected)")
        print("[6] Chi-square contribution (Which phenotypes affect chi²)")
        print("[7] Scatter plot (Expected vs Observed)")
        print("[8] Confidence intervals (With error bars)")
        
        print("\n--- Distribution Charts ---")
        print("[9] Stacked bar chart")
        print("[10] Percentage bar chart (Horizontal)")
        print("[11] Allele frequency pie chart")
        print("[12] Heatmap")
        
        print("\n--- Multi-Experiment Charts ---")
        print("[13] Comparison table (Multiple experiments)")
        print("[14] Multi-generation line graph")
        print("[15] Generation comparison")
        
        print("\n--- Special ---")
        print("[16] Summary dashboard (4-panel overview)")
        print("[17] Cumulative count graph")
        print("[18] Generate ALL charts for this experiment")
        
        choice = input("\nEnter choice: ").strip()
        
        # For single experiment charts
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "17", "18"]:
            experiment = self._select_experiment()
            if not experiment:
                return
        
        try:
            # Basic charts
            if choice == "1":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = ChartGenerator.create_bar_chart(experiment)
                Display.success(f"Bar chart saved: {path}")
            
            elif choice == "2":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = ChartGenerator.create_pie_chart(experiment)
                Display.success(f"Pie chart saved: {path}")
            
            elif choice == "3":
                path = PunnettSquareVisualizer.create_punnett_square(experiment)
                Display.success(f"Punnett Square saved: {path}")
            
            elif choice == "4":
                path = PunnettSquareVisualizer.create_punnett_square(experiment)
                Display.success(f"Punnett Square saved: {path}")
                
                if experiment.is_complete():
                    path = ChartGenerator.create_bar_chart(experiment)
                    Display.success(f"Bar chart saved: {path}")
                    path = ChartGenerator.create_pie_chart(experiment)
                    Display.success(f"Pie chart saved: {path}")
                else:
                    Display.info("Skipping bar/pie (no observations yet)")
            
            # Analysis charts
            elif choice == "5":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_deviation_plot(experiment)
                Display.success(f"Deviation plot saved: {path}")
            
            elif choice == "6":
                if not experiment.is_complete() or not experiment.chi_square_result:
                    Display.error("Need observations and chi-square results.")
                    return
                path = AdvancedChartGenerator.create_chi_square_contribution_chart(experiment)
                Display.success(f"Chi-square contribution saved: {path}")
            
            elif choice == "7":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_expected_vs_observed_scatter(experiment)
                Display.success(f"Scatter plot saved: {path}")
            
            elif choice == "8":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_confidence_interval_chart(experiment)
                Display.success(f"Confidence interval chart saved: {path}")
            
            # Distribution charts
            elif choice == "9":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_stacked_bar_chart(experiment)
                Display.success(f"Stacked bar chart saved: {path}")
            
            elif choice == "10":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_percentage_bar_chart(experiment)
                Display.success(f"Percentage bar chart saved: {path}")
            
            elif choice == "11":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_allele_frequency_chart(experiment)
                Display.success(f"Allele frequency chart saved: {path}")
            
            elif choice == "12":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = AdvancedChartGenerator.create_heatmap(experiment)
                Display.success(f"Heatmap saved: {path}")
            
            # Multi-experiment charts
            elif choice == "13":
                print("\nSelect experiments to compare:")
                experiments = self._select_multiple_experiments()
                if not experiments:
                    return
                path = AdvancedChartGenerator.create_comparison_table_image(experiments)
                Display.success(f"Comparison table saved: {path}")
            
            elif choice == "14":
                print("\nSelect experiments in chronological order:")
                experiments = self._select_multiple_experiments()
                if not experiments:
                    return
                
                # Get trait to track
                trait = input("Enter phenotype name to track (e.g., 'Red eyes'): ").strip()
                if not trait:
                    Display.error("Trait name required.")
                    return
                
                path = GenerationTracker.create_multi_generation_line_graph(experiments, trait)
                Display.success(f"Multi-generation graph saved: {path}")
            
            elif choice == "15":
                print("\nSelect experiments to compare:")
                experiments = self._select_multiple_experiments()
                if not experiments:
                    return
                path = GenerationTracker.create_generation_comparison(experiments)
                Display.success(f"Generation comparison saved: {path}")
            
            # Special charts
            elif choice == "16":
                if not experiment.is_complete():
                    Display.error("Need observations for dashboard.")
                    return
                path = AdvancedChartGenerator.create_summary_dashboard(experiment)
                Display.success(f"Summary dashboard saved: {path}")
            
            elif choice == "17":
                if not experiment.is_complete():
                    Display.error("Need observations for this chart.")
                    return
                path = GenerationTracker.create_cumulative_count_graph(experiment)
                Display.success(f"Cumulative count graph saved: {path}")
            
            elif choice == "18":
                # Generate ALL charts for this experiment
                Display.info("Generating all applicable charts...")
                
                # Always available
                path = PunnettSquareVisualizer.create_punnett_square(experiment)
                Display.success(f"✓ Punnett Square: {path}")
                
                if experiment.is_complete():
                    # Basic charts
                    path = ChartGenerator.create_bar_chart(experiment)
                    Display.success(f"✓ Bar chart: {path}")
                    
                    path = ChartGenerator.create_pie_chart(experiment)
                    Display.success(f"✓ Pie chart: {path}")
                    
                    # Analysis charts
                    path = AdvancedChartGenerator.create_deviation_plot(experiment)
                    Display.success(f"✓ Deviation plot: {path}")
                    
                    path = AdvancedChartGenerator.create_expected_vs_observed_scatter(experiment)
                    Display.success(f"✓ Scatter plot: {path}")
                    
                    path = AdvancedChartGenerator.create_confidence_interval_chart(experiment)
                    Display.success(f"✓ Confidence intervals: {path}")
                    
                    # Distribution charts
                    path = AdvancedChartGenerator.create_stacked_bar_chart(experiment)
                    Display.success(f"✓ Stacked bar: {path}")
                    
                    path = AdvancedChartGenerator.create_percentage_bar_chart(experiment)
                    Display.success(f"✓ Percentage bar: {path}")
                    
                    path = AdvancedChartGenerator.create_allele_frequency_chart(experiment)
                    Display.success(f"✓ Allele frequency: {path}")
                    
                    path = AdvancedChartGenerator.create_heatmap(experiment)
                    Display.success(f"✓ Heatmap: {path}")
                    
                    path = AdvancedChartGenerator.create_summary_dashboard(experiment)
                    Display.success(f"✓ Dashboard: {path}")
                    
                    path = GenerationTracker.create_cumulative_count_graph(experiment)
                    Display.success(f"✓ Cumulative count: {path}")
                    
                    if experiment.chi_square_result:
                        path = AdvancedChartGenerator.create_chi_square_contribution_chart(experiment)
                        Display.success(f"✓ Chi-square contribution: {path}")
                    
                    Display.success(f"\nAll charts generated for {experiment.name}!")
                else:
                    Display.info("Only Punnett Square available (no observations yet)")
            
            else:
                Display.error("Invalid choice.")
        
        except Exception as e:
            Display.error(f"Failed to generate chart: {str(e)}")
            import traceback
            traceback.print_exc()

    def export_to_pdf(self):
        """Export experiment to PDF report."""
        Display.header("EXPORT TO PDF")
        
        experiment = self._select_experiment()
        if not experiment:
            return
    
    try:
        output_path = PDFReportGenerator.generate_report(experiment)
        Display.success(f"PDF report saved: {output_path}")
        
        # Ask if user wants to open it
        open_file = input("\nOpen PDF now? (y/n): ").strip().lower()
        if open_file == 'y':
            import os
            import platform
            
            # Open file with default application
            if platform.system() == 'Darwin':  # macOS
                os.system(f'open "{output_path}"')
            elif platform.system() == 'Windows':
                os.startfile(output_path)
            else:  # Linux
                os.system(f'xdg-open "{output_path}"')
            
            Display.success("PDF opened.")
    
    except Exception as e:
        Display.error(f"Failed to generate PDF: {str(e)}")
        print(f"Details: {e}")

    
    def delete_experiment(self):
        """Delete an experiment."""
        Display.header("DELETE EXPERIMENT")
        
        experiment = self._select_experiment()
        if not experiment:
            return
        
        print(f"\nYou are about to delete: {experiment.name} ({experiment.experiment_id})")
        confirm = input("Are you sure? This cannot be undone. (yes/no): ").strip().lower()
        
        if confirm == "yes":
            if self.storage.delete_experiment(experiment.experiment_id):
                Display.success("Experiment deleted.")
            else:
                Display.error("Failed to delete experiment.")
        else:
            print("Deletion cancelled.")
            
