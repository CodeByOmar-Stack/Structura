"""Main entry point for GestorCarpetas application."""

from ui import GestorCarpetasUI


def main():
    """Run the application."""
    try:
        app = GestorCarpetasUI()
        app.run()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
