# Data Lineage Generator
from lineage.engine import LineageEngine


def main():

    engine = LineageEngine()

    engine.run()


if __name__ == "__main__":
    main()