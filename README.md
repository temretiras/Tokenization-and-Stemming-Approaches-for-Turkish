# Tokenization and Stemming Approaches for Turkish

A small research and implementation repository exploring tokenization and stemming methods for the Turkish language. The project contains Python implementations, experiments, and examples demonstrating different tokenization strategies and stemming/lemmatization techniques suited for Turkish.

## Contents
- tokenization/: scripts and modules for tokenizing Turkish text (rule-based, regex, library-based)
- stemming/: implementations of stemming and light-stemming approaches and experiments
- notebooks/: Jupyter notebooks with experiments and visualizations
- data/: sample datasets and preprocessing scripts
- requirements.txt: Python dependencies

## Features
- Compare different tokenization approaches for Turkish (whitespace, rule-based, regex, library)
- Evaluate stemming and light-stemming methods for Turkish morphology
- Example notebooks to reproduce experiments

## Installation
1. Clone the repository:

   git clone https://github.com/temretiras/Tokenization-and-Stemming-Approaches-for-Turkish.git
   cd Tokenization-and-Stemming-Approaches-for-Turkish

2. Create a virtual environment (recommended) and install dependencies:

   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt

## Usage
- Explore the `notebooks/` folder for example workflows and experiments.
- Run individual scripts in `tokenization/` and `stemming/` to preprocess text and test algorithms.

Example (run a tokenizer script):

   python tokenization/example_tokenizer.py --input data/example.txt --output data/example.tokenized.txt

## Project structure
- tokenization/ — tokenizer implementations and utilities
- stemming/ — stemmers, light-stemmers and evaluation tools
- notebooks/ — Jupyter notebooks for experiments
- data/ — example datasets and preprocessing scripts

## Contributing
Contributions, issues and feature requests are welcome. Please open an issue or submit a pull request.

## License
This project is released under the MIT License. See LICENSE for details.

## Contact
Repository: https://github.com/temretiras/Tokenization-and-Stemming-Approaches-for-Turkish

If you want me to customize the README (add badges, examples, or a detailed usage section), tell me what you'd like to include.