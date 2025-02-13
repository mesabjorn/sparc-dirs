from pathlib import Path
import argparse
from src import await_input, logger

from src.sparc import convert_to_sparc

import shutil


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Convert a generic data directory to SPARC format."
    )
    parser.add_argument(
        "--generic_data_dir",
        type=Path,
        default=Path("./generic_data"),
        help="Path to the generic data directory.",
    )
    parser.add_argument(
        "--sparc_base_dir",
        type=Path,
        default=Path("./sparc_data"),
        help="Path to the output SPARC directory.",
    )
    parser.add_argument(
        "--outputfile",
        type=Path,
        default=Path("result.csv"),
        help="Output database of moved files",
    )

    return parser.parse_args()


def main():
    args = parse_cli_args()
    source_path,target_path = args.generic_data_dir,args.sparc_base_dir
    if target_path.exists():
        answer = await_input(f"{target_path} already exists? Delete (y/n)?", allow=["y","n"])
        if answer == "y":
            shutil.rmtree(args.sparc_base_dir)
    convert_to_sparc(source_path, target_path, outputfile = args.outputfile)


if __name__ == "__main__":
    main()
