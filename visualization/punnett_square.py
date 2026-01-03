# ============================================================================
# FILE: visualization/punnett_square.py (NEW FILE - Add to visualization folder)
# Generates visual Punnett square diagrams
# ============================================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import config

class PunnettSquareVisualizer:
    """
    Creates visual Punnett square diagrams for genetic crosses.
    """
    
    @staticmethod
    def create_punnett_square(experiment, output_path=None):
        """
        Create a visual Punnett square diagram.
        
        Args:
            experiment: Experiment object
            output_path: Where to save diagram (auto-generated if None)
            
        Returns:
            Path to saved diagram
        """
        # Get gametes from parents
        parent1_gametes = experiment.parent1.get_gametes()
        parent2_gametes = experiment.parent2.get_gametes()
        
        # Determine grid size
        rows = len(parent2_gametes)
        cols = len(parent1_gametes)
        
        # Create figure
        fig_width = max(8, cols * 2)
        fig_height = max(8, rows * 2)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Cell dimensions
        cell_width = 1.0
        cell_height = 1.0
        
        # Starting positions (leave room for headers)
        start_x = 1.5
        start_y = 1.5
        
        # Draw grid cells with offspring genotypes
        for i, p2_gamete in enumerate(parent2_gametes):
            for j, p1_gamete in enumerate(parent1_gametes):
                # Calculate position (flip y-axis so it reads top to bottom)
                x = start_x + j * cell_width
                y = start_y + (rows - 1 - i) * cell_height
                
                # Draw cell rectangle
                rect = Rectangle((x, y), cell_width, cell_height,
                                linewidth=2, edgecolor='black', 
                                facecolor='lightblue', alpha=0.3)
                ax.add_patch(rect)
                
                # Combine gametes to get offspring genotype
                offspring = PunnettSquareVisualizer._combine_gametes(p1_gamete, p2_gamete)
                
                # Add text in center of cell
                ax.text(x + cell_width/2, y + cell_height/2, offspring,
                       ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Draw parent 1 gametes (top header)
        for j, gamete in enumerate(parent1_gametes):
            x = start_x + j * cell_width
            y = start_y + rows * cell_height
            
            # Header cell
            rect = Rectangle((x, y), cell_width, cell_height,
                           linewidth=2, edgecolor='black', 
                           facecolor='lightcoral', alpha=0.5)
            ax.add_patch(rect)
            
            ax.text(x + cell_width/2, y + cell_height/2, gamete,
                   ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Draw parent 2 gametes (left header)
        for i, gamete in enumerate(parent2_gametes):
            x = start_x - cell_width
            y = start_y + (rows - 1 - i) * cell_height
            
            # Header cell
            rect = Rectangle((x, y), cell_width, cell_height,
                           linewidth=2, edgecolor='black', 
                           facecolor='lightgreen', alpha=0.5)
            ax.add_patch(rect)
            
            ax.text(x + cell_width/2, y + cell_height/2, gamete,
                   ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Add parent labels
        # Parent 1 label (top)
        ax.text(start_x + (cols * cell_width)/2, 
               start_y + (rows + 1) * cell_height + 0.3,
               f'Parent 1: {experiment.parent1}',
               ha='center', va='bottom', fontsize=12, style='italic')
        
        # Parent 2 label (left)
        ax.text(start_x - cell_width - 0.3,
               start_y + (rows * cell_height)/2,
               f'Parent 2: {experiment.parent2}',
               ha='right', va='center', fontsize=12, 
               style='italic', rotation=90)
        
        # Add title
        ax.text(start_x + (cols * cell_width)/2,
               start_y + (rows + 1.5) * cell_height + 0.5,
               f'Punnett Square: {experiment.name}',
               ha='center', va='bottom', fontsize=16, fontweight='bold')
        
        # Set axis limits with padding
        ax.set_xlim(0, start_x + cols * cell_width + 0.5)
        ax.set_ylim(0, start_y + (rows + 2) * cell_height + 0.5)
        
        # Remove axes
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = config.EXPORTS_DIR / f"{experiment.experiment_id}_punnett_square.png"
        
        plt.savefig(output_path, dpi=config.DEFAULT_CHART_DPI, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    @staticmethod
    def _combine_gametes(gamete1, gamete2):
        """
        Combine two gametes into offspring genotype.
        Sorts so dominant (uppercase) comes first.
        
        Args:
            gamete1: String like "EW"
            gamete2: String like "ew"
            
        Returns:
            String like "Ee Ww"
        """
        if len(gamete1) != len(gamete2):
            raise ValueError("Gametes must have same number of genes")
        
        offspring_pairs = []
        for i in range(len(gamete1)):
            allele1 = gamete1[i]
            allele2 = gamete2[i]
            
            # Sort so uppercase (dominant) comes first
            pair = "".join(sorted([allele1, allele2], 
                                 key=lambda x: (x.lower(), x.islower())))
            offspring_pairs.append(pair)
        
        return " ".join(offspring_pairs)