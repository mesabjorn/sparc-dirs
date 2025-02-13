from pathlib import Path
import shutil
import json
from typing import Union

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
        "manifest"  # This folder holds dataset_description and other metadata
    ]
    
    for folder in structure:
        (base_path / folder).mkdir(parents=True, exist_ok=True)
    logger.info("SPARC directory structure created.")

def move_files_to_sparc(generic_data_dir: Union[str, Path], sparc_base_dir: Union[str, Path]) -> None:
    """Moves data files to appropriate SPARC folders based on a simple heuristic."""
    generic_path = Path(generic_data_dir)
    sparc_path = Path(sparc_base_dir)
    
    for file in generic_path.rglob("*"):
        if file.is_file():
            if file.suffix == ".csv" or "raw" in file.stem.lower():
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
            
            dest_path = sparc_path / dest_folder / file.name
            shutil.move(str(file), str(dest_path))
            logger.info(f"Moved {file.name} to {dest_folder}/")

def create_dataset_description(sparc_base_dir: Union[str, Path]) -> None:
    """Creates a basic dataset_description.json file."""
    metadata = {
        "name": "Example SPARC Dataset",
        "description": "This is a dataset formatted according to SPARC standards.",
        "keywords": ["example", "SPARC", "data"],
        "contributors": [{
            "name": "John Doe",
            "role": "Data Curator"
        }],
        "funding": ["NIH Grant XYZ"],
        "license": "CC-BY-4.0",
        "dataset_identifier": "10.0000/example"
    }
    
    manifest_dir = Path(sparc_base_dir) / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    
    with open(manifest_dir / "dataset_description.json", "w") as f:
        json.dump(metadata, f, indent=4)
    logger.info("dataset_description.json created.")

def convert_to_sparc(generic_data_dir: Union[str, Path], sparc_base_dir: Union[str, Path]) -> None:
    """Converts a generic data directory into SPARC format."""
    create_sparc_directories(sparc_base_dir)
    move_files_to_sparc(generic_data_dir, sparc_base_dir)
    create_dataset_description(sparc_base_dir)
    logger.info("Conversion to SPARC format complete.")