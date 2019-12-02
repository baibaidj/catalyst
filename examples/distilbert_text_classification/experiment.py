from pathlib import Path
import pandas as pd
from typing import Dict
from collections import OrderedDict
from catalyst.data.nlp.classify import TextClassificationDataset
from catalyst.dl import ConfigExperiment


class Experiment(ConfigExperiment):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.config = config

    def get_transforms(self, stage: str = None, mode: str = None):
        return []

    # noinspection PyMethodOverriding
    def get_datasets(
        self, stage: str, path_to_data, train_filename, validation_filename,
        max_sequence_length, **kwargs
    ):
        datasets = OrderedDict()

        path_to_data = Path(path_to_data)

        train_df = pd.read_csv(path_to_data / train_filename)
        valid_df = pd.read_csv(path_to_data / validation_filename)

        train_dataset = TextClassificationDataset(
            texts=train_df['text'],
            labels=train_df['label'],
            label_dict=None,
            max_seq_length=max_sequence_length
        )

        valid_dataset = TextClassificationDataset(
            texts=valid_df['text'],
            labels=valid_df['label'],
            label_dict=train_dataset.label_dict,
            max_seq_length=max_sequence_length
        )

        datasets["train"] = train_dataset
        datasets["valid"] = valid_dataset

        return datasets
