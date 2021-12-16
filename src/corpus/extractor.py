import sys
import gzip
import json
import logging

import regex as re
import pandas as pd
from pathlib import Path
from typing import Union, Generator

from src.config import *
from src.corpus import timer

from mat2vec.processing import MaterialsTextProcessor

_logger = logging.getLogger(__name__)

text_processor = MaterialsTextProcessor()


@timer
def metadata_to_csv(batch: int, fields: list, file_path: Union[str, Path]):
    """
    Returns csv formatted file to which dataframe containing metadata, such as
    paper_id and field of study, is stored.
    :param batch: int;
    :param fields: list of str indicating field of studies;
    :param file_path: path to output metadata csv file;
    :return: csv file.
    """
    _batch = f"BATCH: {batch} "
    try:
        gz_file = f"metadata_{batch}.jsonl.gz"
        meta_gz = Path.joinpath(metadata_path, gz_file)
    except NameError:
        meta_gz = meta_sample_gz
        sufix = ".csv"
        file_path = "".join(file_path.removesuffix(sufix) + "_sample" + sufix)
        print(file_path)

    for field in fields:
        meta_df = _load_metadata_to_df(field, meta_gz)
        try:
            if fields.index(field) == 0:
                meta_df.to_csv(file_path, mode="a", sep="\t", index=False)
            else:
                meta_df.to_csv(file_path, mode="a", sep="\t", index=False,
                               header=False)
        except ValueError:
            pass

        df_size = sys.getsizeof(meta_df) / 1024 ** 2
        _info = f"FIELD: {field:23} #{meta_df.shape[0]:2} pdfs: {df_size:.3f} MB"
        _msg = "".join(_batch + _info)
        _logger.info(_msg)
        print(_msg)


def _load_metadata_to_df(field: str, file_path: Union[str, Path],
                         keep_other_ids=False) -> pd.DataFrame:
    """
    Selects manuscripts, published in English and associated with fixed field of
    study (e.g. Chemistry), while containing only full body text, to store them
    in metadata dataframe for further addendum of body text to corpus.
    :param field: str indicating field of study;
    :param file_path: path to metadata gzip file (metadata_batch.jsonl.gz)
    :param keep_other_ids: bool; True if alternative manuscripts' ids, such as
    arxiv_id, doi, pubmed_id, etc. are saved in df, otherwise False.
    :return: pd.DataFrame containing filtered metadata.
    """
    df = pd.DataFrame()
    # METADATA: Unzipping jsonl file.
    data = _parse_s2orc_jsonl(file_path)
    english_check = re.compile(r'[a-zA-Z0-9αβγδεπσηχ()"”{}$*_-]')
    # Searching full text manuscripts.
    for line in data:
        # Save pdf of manuscripts with available full text and for selected
        # field of study.
        try:
            if line["has_pdf_body_text"]:
                try:
                    if field in line["mag_field_of_study"]:
                        # After verifying the presence of full body text in the
                        # S2ORC manuscript, inspect weather the manuscript is
                        # written in English. If so, remove those pdfs from
                        # the selection or further processing.
                        if not english_check.match(line["title"]):
                            _msg = line["title"]
                            _logger.info(_msg)
                            print(_msg)
                        else:
                            del line["abstract"]
                            del line["authors"]
                            del line["has_inbound_citations"]
                            del line["has_outbound_citations"]
                            del line["has_pdf_body_text"]
                            del line["has_pdf_parse"]
                            del line["has_pdf_parsed_abstract"]
                            del line["has_pdf_parsed_bib_entries"]
                            del line["has_pdf_parsed_body_text"]
                            del line["has_pdf_parsed_ref_entries"]
                            del line["inbound_citations"]
                            del line["journal"]
                            # del line["mag_field_of_study"]
                            del line["outbound_citations"]
                            del line["s2_url"]
                            del line["title"]
                            del line["venue"]
                            del line["year"]
                            if not keep_other_ids:
                                # Keep or delete manuscripts' identification.
                                del line["arxiv_id"]
                                del line["acl_id"]
                                del line["pmc_id"]
                                del line["pubmed_id"]
                                del line["mag_id"]
                                # del line["doi"]
                            df = df.append(line, ignore_index=True)
                except TypeError:
                    pass
        except KeyError:
            pass
    return df


def save_corpus(batch: int, csv_filename: Union[str, Path],
                segment_sentences: bool, remove_references: bool):
    """
    Loads csv metadata as pandas dataframe, removes duplicate ids, and saves
    tokenized body text to corpus file set for training.
    """
    try:
        gz_file = f"pdf_parses_{batch}.jsonl.gz"
        pdf_gz = Path.joinpath(pdf_path, gz_file)
    except NameError:
        # In case of using the corpus_sample S2ORC files uncomment the
        # following lines.
        pdf_gz = pdf_sample_gz
        # corpus = corpus_sample

    if not Path(csv_filename).is_file():
        print("Use sample metadata ids!")
        sufix = ".csv"
        csv_filename = "".join(csv_filename.removesuffix(sufix) + "_sample" + sufix)

    df = pd.read_csv(csv_filename, delimiter="\t")
    df.drop_duplicates(subset='paper_id', keep="first", inplace=True)
    df_size = sys.getsizeof(df) / 1024 ** 2
    _msg = f"Total metadata: #{df.shape[0]} pdfs = {df_size:.3f} MB"
    _logger.info(_msg)

    with open(corpus, "a", encoding="utf-8") as file:
        text_generator = _bodytext_generator(pdf_gz, df)
        for pdf in text_generator:
            token_generator = tokenize(text_processor, pdf, segment_sentences,
                                       remove_references)
            for token in token_generator:
                file.write(token + '\n')

        # Check the size of corpus object.
        csize = file.tell() / 1024 ** 2
        _msg = f"corpus size = {csize:.3f} MB\n"
        _logger.info(_msg)
        print(_msg)
    # with open(corpus, "a", encoding="utf-8") as file:


