# -*- coding: utf-8 -*-

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = "scaimc"
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)
TRAIN_DATA_URL = "https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Train-Corpus.xml"
TEST_DATA_URL = "https://www.scai.fraunhofer.de/content/dam/scai/de/downloads/bioinformatik/miRNA/miRNA-Test-Corpus.xml"
TRAIN_DATA_FILE_PATH = os.path.join(DATA_DIR, "miRNA-Train-Corpus.xml")
TEST_DATA_FILE_PATH = os.path.join(DATA_DIR, "miRNA-Test-Corpus.xml")
col_names = ["PubMed ID", "Pair ID", "Entity-1 term", "Entity-1 type", "Entity-1 offsets", "Entity-2 term",
             "Entity-2 type", "Entity-2 offsets", "Sentence", "Interaction", "Interaction type"]
