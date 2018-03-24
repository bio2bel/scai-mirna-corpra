# -*- coding: utf-8 -*-

import logging
import os
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve

import pandas as pd

from .constants import TRAIN_DATA_FILE_PATH, TRAIN_DATA_URL, TEST_DATA_FILE_PATH, TEST_DATA_URL, col_names

log = logging.getLogger(__name__)


def download_scai_mirna_corpora(force_download=False):
    """Download the scai-mirna-corpora as XMLs

    :param bool force_download: If true, forces the data to get downloaded again; defaults to False
    :return: The system file path of the downloaded files
    :rtype: str
    """

    # Load training set
    log.info("Load training data")

    if os.path.exists(TRAIN_DATA_FILE_PATH) and not force_download:
        log.info('using cached data at %s', TRAIN_DATA_FILE_PATH)
    else:
        log.info('downloading %s to %s', TRAIN_DATA_URL, TRAIN_DATA_FILE_PATH)
        urlretrieve(TRAIN_DATA_URL, TRAIN_DATA_FILE_PATH)

    # Load test set
    log.info("Load test data")
    if os.path.exists(TEST_DATA_FILE_PATH) and not force_download:
        log.info('using cached data at %s', TEST_DATA_FILE_PATH)
    else:
        log.info('downloading %s to %s', TEST_DATA_URL, TEST_DATA_FILE_PATH)
        urlretrieve(TEST_DATA_URL, TEST_DATA_FILE_PATH)

    return TRAIN_DATA_FILE_PATH, TEST_DATA_FILE_PATH


def get_scai_mirna_dfs(train_url=None, test_url=None, cache=True, force_download=False):
    """Loads the pairs annotated in the training and test set

    1) PubMed ID
    2) Pair ID
    3) Entity-1 term
    4) Entity-1 type
    5) Entity-1 offset
    6) Entity-2 term
    7) Entity-2 type"
    8) Entity-2 offset
    9) Sentence
    10) Interaction
    11) Interaction type

    :param Optional[str] train_url: A custom path to use for data
    :param bool cache: If true, the data is downloaded to the file system, else it is loaded from the internet
    :param bool force_download: If true, overwrites a previously cached file
    :rtype: pandas.DataFrame
    """
    if (train_url is None or test_url is None) and cache:
        train_url, test_url = download_scai_mirna_corpora(force_download=force_download)

    # Create data frame for the training set
    training_df = create_dataframe_of_pairs(url=train_url)

    # Create data frame for the test set
    test_df = create_dataframe_of_pairs(url=test_url)

    return training_df, test_df


def create_dataframe_of_pairs(url):
    """
    Creates a pandas.DataFrame containing only the pairs annotations. A pair can either interacting or not.
    :param url: Location for retrieving dataset
    :rtype: pandas.DataFrame

    1) PubMed ID
    2) Pair ID
    3) Entity-1 term
    4) Entity-1 type
    5) Entity-1 offset
    6) Entity-2 term
    7) Entity-2 type"
    8) Entity-2 offset
    9) Sentence
    10) Interaction
    11) Interaction type
    """

    df = pd.DataFrame(columns=col_names)
    tree = ET.parse(url)
    root = tree.getroot()

    for doc in root.iter('document'):
        pubMed_id = doc.get('origId')
        for sentence_anno in doc.iter('sentence'):
            if sentence_anno.find('pair') == None:
                continue

            entity_annotation_dict = get_entity_anno_dict(sentence_anno=sentence_anno)

            for pair in sentence_anno.iter('pair'):
                e1_id = pair.get('e1')
                e2_id = pair.get('e2')

                e1 = entity_annotation_dict[e1_id]
                e2 = entity_annotation_dict[e2_id]

                e1_text = e1.get('text')
                e2_text = e2.get('text')

                e1_type = e1.get('type')
                e2_type = e2.get('type')

                e1_offsets = e1.get('charOffset').split('-')
                e2_offsets = e2.get('charOffset').split('-')

                sentence_text = sentence_anno.get('text')

                pair_id = pair.get('id')
                interaction = pair.get('interaction')
                interaction_type = pair.get('type')

                new_row = [pubMed_id, pair_id, e1_text, e1_type, e1_offsets, e2_text, e2_type, e2_offsets,
                           sentence_text, interaction, interaction_type]
                df.append(new_row)
    return df


def get_entity_anno_dict(sentence_anno):
    """
    For each sentence annotation all annotated entities are extracted and saved in a dictionary.
    :param sentence_anno: An sentence annotation
    :rtype: dict
    """
    entity_dict = dict()

    for entity in sentence_anno.iter('entity'):
        entity_id = entity.get('id')
        entity_dict[entity_id] = entity

    return entity_dict
