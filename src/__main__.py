from src.corpus import time_main, metadata_to_csv, save_corpus, one_pdf


@time_main
def main():
    """Unzip & extract S2ORC manuscripts to corpus set for training."""

    save = int(input("1 -- inspect the body text of a single pdf\n"
                     "2 -- Save the corpus \nSelect option 1 or 2: "))
    if save == "2":
        print("\t\n-- Initiating S2ORC PDFs extractor --\n")
        batches = 40
        for batch in range(20, batches):
            # fields = ["Physics", "Chemistry", "Engineering", "Materials Science"]
            fields = ["Chemistry"]

            # Following is the name of the csv formatted file containing each
            # manuscript's metadata, used to filter out pdfs relevant for
            # corpus. Depending on the input settings, the file might simply
            # contain its S2ORC id and field of study, however, it can also
            # include other pdf identifiers, such as acl, arxiv, pmc, pubmed,
            # mag, or doi.
            if len(fields) == 1:
                meta_filter = f"data/interim/meta/ids_batch-{fields[0]}-{batch}.csv"
            else:
                meta_filter = f"data/interim/meta/ids_batch-{batch}.csv"

            # Generates aforementioned csv file.
            metadata_to_csv(batch, fields, meta_filter)

            # Uses S2ORC-metadata containing csv file to filter pdfs one batch
            # at a time, and to store full body manuscripts in the corpus file
            # set for further training. Optionally, select segmenting ofs
            # sentences.
            save_corpus(batch, meta_filter, segment_sentences=True,
                        remove_references=True)
            print("\nPDFs Extraction, Tokenization, & Ordering -- Complete!\n"
                  "Path to corpus:\tdata/corpus/corpus"
                  "Local metadata file:\t /data/interim/meta")
    elif save == 1:
        print("\t\n-- Initiating S2ORC onePDF extractor --\n")
        # From a list of three provided S2ORC paper_ids select one to inspect
        # the form of the extracted manuscript.
        ids = ["94551546", "138410295", "54785367"]
        dois = ["10.1038/am.2015.67", "10.1039/C3TA12002C",
                "10.1103/PhysRevMaterials.2.023803"]
        index = int(input("0 -- 10.1038/am.2015.67\n"
                         "1 -- 10.1039/C3TA12002C\n"
                         "2 -- 10.1103/PhysRevMaterials.2.023803\n"
                          "\nSelect doi for inspection: \n" ))
        one_pdf(ids, dois, index=index)
        print("\nPDFs Extraction, Tokenization, & Ordering -- Complete!\n"
              "Path to corpus: \tdata/corpus/one_pdf_corpus")
    else:
        print("Select either 1 or 2!")


if __name__ == "__main__":
    main()
