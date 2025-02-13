## SPARC data directory generation to sub and sam

Parses a data directory for dicom (.dcm) files and creates a sparc-like target directory containing subject and sam directory.

Result.csv contains created mapping and file origins.

## authors: Björn van der Ster and Berend Westerhof

### 13-Feb-2025

### Requirements:

- Python v3.10 or newer
- Optionally git for cloning

### Setup

- Clone the repository  
   `git clone https://github.com/mesabjorn/sparc-dirs
`
- Optionally create a virtual environment
  `python -m venv venv`
- Install dependencies:
  `venv\scripts\pip install -r requirements.txt`

### Usage

- Start main.py with your data directory and target directory (optional defaults to ./sparc-data)

`venv\scripts\python main.py --generic_data_dir /your/data/directory [--sparc_base_dir] /your/target/sparc/directory`

- Wait to finish: sparc_base_dir should then have a primary folder which contains all data: a subject folder for every folder in generic_data_dir and a sam directory for every sample collection
