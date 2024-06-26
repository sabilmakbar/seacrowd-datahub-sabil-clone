from pathlib import Path
from typing import List

import datasets
import pandas as pd
from datasets.download.download_manager import DownloadManager

from seacrowd.utils import schemas
from seacrowd.utils.configs import SEACrowdConfig
from seacrowd.utils.constants import Licenses, Tasks

# No paper citation found.
_CITATION = ""

_LOCAL = False
_LANGUAGES = ["tha"]
_DATASETNAME = "thai_alpaca"
_DESCRIPTION = """\
This is a Thai 🇹🇭-instructed dataset translated from cleaned version of the original
Alpaca Dataset released by Stanford using Google Cloud Translation, contain 52,000
instructions and demonstrations generated by OpenAI's text-davinci-003 engine. This
instruction data can be used to conduct instruction-tuning for language models and
make the language model follow instruction better.
"""

_HOMEPAGE = "https://huggingface.co/datasets/Thaweewat/alpaca-cleaned-52k-th"
_LICENSE = Licenses.CC_BY_NC_4_0.value
_URL = "https://huggingface.co/datasets/Thaweewat/alpaca-cleaned-52k-th/resolve/main/alpaca-cleaned-th.parquet"
_SUPPORTED_TASKS = [Tasks.INSTRUCTION_TUNING]
_SOURCE_VERSION = "1.0.0"
_SEACROWD_VERSION = "2024.06.20"


class ThaiAlpacaDataset(datasets.GeneratorBasedBuilder):
    """Thai Alpaca Dataset"""

    SOURCE_VERSION = datasets.Version(_SOURCE_VERSION)
    SEACROWD_VERSION = datasets.Version(_SEACROWD_VERSION)

    SEACROWD_SCHEMA_NAME = "t2t"

    BUILDER_CONFIGS = [
        SEACrowdConfig(
            name=f"{_DATASETNAME}_source",
            version=SOURCE_VERSION,
            description="Thai-Alpaca source schema",
            schema="source",
            subset_id=_DATASETNAME,
        ),
        SEACrowdConfig(
            name=f"{_DATASETNAME}_seacrowd_{SEACROWD_SCHEMA_NAME}",
            version=SEACROWD_VERSION,
            description="Thai-Alpaca SEACrowd schema",
            schema=f"seacrowd_{SEACROWD_SCHEMA_NAME}",
            subset_id=_DATASETNAME,
        ),
    ]

    DEFAULT_CONFIG_NAME = "thai_alpaca_source"

    def _info(self) -> datasets.DatasetInfo:
        if self.config.schema == "source":
            features = datasets.Features(
                {
                    "instruction": datasets.Value("string"),
                    "input": datasets.Value("string"),
                    "output": datasets.Value("string"),
                }
            )
        elif self.config.schema == f"seacrowd_{self.SEACROWD_SCHEMA_NAME}":
            features = schemas.text2text_features

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: DownloadManager) -> List[datasets.SplitGenerator]:
        """Returns SplitGenerators."""
        data_file = Path(dl_manager.download_and_extract(_URL))
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_file})]

    def _generate_examples(self, filepath: Path):
        """Yield examples as (key, example) tuples"""
        df = pd.read_parquet(filepath)
        for idx, row in df.iterrows():
            if self.config.schema == "source":
                example = {"instruction": row.get("instruction"), "input": row.get("input"), "output": row.get("output")}

            elif self.config.schema == f"seacrowd_{self.SEACROWD_SCHEMA_NAME}":
                inputs = row.get("input")
                if inputs:
                    text_1 = f"Context: {inputs}\n\n{row.get('instruction')}"
                else:
                    text_1 = f"Context: {row.get('instruction')}"

                example = {
                    "id": str(idx),
                    "text_1": text_1,
                    "text_2": row.get("output"),
                    "text_1_name": "input_instruction",
                    "text_2_name": "output",
                }

            yield idx, example