def _bodytext_generator(pdfs_path: Union[str, Path],
                        df: pd.DataFrame) -> Generator[str, None, None]:
    """
    Selects pdfs with S2ORC id corresponding to those in metadata dataframe
    and returns them as body_text generator.
    :param pdfs_path: path to pdf_parses_batch.json.gz
    :param df: metadata dataframe
    :return: body_text generator
    """
    print("\nFiltering pdfs using S2ORC ids stored in metadata df...")
    data = _parse_s2orc_jsonl(pdfs_path)
    for line in data:
        pid = int(line["paper_id"])
        if df["paper_id"].isin([pid]).any():
            body_text = body_of_manuscript(line["body_text"])
            yield body_text


def one_pdf(ids, dois, index=0):
    """Unzip & extract one S2ORC manuscript for inspection."""
    # fields = ["Materials Science"]
    batch = 0
    paper_id = ids[index]
    doi = dois[index]
    y_n = input("Tokenize text? y/n: ")
    if y_n == "n":
        tokenize_pdf = False
    else:
        tokenize_pdf = True
    print(f"\nSaving file \tBATCH: {batch} \tDOI: {doi} \tpaper_id: {paper_id}")
    save_one_file(batch, paper_id, doi, tokenize_pdf)


def save_one_file(batch: int, paper_id: str, doi: str, tokenize_pdf: bool):
    gz_file = f"pdf_parses_{batch}.jsonl.gz"
    pdf_gz = Path.joinpath(pdf_path, gz_file)
    with open(one_pdf_corpus, "a", encoding="utf-8") as file:
        pdf = _onepdf_bodytext_generator(pdf_gz, paper_id, doi)
        if not tokenize_pdf:
            file.write(pdf + '\n')
        else:
            token_generator = tokenize(text_processor, pdf, True, True)
            for token in token_generator:
                file.write(token + '\n')


def _onepdf_bodytext_generator(pdfs_path: Union[str, Path], paper_id: str, doi: str):
    data = _parse_s2orc_jsonl(pdfs_path)
    for line in data:
        if line["paper_id"] == paper_id:
            print(f"{doi} doi found...")
            body_text = body_of_manuscript(line["body_text"])
            return body_text


def _parse_s2orc_jsonl(file_path: Union[str, Path]):
    try:
        with gzip.GzipFile(file_path, 'rb') as jsonl_file:
            for line in jsonl_file:
                yield json.loads(line.decode("utf-8"))
    except json.JSONDecodeError:
        print("Error while reading json file.")
    except FileNotFoundError:
        print(f"JSON file not found at given path: \n{file_path}.")
        pass
    except EOFError:
        # _msg = "The compressed file is incomplete."
        pass


def body_of_manuscript(body_text: list) -> str:
    """Returns a string of S2ORC manuscript's raw text set for tokenization."""
    n = len(body_text)
    manuscript = [body_text[i]['text'] for i in range(n)]
    manuscript = " ".join(manuscript)
    return manuscript


def delete_references(tokens: str) -> str:
    # If references are provided as tokens, remove them from text:
    # "It has been widely used the literature [28] and [29]." ->
    # "It has been widely used in the literature."
    pattern = re.compile(r'\[.*?\]')
    tokens = re.sub(pattern, '<nUm>', tokens)
    return tokens


def scispacy_tokenizer(document: str) -> list:
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    doc = nlp(document)
    sentences_list = [sentence for sentence in doc.sents]
    return sentences_list


def tokenize(tokenizer, manuscript: str, segment_sentences: bool,
             remove_references: bool) -> str:
    """
    Returns string of processed text as tokens, tokenized using mat2vec type of
    text processor and tokenizer.
    :param segment_sentences: bool -- if True scispacy NLP tool will segment
        sentences in each manuscript, in which case every sentence will be
        stored in a separate line in the final corpus file.
    :param remove_references: bool -- True if references are to be replaced with <nUm>
    :param tokenizer: class -- Materials science text processing tool
    :param manuscript: str -- corresponding to S2ORC body text
    """
    if segment_sentences:
        sentences_list = scispacy_tokenizer(manuscript)
        for sentence in sentences_list:
            tokens_list = tokenizer.tokenize(
                text=str(sentence),
                split_oxidation=True,
                keep_sentences=False,
            )
            # Process further a pre-tokenized list of strings.
            tokens = tokenizer.process(
                tokens=tokens_list,
                exclude_punct=True,
                convert_num=True,
                normalize_materials=True,
                remove_accents=True,
                make_phrases=True,
                split_oxidation=True
            )
            tokens = " ".join(tokens[0])
            if remove_references:
                tokens = delete_references(tokens)
            yield tokens
    else:
        tokens_list = tokenizer.tokenize(
            text=manuscript,
            split_oxidation=True,
            keep_sentences=False,
        )
        tokens = tokenizer.process(
            tokens=tokens_list,
            exclude_punct=True,
            convert_num=True,
            normalize_materials=True,
            remove_accents=True,
            make_phrases=True,
            split_oxidation=True
        )
        tokens = " ".join(tokens[0])
        if remove_references:
            tokens = delete_references(tokens)
        return tokens


__all__ = [
    "metadata_to_csv",
    "save_corpus",
    "one_pdf"
]