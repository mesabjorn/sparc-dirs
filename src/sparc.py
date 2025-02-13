from pathlib import Path
import shutil
import json
from typing import Union

import hashlib

import pandas as pd


def sha256_to_str(name: str) -> str:
    return hashlib.sha256(bytes(name)).hexdigest()


from . import logger


def create_sparc_directories(base_dir: Union[str, Path]) -> None:
    """Creates the necessary SPARC directory structure."""
    base_path = Path(base_dir)
    structure = [
        "primary",
        "derivative",
        "code",
        "protocol",
        "docs",
        "source",
        "manifest",  # This folder holds dataset_description and other metadata
    ]

    for folder in structure:
        (base_path / folder).mkdir(parents=True, exist_ok=True)
    logger.info("SPARC directory structure created.")


def move_files_to_sparc(
    generic_data_dir: Union[str, Path], sparc_base_dir: Union[str, Path]
) -> None:
    """Moves data files to appropriate SPARC folders based on a simple heuristic."""
    generic_path = Path(generic_data_dir)
    sparc_path = Path(sparc_base_dir)
    rows = []
    subcount = 0
    for subject in generic_path.iterdir():
        if not subject.is_dir():
            continue
        subject_name = f"sub-{subcount:03d}"

        for file in subject.rglob("*"):
            if file.is_file():
                if file.suffix in {".csv", ".dcm"} or "raw" in file.stem.lower():
                    dest_folder = "primary"
                elif file.suffix == ".json" or "processed" in file.stem.lower():
                    dest_folder = "derivative"
                elif file.suffix in {".py", ".m"}:
                    dest_folder = "code"
                elif "protocol" in file.stem.lower():
                    dest_folder = "protocol"
                elif file.suffix in {".pdf", ".docx"}:
                    dest_folder = "docs"
                else:
                    dest_folder = "source"
                if file.suffix == ".dcm":
                    relative_path = file.relative_to(generic_path)
                    h = sha256_to_str(relative_path.parent)
                    dest_folder += f"/{subject_name}/{h}"

                    row = [
                        dest_folder,
                        str(relative_path.parent),
                        str(relative_path.name),
                        len(list(file.parent.iterdir())),
                    ]
                    rows.append(row)

                dest_path = sparc_path / dest_folder / file.name
                dest_path.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy(str(file), str(dest_path))
                logger.info(f"Moved {file.name} to {dest_path}/")
        subcount += 1
    "return result rows as a pandas dataframe"
    df = pd.DataFrame(
        rows,
        columns=["target_location", "original_location", "filename", "n_files"],
    )
    return df


def create_dataset_description(sparc_base_dir: Union[str, Path]) -> None:
    """Creates a basic dataset_description.json file."""
    metadata = {
        "name": "Example SPARC Dataset",
        "description": "This is a dataset formatted according to SPARC standards.",
        "keywords": ["example", "SPARC", "data"],
        "contributors": [{"name": "John Doe", "role": "Data Curator"}],
        "funding": ["NIH Grant XYZ"],
        "license": "CC-BY-4.0",
        "dataset_identifier": "10.0000/example",
    }

    manifest_dir = Path(sparc_base_dir) / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_dir / "dataset_description.json", "w") as f:
        json.dump(metadata, f, indent=4)
    logger.info("dataset_description.json created.")


def generate_sam(sparc_path: Path, df: pd.DataFrame):
    samcounter = 0
    sam_mapping = {}

    for d in df.target_location.unique():
        target_location = sparc_path / d
        samname = f"sam-{samcounter:03d}"

        if target_location.exists() and target_location.is_dir():
            new_location = target_location.parent / samname
            target_location.rename(new_location)
            sam_mapping[d] = new_location  # Map original to new name
        else:
            sam_mapping[d] = None  # Preserve structure even if path doesn't exist
        samcounter += 1
    # Assign correct sam_name to each row based on target_location
    df["target_location"] = df["target_location"].map(sam_mapping)
    return df


def convert_to_sparc(
    generic_data_dir: Union[str, Path], sparc_base_dir: Union[str, Path],outputfile:str|Path
) -> None:
    """Converts a generic data directory into SPARC format."""
    create_sparc_directories(sparc_base_dir)
    df = move_files_to_sparc(generic_data_dir, sparc_base_dir)
    
    df = generate_sam(sparc_base_dir, df)
    df.to_csv(outputfile, encoding="utf-8", index=False)
    logger.info(f"created csv file: {outputfile}")

    create_dataset_description(sparc_base_dir)
    logger.info("Conversion to SPARC format complete.")
