# ============================================================================
# FILE: core/statistics.py
# Statistical analysis (chi-square test)
# ============================================================================

from scipy import stats
import config

class StatisticalAnalyzer:
    """
    Performs statistical analysis on genetics experiment results.
    """
    
    @staticmethod
    def chi_square_test(expected_counts, observed_counts, alpha=None):
        """
        Perform chi-square goodness-of-fit test.
        
        Args:
            expected_counts: Dict mapping phenotype to expected count
            observed_counts: Dict mapping phenotype to observed count
            alpha: Significance level (uses config default if None)
            
        Returns:
            Dict with chi_square, p_value, degrees_freedom, critical_value, passed
        """
        if alpha is None:
            alpha = config.ALPHA_LEVEL
        
        # Ensure same phenotypes in both dicts
        if set(expected_counts.keys()) != set(observed_counts.keys()):
            raise ValueError("Expected and observed must have same phenotypes")
        
        # Get lists in same order
        phenotypes = list(expected_counts.keys())
        expected = [expected_counts[p] for p in phenotypes]
        observed = [observed_counts[p] for p in phenotypes]
        
        # Perform chi-square test
        chi_square, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
        
        # Degrees of freedom
        df = len(phenotypes) - 1
        
        # Critical value at given alpha
        critical_value = stats.chi2.ppf(1 - alpha, df)
        
        # Test passes if chi_square < critical_value (or p_value > alpha)
        passed = chi_square < critical_value
        
        return {
            "chi_square": round(chi_square, 3),
            "p_value": round(p_value, 3),
            "degrees_freedom": df,
            "critical_value": round(critical_value, 3),
            "alpha": alpha,
            "passed": passed,
            "interpretation": StatisticalAnalyzer._interpret_result(passed)
        }
    
    @staticmethod
    def _interpret_result(passed):
        """Generate human-readable interpretation."""
        if passed:
            return ("Your observed data matches the expected Mendelian ratios. "
                   "There is no statistically significant deviation.")
        else:
            return ("Your observed data significantly deviates from expected ratios. "
                   "This may indicate: counting error, selection bias, or different "
                   "genetic mechanism than predicted.")

