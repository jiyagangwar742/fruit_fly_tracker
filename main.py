# ============================================================================
# FILE: main.py
# Main entry point for the CLI application
# ============================================================================

from cli.menu import MenuSystem

def main():
    """Main entry point for the application."""
    try:
        menu = MenuSystem()
        menu.start()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please report this issue.")

if __name__ == "__main__":
    main()