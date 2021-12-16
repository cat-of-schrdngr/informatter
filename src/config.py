import sys
from pathlib import Path

from dotenv import dotenv_values

import os
# from dotenv import load_dotenv

dotenv_path = Path("src/.env")
print(dotenv_path)

# load_dotenv(dotenv_path=dotenv_path)

# BASE_DIR = os.getenv('BASE_DIR')
BASE_DIR = Path(dotenv_values(dotenv_path)["BASE_DIR"])
# BASE_DIR = Path(dotenv_values(".env")["BASE_DIR"])
print("BASE_DIR:", BASE_DIR)


# Path to zipped S2ORC metadata and full pdf files.
s2orc_mzip = "s2orc/20200705v1/full/metadata/gzip"
s2orc_pzip = "s2orc/20200705v1/full/pdf_parses/gzip"

metadata_path = Path.joinpath(BASE_DIR, s2orc_mzip)
pdf_path = Path.joinpath(BASE_DIR, s2orc_pzip)

# A path to file containing saved corpus.
corpus = Path.cwd() / "data/corpus/corpus"
corpus_sample = Path.cwd() / "data/corpus/corpus_sample"
one_pdf_corpus = Path.cwd() / "data/corpus/one_pdf_corpus"

# Sample files are stored in the local project.
meta_sample_gz = Path.cwd() / "data/gzip/sample_meta.jsonl.gz"
pdf_sample_gz = Path.cwd() / "data/gzip/sample_pdf.jsonl.gz"

m2v_lib = Path.joinpath(Path.home(), BASE_DIR, "m2v")
try:
    sys.path.append(str(m2v_lib))
except ModuleNotFoundError:
    print("mat2vec library is not in designated path.")

# Variable __all__ explicitly lists the exported names if import statement
# includes * (i.e, from config import *)
__all__ = [
    "BASE_DIR",
    "metadata_path",
    "pdf_path",
    "corpus",
    "one_pdf_corpus"

    # TODO: What's the problem with corpus_sample? The code creates, but it
    #  doesn't save the file.

    # To test the sample gz files comment above metadata_path and pdf_path,
    # and uncomment corpus = corpus_sample line in save_corpus.
    # "pdf_sample_gz",
    # "meta_sample_gz",
    # "corpus_sample"
]
