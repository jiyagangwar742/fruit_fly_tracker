# ============================================================================
# FILE: visualization/advanced_charts.py (NEW FILE - Add to visualization folder)
# Advanced visualization options for genetics experiments
# ============================================================================
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import config
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D

class AdvancedChartGenerator:
    """
    Generates advanced visualizations for genetics experiment analysis.
    """
    
    @staticmethod
    def create_stacked_bar_chart(experiment, output_path=None):
        """
        Create stacked bar chart showing genotype breakdown within phenotypes.
        NOTE: This requires genotype tracking which current implementation doesn't have.
        This is a placeholder that shows phenotype distribution stacked.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.observed_counts.keys())
        counts = [experiment.observed_counts[p] for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        # For now, show as single stack (future: break down by genotype)
        ax.bar(phenotypes, counts, color='steelblue', label='Observed')
        
        ax.set_xlabel('Phenotype')
        ax.set_ylabel('Count')
        ax.set_title(f'{experiment.name} - Phenotype Distribution')
        plt.xticks(rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_stacked_bar.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_deviation_plot(experiment, output_path=None):
        """
        Create deviation plot showing how far each phenotype deviates from expected.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.expected_counts.keys())
        deviations = []
        
        for phenotype in phenotypes:
            expected = experiment.expected_counts[phenotype]
            observed = experiment.observed_counts[phenotype]
            deviation = observed - expected
            deviations.append(deviation)
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        colors = ['red' if d < 0 else 'green' for d in deviations]
        bars = ax.bar(phenotypes, deviations, color=colors, alpha=0.7)
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        ax.set_xlabel('Phenotype')
        ax.set_ylabel('Deviation from Expected')
        ax.set_title(f'{experiment.name} - Observed vs Expected Deviation')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, dev in zip(bars, deviations):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{dev:+.1f}',
                   ha='center', va='bottom' if height >= 0 else 'top')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_deviation.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_chi_square_contribution_chart(experiment, output_path=None):
        """
        Show which phenotypes contribute most to chi-square value.
        
        Args:
            experiment: Experiment object with chi-square results
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete() or not experiment.chi_square_result:
            raise ValueError("Experiment must have observations and chi-square results")
        
        phenotypes = list(experiment.expected_counts.keys())
        contributions = []
        
        # Calculate each phenotype's contribution to chi-square
        for phenotype in phenotypes:
            expected = experiment.expected_counts[phenotype]
            observed = experiment.observed_counts[phenotype]
            contribution = ((observed - expected) ** 2) / expected
            contributions.append(contribution)
        
        # Calculate percentages
        total_chi = sum(contributions)
        percentages = [(c / total_chi * 100) if total_chi > 0 else 0 for c in contributions]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        bars = ax.bar(phenotypes, contributions, color='coral', alpha=0.7)
        ax.set_xlabel('Phenotype')
        ax.set_ylabel('Chi-Square Contribution')
        ax.set_title(f'{experiment.name} - Chi-Square Contribution by Phenotype')
        plt.xticks(rotation=45, ha='right')
        
        # Add percentage labels
        for bar, pct in zip(bars, percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{pct:.1f}%',
                   ha='center', va='bottom')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_chi_contribution.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_expected_vs_observed_scatter(experiment, output_path=None):
        """
        Scatter plot with expected on X-axis and observed on Y-axis.
        Perfect match would be on the diagonal line.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.expected_counts.keys())
        expected = [experiment.expected_counts[p] for p in phenotypes]
        observed = [experiment.observed_counts[p] for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Plot points
        ax.scatter(expected, observed, s=100, alpha=0.6, color='steelblue')
        
        # Add diagonal reference line (perfect match)
        max_val = max(max(expected), max(observed))
        ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfect Match')
        
        # Label points
        for i, phenotype in enumerate(phenotypes):
            ax.annotate(phenotype, (expected[i], observed[i]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax.set_xlabel('Expected Count')
        ax.set_ylabel('Observed Count')
        ax.set_title(f'{experiment.name} - Expected vs Observed')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_scatter.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_allele_frequency_chart(experiment, output_path=None):
        """
        Pie chart showing proportion of each allele in the population.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        # Count alleles across all observed offspring
        from core.genetics import GeneticsCalculator
        
        # Generate all offspring genotypes based on observations
        offspring = GeneticsCalculator.generate_punnett_square(
            experiment.parent1, experiment.parent2
        )
        
        # Count alleles
        allele_counts = {}
        for genotype_str in offspring:
            for pair in genotype_str.split():
                for allele in pair:
                    allele_counts[allele] = allele_counts.get(allele, 0) + 1
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        alleles = list(allele_counts.keys())
        counts = list(allele_counts.values())
        
        ax.pie(counts, labels=alleles, autopct='%1.1f%%', startangle=90)
        ax.set_title(f'{experiment.name} - Allele Frequency Distribution')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_allele_freq.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_confidence_interval_chart(experiment, output_path=None):
        """
        Bar chart with error bars showing confidence intervals.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.expected_counts.keys())
        expected = [experiment.expected_counts[p] for p in phenotypes]
        observed = [experiment.observed_counts[p] for p in phenotypes]
        
        # Calculate 95% confidence intervals (approximate using sqrt(np))
        ci_ranges = [1.96 * np.sqrt(exp) for exp in expected]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        x = np.arange(len(phenotypes))
        width = 0.35
        
        # Expected with error bars
        ax.bar(x - width/2, expected, width, label='Expected', 
               yerr=ci_ranges, capsize=5, color='steelblue', alpha=0.7)
        
        # Observed
        ax.bar(x + width/2, observed, width, label='Observed', 
               color='coral', alpha=0.7)
        
        ax.set_xlabel('Phenotype')
        ax.set_ylabel('Count')
        ax.set_title(f'{experiment.name} - With 95% Confidence Intervals')
        ax.set_xticks(x)
        ax.set_xticklabels(phenotypes, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_confidence.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_heatmap(experiment, output_path=None):
        """
        Heatmap for multi-trait experiments showing frequency of combinations.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.observed_counts.keys())
        
        # For simple experiments, create a single-row heatmap
        # For complex multi-trait, this would be a 2D grid
        counts = [experiment.observed_counts[p] for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        # Create 2D array for heatmap (single row for now)
        data = np.array([counts])
        
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        
        # Set ticks
        ax.set_xticks(np.arange(len(phenotypes)))
        ax.set_xticklabels(phenotypes, rotation=45, ha='right')
        ax.set_yticks([0])
        ax.set_yticklabels(['Count'])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Count', rotation=270, labelpad=15)
        
        # Add text annotations
        for i, count in enumerate(counts):
            ax.text(i, 0, str(count), ha='center', va='center', color='black')
        
        ax.set_title(f'{experiment.name} - Phenotype Frequency Heatmap')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_heatmap.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_percentage_bar_chart(experiment, output_path=None):
        """
        Horizontal bar chart showing percentages instead of counts.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.observed_counts.keys())
        total = sum(experiment.observed_counts.values())
        
        expected_pct = [(experiment.expected_counts[p] / experiment.total_expected * 100) 
                       for p in phenotypes]
        observed_pct = [(experiment.observed_counts[p] / total * 100) 
                       for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        y = np.arange(len(phenotypes))
        height = 0.35
        
        ax.barh(y - height/2, expected_pct, height, label='Expected %', color='steelblue')
        ax.barh(y + height/2, observed_pct, height, label='Observed %', color='coral')
        
        ax.set_yticks(y)
        ax.set_yticklabels(phenotypes)
        ax.set_xlabel('Percentage (%)')
        ax.set_title(f'{experiment.name} - Percentage Distribution')
        ax.legend()
        ax.grid(True, axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_percentage.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_summary_dashboard(experiment, output_path=None):
        """
        Create a multi-panel dashboard with key visualizations.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        fig = plt.figure(figsize=(14, 10))
        
        phenotypes = list(experiment.expected_counts.keys())
        expected = [experiment.expected_counts[p] for p in phenotypes]
        observed = [experiment.observed_counts[p] for p in phenotypes]
        deviations = [observed[i] - expected[i] for i in range(len(phenotypes))]
        
        # Panel 1: Bar chart
        ax1 = plt.subplot(2, 2, 1)
        x = np.arange(len(phenotypes))
        width = 0.35
        ax1.bar(x - width/2, expected, width, label='Expected', color='steelblue')
        ax1.bar(x + width/2, observed, width, label='Observed', color='coral')
        ax1.set_xlabel('Phenotype')
        ax1.set_ylabel('Count')
        ax1.set_title('Expected vs Observed')
        ax1.set_xticks(x)
        ax1.set_xticklabels(phenotypes, rotation=45, ha='right')
        ax1.legend()
        
        # Panel 2: Pie chart
        ax2 = plt.subplot(2, 2, 2)
        ax2.pie(observed, labels=phenotypes, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Observed Distribution')
        
        # Panel 3: Deviation plot
        ax3 = plt.subplot(2, 2, 3)
        colors = ['red' if d < 0 else 'green' for d in deviations]
        ax3.bar(phenotypes, deviations, color=colors, alpha=0.7)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax3.set_xlabel('Phenotype')
        ax3.set_ylabel('Deviation')
        ax3.set_title('Deviation from Expected')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Panel 4: Statistical summary
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        if experiment.chi_square_result:
            result = experiment.chi_square_result
            summary_text = f"""
Statistical Summary:

Chi-Square: {result['chi_square']}
P-Value: {result['p_value']}
DF: {result['degrees_freedom']}
Critical Value: {result['critical_value']}

Result: {'PASS ✓' if result['passed'] else 'FAIL ✗'}

Total Counted: {sum(observed)}
            """
        else:
            summary_text = "No statistical analysis available"
        
        ax4.text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        ax4.set_title('Statistical Analysis')
        
        plt.suptitle(f'{experiment.name} - Summary Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_dashboard.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_comparison_table_image(experiments, output_path=None):
        """
        Create a visual table comparing multiple experiments.
        
        Args:
            experiments: List of Experiment objects to compare
            output_path: Where to save image
            
        Returns:
            Path to saved image
        """
        if not experiments:
            raise ValueError("Need at least one experiment to compare")
        
        fig, ax = plt.subplots(figsize=(12, max(6, len(experiments) * 0.8)))
        ax.axis('tight')
        ax.axis('off')
        
        # Build table data
        headers = ['Experiment', 'Date', 'Parents', 'Total', 'Chi²', 'Status']
        rows = []
        
        for exp in experiments:
            chi_val = '---'
            if exp.chi_square_result:
                chi_val = f"{exp.chi_square_result['chi_square']}"
            
            total = sum(exp.observed_counts.values()) if exp.is_complete() else '---'
            status = '✓' if exp.is_complete() else '⏳'
            
            rows.append([
                exp.name[:20],  # Truncate long names
                exp.date_created.strftime('%Y-%m-%d'),
                f"{exp.parent1} × {exp.parent2}",
                str(total),
                chi_val,
                status
            ])
        
        table = ax.table(cellText=rows, colLabels=headers, 
                        cellLoc='left', loc='center',
                        colWidths=[0.25, 0.12, 0.2, 0.1, 0.1, 0.08])
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style header row
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#3498DB')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(rows) + 1):
            for j in range(len(headers)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ECF0F1')
        
        plt.title('Experiment Comparison', fontsize=14, fontweight='bold', pad=20)
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / "experiments_comparison.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI, bbox_inches='tight')
        plt.close()
        
        return output_path