# ============================================================================
# FILE: visualization/charts.py
# Generate visualizations of experiment results
# ============================================================================

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import config
from pathlib import Path

class ChartGenerator:
    """
    Generates charts and graphs for experiment results.
    """
    
    @staticmethod
    def create_bar_chart(experiment, output_path=None):
        """
        Create bar chart comparing expected vs observed counts.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart (auto-generated if None)
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations to create chart")
        
        phenotypes = list(experiment.expected_counts.keys())
        expected = [experiment.expected_counts[p] for p in phenotypes]
        observed = [experiment.observed_counts[p] for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        x = range(len(phenotypes))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], expected, width, label='Expected', color='steelblue')
        ax.bar([i + width/2 for i in x], observed, width, label='Observed', color='coral')
        
        ax.set_xlabel('Phenotype')
        ax.set_ylabel('Count')
        ax.set_title(f'{experiment.name} - Expected vs Observed')
        ax.set_xticks(x)
        ax.set_xticklabels(phenotypes, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_bar_chart.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_pie_chart(experiment, output_path=None):
        """
        Create pie chart showing phenotype distribution.
        
        Args:
            experiment: Experiment object with observations
            output_path: Where to save chart (auto-generated if None)
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations to create chart")
        
        phenotypes = list(experiment.observed_counts.keys())
        counts = [experiment.observed_counts[p] for p in phenotypes]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        ax.pie(counts, labels=phenotypes, autopct='%1.1f%%', startangle=90)
        ax.set_title(f'{experiment.name} - Phenotype Distribution')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_pie_chart.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path