
# ============================================================================
# FILE: models/experiment.py
# Represents a complete genetics experiment
# ============================================================================

from datetime import datetime
from models.genotype import Genotype
from models.allele import Allele

class Experiment:
    """
    Represents a complete fruit fly genetics experiment.
    
    Attributes:
        experiment_id: Unique identifier
        name: Human-readable experiment name
        date_created: When experiment was created
        parent1: Genotype of first parent
        parent2: Genotype of second parent
        allele_definitions: Dict of allele symbols to Allele objects
        expected_counts: Dict of phenotypes to expected counts
        observed_counts: Dict of phenotypes to observed counts (None until recorded)
        total_expected: Total number of offspring expected
        notes: User notes about the experiment
        chi_square_result: Statistical test result (None until observations added)
    """
    
    def __init__(self, experiment_id, name, parent1_string, parent2_string, 
                 allele_definitions, total_expected, notes=""):
        """
        Initialize a new experiment.
        
        Args:
            experiment_id: Unique ID (e.g., "EXP_001")
            name: Experiment name
            parent1_string: Genotype string for parent 1 (e.g., "Ee")
            parent2_string: Genotype string for parent 2 (e.g., "ee")
            allele_definitions: Dict mapping symbols to Allele objects
            total_expected: Expected number of offspring to count
            notes: Optional notes
        """
        self.experiment_id = experiment_id
        self.name = name
        self.date_created = datetime.now()
        self.date_modified = self.date_created
        self.allele_definitions = allele_definitions
        self.parent1 = Genotype(parent1_string, allele_definitions)
        self.parent2 = Genotype(parent2_string, allele_definitions)
        self.total_expected = total_expected
        self.expected_counts = {}  # Will be calculated
        self.observed_counts = None  # None until observations recorded
        self.notes = notes
        self.chi_square_result = None  # None until analysis run
    
    def set_expected_counts(self, expected_counts):
        """
        Set the expected counts for each phenotype.
        This is calculated by the genetics module.
        
        Args:
            expected_counts: Dict mapping phenotype to expected count
        """
        self.expected_counts = expected_counts
        self.date_modified = datetime.now()
    
    def add_observations(self, observed_counts):
        """
        Record observed counts from actual experiment.
        
        Args:
            observed_counts: Dict mapping phenotype to observed count
        """
        self.observed_counts = observed_counts
        self.date_modified = datetime.now()
    
    def set_chi_square_result(self, result):
        """
        Store chi-square statistical test result.
        
        Args:
            result: Dict with chi_square, p_value, passed keys
        """
        self.chi_square_result = result
        self.date_modified = datetime.now()
    
    def is_complete(self):
        """Check if experiment has observations recorded."""
        return self.observed_counts is not None
    
    def get_status(self):
        """Get human-readable status."""
        return "Complete" if self.is_complete() else "Pending"
    
    def to_dict(self):
        """Convert experiment to dictionary for storage."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "date_created": self.date_created.isoformat(),
            "date_modified": self.date_modified.isoformat(),
            "parent1": self.parent1.to_dict(),
            "parent2": self.parent2.to_dict(),
            "allele_definitions": {k: v.to_dict() for k, v in self.allele_definitions.items()},
            "total_expected": self.total_expected,
            "expected_counts": self.expected_counts,
            "observed_counts": self.observed_counts,
            "notes": self.notes,
            "chi_square_result": self.chi_square_result
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create experiment from dictionary."""
        # Reconstruct allele definitions
        allele_defs = {
            k: Allele.from_dict(v) 
            for k, v in data["allele_definitions"].items()
        }
        
        # Create experiment
        exp = cls(
            experiment_id=data["experiment_id"],
            name=data["name"],
            parent1_string=data["parent1"]["genotype_string"],
            parent2_string=data["parent2"]["genotype_string"],
            allele_definitions=allele_defs,
            total_expected=data["total_expected"],
            notes=data.get("notes", "")
        )
        
        # Restore dates
        exp.date_created = datetime.fromisoformat(data["date_created"])
        exp.date_modified = datetime.fromisoformat(data["date_modified"])
        
        # Restore calculated/observed data
        exp.expected_counts = data.get("expected_counts", {})
        exp.observed_counts = data.get("observed_counts")
        exp.chi_square_result = data.get("chi_square_result")
        
        return exp
    
    def __repr__(self):
        return f"Experiment({self.experiment_id}, {self.name}, {self.get_status()})"
