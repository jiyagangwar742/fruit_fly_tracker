# ============================================================================
# FILE: cli/display.py
# CLI display formatting utilities
# ============================================================================

from datetime import datetime

class Display:
    """Formatting utilities for CLI display."""
    
    @staticmethod
    def header(text):
        """Display a header."""
        line = "=" * 60
        print(f"\n{line}")
        print(text.center(60))
        print(f"{line}\n")
    
    @staticmethod
    def section(text):
        """Display a section header."""
        print(f"\n{text}")
        print("-" * len(text))
    
    @staticmethod
    def table(headers, rows):
        """Display a simple table."""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
    
    @staticmethod
    def success(text):
        """Display success message."""
        print(f"✓ {text}")
    
    @staticmethod
    def error(text):
        """Display error message."""
        print(f"✗ {text}")
    
    @staticmethod
    def info(text):
        """Display info message."""
        print(f"ℹ {text}")
