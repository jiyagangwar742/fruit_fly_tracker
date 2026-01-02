# ============================================================================
# FILE: core/genetics.py
# Core genetics calculations: Punnett squares and phenotype ratios
# ============================================================================

from itertools import product
from collections import Counter

class GeneticsCalculator:
    """
    Handles genetic calculations including Punnett squares and phenotype ratios.
    """
    
    @staticmethod
    def generate_punnett_square(parent1, parent2):
        """
        Generate all offspring genotypes from a genetic cross.
        
        Args:
            parent1: Genotype object for parent 1
            parent2: Genotype object for parent 2
            
        Returns:
            List of offspring genotype strings
        """
        # Get all possible gametes from each parent
        parent1_gametes = parent1.get_gametes()
        parent2_gametes = parent2.get_gametes()
        
        # Combine all gametes to get offspring
        offspring = []
        for g1, g2 in product(parent1_gametes, parent2_gametes):
            # Combine gametes into offspring genotype
            offspring_genotype = GeneticsCalculator._combine_gametes(g1, g2)
            offspring.append(offspring_genotype)
        
        return offspring
    
    @staticmethod
    def _combine_gametes(gamete1, gamete2):
        """
        Combine two gametes into an offspring genotype.
        Sorts alleles so dominant comes first (convention).
        
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
            pair = "".join(sorted([allele1, allele2], key=lambda x: (x.lower(), x.islower())))
            offspring_pairs.append(pair)
        
        return " ".join(offspring_pairs)
    
    @staticmethod
    def calculate_genotype_ratios(offspring_genotypes):
        """
        Calculate ratios of different genotypes.
        
        Args:
            offspring_genotypes: List of genotype strings
            
        Returns:
            Dict mapping genotype to (count, ratio)
        """
        total = len(offspring_genotypes)
        counts = Counter(offspring_genotypes)
        
        ratios = {}
        for genotype, count in counts.items():
            ratios[genotype] = {
                "count": count,
                "ratio": count / total,
                "fraction": f"{count}/{total}"
            }
        
        return ratios
    
    @staticmethod
    def calculate_phenotype_ratios(offspring_genotypes, allele_definitions):
        """
        Calculate ratios of observable phenotypes based on dominance.
        
        Args:
            offspring_genotypes: List of genotype strings
            allele_definitions: Dict mapping allele symbols to Allele objects
            
        Returns:
            Dict mapping phenotype to (count, ratio)
        """
        phenotype_counts = Counter()
        
        for genotype in offspring_genotypes:
            phenotype = GeneticsCalculator._genotype_to_phenotype(
                genotype, allele_definitions
            )
            phenotype_counts[phenotype] += 1
        
        total = len(offspring_genotypes)
        ratios = {}
        for phenotype, count in phenotype_counts.items():
            ratios[phenotype] = {
                "count": count,
                "ratio": count / total,
                "fraction": f"{count}/{total}"
            }
        
        return ratios
    
    @staticmethod
    def _genotype_to_phenotype(genotype_string, allele_definitions):
        """
        Convert genotype to observable phenotype using dominance rules.
        
        Args:
            genotype_string: String like "Ee Ww"
            allele_definitions: Dict of allele symbols to Allele objects
            
        Returns:
            String describing phenotype (e.g., "Red eyes, Normal wings")
        """
        gene_pairs = genotype_string.split()
        phenotype_parts = []
        
        for pair in gene_pairs:
            # Get both alleles in the pair
            allele1_symbol = pair[0]
            allele2_symbol = pair[1]
            
            # Check which allele is dominant
            allele1 = allele_definitions.get(allele1_symbol)
            allele2 = allele_definitions.get(allele2_symbol)
            
            if not allele1 or not allele2:
                raise ValueError(f"Allele definition missing for {pair}")
            
            # Determine phenotype based on dominance
            if allele1.is_dominant or allele1_symbol == allele2_symbol:
                phenotype_parts.append(allele1.description)
            elif allele2.is_dominant:
                phenotype_parts.append(allele2.description)
            else:
                # Both recessive - use the description of either
                phenotype_parts.append(allele2.description)
        
        return ", ".join(phenotype_parts)
    
    @staticmethod
    def calculate_expected_counts(phenotype_ratios, total_expected):
        """
        Calculate expected counts for each phenotype.
        
        Args:
            phenotype_ratios: Dict from calculate_phenotype_ratios
            total_expected: Total number of offspring expected
            
        Returns:
            Dict mapping phenotype to expected count
        """
        expected_counts = {}
        for phenotype, data in phenotype_ratios.items():
            expected_counts[phenotype] = round(data["ratio"] * total_expected, 1)
        
        return expected_counts