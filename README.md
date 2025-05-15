# Informatter

## Extraction, Ordering, and Tokenization of Scientific Manuscripts

Python helper code for extraction, ordering, and tokenization of scientific manuscripts using The Semantic Scholar Open Research Corpus [S2ORC](https://github.com/allenai/s2orc) manuscripts database and [mat2vec](https://github.com/materialsintelligence/mat2vec?tab=readme-ov-file#thermoelectric-data). 

Full-text manuscripts, published in the English language, can be selected and extracted according to their respective S2ORC metadata tags (e.g, chemistry, physics, and materials science, and more) and further partitioned into sentences using the [SciSpaCy](https://allenai.github.io/scispacy/) tokenizer. The `en_core_sci_sm` model, focused on the biomedical domain, is a default selection that can be manually modified in a provided requirements.txt file. Each sentence is stored in a text file, one sentence per line of a file, by which a corpus of documents for training a Word2vec-type model is generated. Before storing the partitioned manuscript in a corpus, the mat2vec native tokenizer can be used to process and tokenize sentences using the ChemDataExtractor tokenizer. All tokens are lower-cased except chemical formulas (H2O, MgH2) and units of measurement (0C, kJ/mol, A/m2).

- For `extractor.py` file to work, it requires `Python3.9` version, as well as earlier versions of other libraries, all of which are listed in the requirements.txt file.

Corpus files - materials science, chemistry, physics, and mixed - generated with this code were used to train the mat2vec model. Domain-specific corpora ready for training are open-sourced [here](https://doi.org/10.6084/m9.figshare.28740341) and domain-specific trained models - Chem300, Phys300, MatSci200, MatSci300, and Mixed300 are open-sourced [here](https://doi.org/10.6084/m9.figshare.28740122). To fully reproduce the corpora files and trained models, one is required to install the [mat2vec](https://github.com/materialsintelligence/mat2vec?tab=readme-ov-file#thermoelectric-data) module with all its requirements and use it for model training.
