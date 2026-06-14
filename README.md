# Tokenization and Stemming Approaches for Turkish

**Author:** Tarık Emre Tıraş (Boğaziçi University)

A collection of preprocessing tools for Turkish text, designed for compatibility with Universal Dependencies (UD) standards. This repository contains a rule-based stemmer, a rule-based tokenizer with optional multiword expression (MWE) support, and a character-level statistical machine learning tokenizer.

## Components & Methodology

### 1. Rule-Based Stemmer
* **Stripping & Lexicon**: Implements ordered suffix stripping using inflectional and derivational suffix inventories, validating candidate stems against a root lexicon of approximately 38K forms.
* **Morphophonemic Repairs**: Includes dedicated repair modules to handle Turkish phonological shifts, such as vowel alternations, consonant devoicing ($b\rightarrow p, d\rightarrow t, g\rightarrow k$), and consonant gemination.
* **Normalization**: Uses a shared Unicode normalization step (NFKC/NFC) alongside Turkish-specific lowercasing to avoid dotted/undotted 'i' character mismatches.

### 2. Rule-Based Tokenizer
* **Regex Engine**: Employs regular expression patterns optimized to isolate punctuation, numbers, timestamps, and web elements (URLs, emails, hashtags).
* **Orthographic Post-Processing**: Manages abbreviations via an explicit lookup array, safeguards Roman numerals, and handles proper-noun apostrophe suffixes correctly.
* **Optional MWE Merger**: Utilizes a longest-match strategy using exact matching and head-lemma matching rules, utilizing a lexicon drawn from the Kenet Turkish WordNet.

### 3. Character-Level Logistic Regression Tokenizer
* **Feature Space**: Maps a 27-feature space tracking character classifications (uppercase, lowercase, digits, spacing, punctuation), neighboring character contexts, and specific structural layouts (e.g., URL components or decimal indicators).
* **Classification Engine**: Trains an $l_2$-regularized linear binary logistic regression classifier over character arrays to predict token-start or continuation boundaries natively according to UD principles.

## Performance Evaluation

All components were evaluated against reference partitions from Turkish Universal Dependencies treebanks (BOUN-UD and Kenet).

| Component | Evaluation Dataset Split | Evaluation Metric | Result |
| :--- | :--- | :--- | :---: |
| **Rule-Based Stemmer** | BOUN-UD Dev Split | Strict Exact-Match Accuracy | 80.2% |
| | BOUN-UD Dev Split | Soft Accuracy ($\ge 0.7$ similarity) | 93.3% |
| **Rule-Based Tokenizer** | Kenet UD Treebank | Sentence-Level Exact Match | 99.73% |
| *(UD-Compatible)* | Kenet UD Treebank | Average Token Jaccard Similarity | 0.999 |
| **MWE Merger Mode** | Independent 201-Sentence Set | Multiword Expression F1-Score | 0.822 |
| **ML Tokenizer** | BOUN-UD Test Split | Character-Level Boundary Accuracy | ~0.99 |
| *(Logistic Regression)* | BOUN-UD Test Split | Macro F1-Score (Boundary vs. Continuation) | 0.97 |

* **Strict vs. Soft Analysis**: The stemmer's strict metrics reflect the granular lemma assignments for complex derivative variations found in UD, while soft sequence matching tracks authentic morphophonemic performance closely.
