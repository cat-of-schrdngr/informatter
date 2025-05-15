# Informatter

## Extraction, Ordering, and Tokenization of Scientific Manuscripts

Python helper code for extraction, ordering, and tokenization of scientific manuscripts using The Semantic Scholar Open Research Corpus [S2ORC](https://github.com/allenai/s2orc) manuscripts database and [mat2vec](https://github.com/materialsintelligence/mat2vec?tab=readme-ov-file#thermoelectric-data). 

Full-text manuscripts, published in the English language, can be selected and extracted according to their respective S2ORC metadata tags (e.g, chemistry, physics, and materials science, and more) and further partitioned into sentences using the [SciSpaCy](https://allenai.github.io/scispacy/) tokenizer. The `en_core_sci_sm` model, focused on the biomedical domain, is a default selection that can be manually modified in a provided requirements.txt file. Each sentence is stored in a text file, one sentence per line of a file, by which a corpus of documents for training a Word2vec-type model is generated. Before storing the partitioned manuscript in a corpus, the mat2vec native tokenizer can be used to process and tokenize sentences using the [ChemDataExtractor](http://chemdataextractor.org/) tokenizer. All tokens are lower-cased except chemical formulas (e.g., H2O, MgH2) and units of measurement (e.g., 0C, kJ/mol, A/m2).

- For `extractor.py` file to work, it requires `Python3.9` version, as well as earlier versions of other libraries, all of which are listed in the requirements.txt file.

### Generated corpora and trained models 

Using the code provided in this repository, four corpora files were generated based on the S2ORC tags: materials science, chemistry, and physics. Materials science (corpus-matsci980k), chemistry (corpus-chem980k), and physics (corpus-phys900k) corpora contain roughly 3.6 million tokens, with approximately 900k unique terms, while the mixed corpus (corpus-mixed1800k), generated as a mixture of documents in the following percentage, chemistry:matsci:physics = 23:32:45, contains about 7.7 million tokens with approximately 1800k unique terms. During the assembly process, the absolute number of articles from the given domain was assumed to be insignificant as long as the total number of generated tokens was aligned across corpora.

- All four domain-specific corpora (corpus-mixed1800k, corpus-matsci980k, corpus-chem980k, corpus-phys900k) ready for training are open-sourced [here](https://doi.org/10.6084/m9.figshare.28740341). 

The corpora were used to generate domain-specific word embeddings using Word2vec, a natural language processing technique comprised of language model architectures for fast and efficient learning of distributed representations of words. Continuous Skip-gram model architecture with a negative sampling strategy, as implemented in the Gensim library, is employed for model training. The word embeddings, consisting of 200 and 300 vectorial components for materials science and 300 vectorial components for chemistry, physics, and mixed domains, are provided. To fully reproduce the corpora files and trained models, one is required to install the [mat2vec](https://github.com/materialsintelligence/mat2vec?tab=readme-ov-file#thermoelectric-data) module with all its requirements and use it for model training.

- All domain-specific trained models (Chem300, Phys300, MatSci200, MatSci300, and Mixed300) are open-sourced [here](https://doi.org/10.6084/m9.figshare.28740122). 

