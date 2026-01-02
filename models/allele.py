# ============================================================================
# FILE: models/allele.py
# Represents a single allele (genetic variant)
# ============================================================================

class Allele:
    """
    Represents a single allele (genetic variant) for a trait.
    
    Attributes:
        symbol: Letter representing the allele (e.g., 'E' or 'e')
        description: What this allele codes for (e.g., 'Red eyes')
        is_dominant: Whether this is the dominant allele
    """
    
    def __init__(self, symbol, description, is_dominant=False):
        """
        Initialize an allele.
        
        Args:
            symbol: Single letter representing the allele
            description: Phenotype this allele produces
            is_dominant: True if dominant, False if recessive
        """
        self.symbol = symbol
        self.description = description
        self.is_dominant = is_dominant
    
    def to_dict(self):
        """Convert allele to dictionary for storage."""
        return {
            "symbol": self.symbol,
            "description": self.description,
            "is_dominant": self.is_dominant
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create allele from dictionary."""
        return cls(
            symbol=data["symbol"],
            description=data["description"],
            is_dominant=data["is_dominant"]
        )
    
    def __repr__(self):
        return f"Allele({self.symbol}, {self.description}, dominant={self.is_dominant})"
