from pathlib import Path
import argparse

from src.sparc import convert_to_sparc


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Convert a generic data directory to SPARC format.")
    parser.add_argument("--generic_data_dir", type=Path, default=Path("./generic_data"), help="Path to the generic data directory.")
    parser.add_argument("--sparc_base_dir", type=Path, default=Path("./sparc_data"), help="Path to the output SPARC directory.")
    
    return parser.parse_args()

def main():
    args = parse_cli_args()
    convert_to_sparc(args.generic_data_dir, args.sparc_base_dir)

if __name__ == "__main__":
    main()