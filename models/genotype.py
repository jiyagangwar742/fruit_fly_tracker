# ============================================================================
# FILE: models/genotype.py
# Represents a genotype (genetic makeup) for one or more traits
# ============================================================================

from models.allele import Allele

class Genotype:
    """
    Represents the genetic makeup (genotype) of an organism.
    Can handle single or multiple traits.
    
    Attributes:
        alleles: Dictionary mapping trait names to pairs of alleles
                Example: {"eye_color": ("E", "e"), "wing": ("W", "w")}
    """
    
    def __init__(self, genotype_string, allele_definitions):
        """
        Initialize a genotype from a string like "Ee Ww".
        
        Args:
            genotype_string: String like "Ee" or "Ee Ww" representing genotype
            allele_definitions: Dict mapping symbols to Allele objects
        """
        self.genotype_string = genotype_string.strip()
        self.allele_definitions = allele_definitions
        self.alleles = self._parse_genotype()
    
    def _parse_genotype(self):
        """
        Parse genotype string into structured format.
        
        Returns:
            Dictionary of trait names to allele pairs
        """
        # Split by spaces to get individual gene pairs (e.g., ["Ee", "Ww"])
        gene_pairs = self.genotype_string.split()
        
        alleles = {}
        for i, pair in enumerate(gene_pairs):
            if len(pair) != 2:
                raise ValueError(f"Each gene must have exactly 2 alleles. Got: {pair}")
            
            trait_name = f"trait_{i+1}"
            alleles[trait_name] = (pair[0], pair[1])
        
        return alleles
    
    def get_gametes(self):
        """
        Generate all possible gametes (sex cells) this genotype can produce.
        Uses combinatorics for multiple traits.
        
        Returns:
            List of gamete strings (e.g., ["EW", "Ew", "eW", "ew"] for EeWw)
        """
        from itertools import product
        
        # Get one allele from each trait for each gamete
        allele_choices = []
        for trait_alleles in self.alleles.values():
            allele_choices.append(list(trait_alleles))
        
        # Generate all combinations
        gametes = []
        for combination in product(*allele_choices):
            gametes.append("".join(combination))
        
        return list(set(gametes))  # Remove duplicates
    
    def to_dict(self):
        """Convert to dictionary for storage."""
        return {
            "genotype_string": self.genotype_string,
            "alleles": self.alleles
        }
    
    @classmethod
    def from_dict(cls, data, allele_definitions):
        """Create from dictionary."""
        return cls(data["genotype_string"], allele_definitions)
    
    def __str__(self):
        return self.genotype_string
    
    def __repr__(self):
        return f"Genotype({self.genotype_string})"