# ============================================================================
# FILE: visualization/generation_tracker.py (NEW FILE)
# Track and visualize data across multiple generations
# ============================================================================

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import config
matplotlib.use('Agg')
from storage.file_storage import ExperimentStorage

class GenerationTracker:
    """
    Visualizations for tracking traits across multiple generations.
    """
    
    @staticmethod
    def create_multi_generation_line_graph(experiments, trait_name, output_path=None):
        """
        Create line graph showing how a trait changes across generations.
        Assumes experiments are labeled with generation info (F1, F2, F3, etc.)
        
        Args:
            experiments: List of Experiment objects in chronological order
            trait_name: Name of phenotype to track
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiments:
            raise ValueError("Need experiments to track")
        
        generations = []
        frequencies = []
        
        for i, exp in enumerate(experiments):
            if not exp.is_complete():
                continue
            
            # Generation label (use index if no explicit label)
            gen_label = f"Gen {i+1}"
            generations.append(gen_label)
            
            # Calculate frequency of trait
            if trait_name in exp.observed_counts:
                total = sum(exp.observed_counts.values())
                frequency = (exp.observed_counts[trait_name] / total) * 100
                frequencies.append(frequency)
            else:
                frequencies.append(0)
        
        if not generations:
            raise ValueError("No complete experiments to display")
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        ax.plot(generations, frequencies, marker='o', linewidth=2, 
               markersize=8, color='steelblue')
        
        # Add value labels
        for i, (gen, freq) in enumerate(zip(generations, frequencies)):
            ax.text(i, freq + 2, f'{freq:.1f}%', ha='center', va='bottom')
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Frequency (%)')
        ax.set_title(f'Frequency of "{trait_name}" Across Generations')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 110)
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"multi_gen_{trait_name.replace(' ', '_')}.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_generation_comparison(experiments, output_path=None):
        """
        Compare all phenotypes across generations side by side.
        
        Args:
            experiments: List of Experiment objects
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiments:
            raise ValueError("Need experiments to compare")
        
        # Get all unique phenotypes across experiments
        all_phenotypes = set()
        for exp in experiments:
            if exp.is_complete():
                all_phenotypes.update(exp.observed_counts.keys())
        
        phenotypes = sorted(list(all_phenotypes))
        
        # Build data matrix
        data = []
        gen_labels = []
        
        for i, exp in enumerate(experiments):
            if not exp.is_complete():
                continue
            
            gen_labels.append(f"Gen {i+1}")
            gen_data = []
            total = sum(exp.observed_counts.values())
            
            for phenotype in phenotypes:
                count = exp.observed_counts.get(phenotype, 0)
                percentage = (count / total * 100) if total > 0 else 0
                gen_data.append(percentage)
            
            data.append(gen_data)
        
        if not data:
            raise ValueError("No complete experiments to display")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(gen_labels))
        width = 0.8 / len(phenotypes)
        
        for i, phenotype in enumerate(phenotypes):
            phenotype_data = [gen[i] for gen in data]
            offset = (i - len(phenotypes)/2) * width + width/2
            ax.bar(x + offset, phenotype_data, width, label=phenotype)
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Percentage (%)')
        ax.set_title('Phenotype Distribution Across Generations')
        ax.set_xticks(x)
        ax.set_xticklabels(gen_labels)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / "generation_comparison.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path
    
    @staticmethod
    def create_cumulative_count_graph(experiment, phenotype_order=None, output_path=None):
        """
        Show cumulative counts as if flies were counted sequentially.
        Simulates the counting process to show running totals.
        
        Args:
            experiment: Experiment object with observations
            phenotype_order: Order in which phenotypes were counted (if known)
            output_path: Where to save chart
            
        Returns:
            Path to saved chart
        """
        if not experiment.is_complete():
            raise ValueError("Experiment must have observations")
        
        phenotypes = list(experiment.observed_counts.keys())
        
        # Simulate sequential counting (in reality would need actual count sequence)
        # For now, distribute counts evenly as if counted in batches
        total_flies = sum(experiment.observed_counts.values())
        
        fig, ax = plt.subplots(figsize=config.DEFAULT_CHART_SIZE)
        
        cumulative_x = []
        cumulative_y = {}
        
        for phenotype in phenotypes:
            cumulative_y[phenotype] = []
        
        # Simulate counting in small batches
        batch_size = 10
        current_counts = {p: 0 for p in phenotypes}
        
        for fly_num in range(0, total_flies + batch_size, batch_size):
            cumulative_x.append(fly_num)
            
            # Distribute this batch proportionally
            for phenotype in phenotypes:
                target = experiment.observed_counts[phenotype]
                proportion = target / total_flies
                increment = min(batch_size * proportion, target - current_counts[phenotype])
                current_counts[phenotype] += increment
                cumulative_y[phenotype].append(current_counts[phenotype])
        
        # Plot lines for each phenotype
        for phenotype in phenotypes:
            ax.plot(cumulative_x, cumulative_y[phenotype], 
                   marker='', linewidth=2, label=phenotype)
        
        # Add expected lines (dashed)
        for phenotype in phenotypes:
            expected_ratio = experiment.expected_counts[phenotype] / experiment.total_expected
            expected_line = [x * expected_ratio for x in cumulative_x]
            ax.plot(cumulative_x, expected_line, '--', alpha=0.5, linewidth=1)
        
        ax.set_xlabel('Flies Counted')
        ax.set_ylabel('Cumulative Count')
        ax.set_title(f'{experiment.name} - Cumulative Counting Progress')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_cumulative.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI)
        plt.close()
        
        return output_path