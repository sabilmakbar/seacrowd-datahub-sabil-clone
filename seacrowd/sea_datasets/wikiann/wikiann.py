from pathlib import Path
from typing import List

import datasets
from datasets import NamedSplit

from seacrowd.utils import schemas
from seacrowd.utils.configs import SEACrowdConfig
from seacrowd.utils.constants import Tasks, Licenses

_DATASETNAME = "wikiann"

_LANGUAGES = ["ind", "jav", "min", "sun", "ace", "zlm", "map-bms", "mya", "tgl", "tha", "vie", "khm"]
_LOCAL = False
_CITATION = """\
@inproceedings{pan-etal-2017-cross,
    title = "Cross-lingual Name Tagging and Linking for 282 Languages",
    author = "Pan, Xiaoman  and
      Zhang, Boliang  and
      May, Jonathan  and
      Nothman, Joel  and
      Knight, Kevin  and
      Ji, Heng",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1178",
    doi = "10.18653/v1/P17-1178",
    pages = "1946--1958",
    abstract = "The ambitious goal of this work is to develop a cross-lingual name tagging and linking framework
    for 282 languages that exist in Wikipedia. Given a document in any of these languages, our framework is able
    to identify name mentions, assign a coarse-grained or fine-grained type to each mention, and link it to
    an English Knowledge Base (KB) if it is linkable. We achieve this goal by performing a series of
    new KB mining methods: generating {``}silver-standard{''} annotations by
    transferring annotations from English to other languages through cross-lingual links and KB properties,
    refining annotations through self-training and topic selection,
    deriving language-specific morphology features from anchor links, and mining word translation pairs from
    cross-lingual links. Both name tagging and linking results for 282 languages are promising
    on Wikipedia data and on-Wikipedia data.",
}
@inproceedings{rahimi-etal-2019-massively,
    title = "Massively Multilingual Transfer for {NER}",
    author = "Rahimi, Afshin  and
      Li, Yuan  and
      Cohn, Trevor",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1015",
    pages = "151--164",
}
"""

_DESCRIPTION = """\
The wikiann dataset contains NER tags with labels from O (0), B-PER (1), I-PER (2), B-ORG (3), I-ORG (4), B-LOC (5), I-LOC (6). The Indonesian subset is used.
WikiANN (sometimes called PAN-X) is a multilingual named entity recognition dataset consisting of Wikipedia articles
 annotated with LOC (location), PER (person), and ORG (organisation)
 tags in the IOB2 format. This version corresponds to the balanced train, dev, and test splits of
  Rahimi et al. (2019), and uses the following subsets from the original WikiANN corpus

Language	WikiAnn	ISO 639-3
Indonesian	id	ind
Javanese	jv	jav
Minangkabau	min	min
Sundanese	su	sun
Acehnese	ace	ace
Malay	ms	zlm
Banyumasan	map-bms	map-bms
Myanmar my mya
Tagalog tl tgl
Thailand th tha
Vietnam vi vie
Khmer km khm


"""

_HOMEPAGE = "https://github.com/afshinrahimi/mmner"

_LICENSE = Licenses.APACHE_2_0.value

_URL = "https://s3.amazonaws.com/datasets.huggingface.co/wikiann/1.1.0/panx_dataset.zip"

_SUPPORTED_TASKS = [Tasks.NAMED_ENTITY_RECOGNITION]

_SOURCE_VERSION = "1.1.0"
_SEACROWD_VERSION = "2024.06.20"


def seacrowd_config_constructor(lang, schema, version):
    if lang == "":
        raise ValueError(f"Invalid lang {lang}")

    if schema != "source" and schema != "seacrowd_seq_label":
        raise ValueError(f"Invalid schema: {schema}")

    return SEACrowdConfig(
        name="wikiann_{lang}_{schema}".format(lang=lang, schema=schema),
        version=datasets.Version(version),
        description="wikiann with {schema} schema for {lang} language".format(lang=lang, schema=schema),
        schema=schema,
        subset_id="wikiann",
    )


LANGUAGES_MAP = {"ind": "indonesian", "jav": "javanese", "min": "minangkabau", "sun": "sundanese", "ace": "acehnese", "zlm": "malay", "map_bms": "banyumasan", "mya": "myanmar", "tgl": "tagalog", "tha": "thailand", "vie": "vietnam", "khm": "khmer"}
LANG_CODES = {"ind": "id", "jav": "jv", "min": "min", "sun": "su", "ace": "ace", "zlm": "ms", "map_bms": "map-bms", "mya": "my", "tgl": "tl", "tha": "th","vie": "vi","khm": "km"}


class WikiAnnDataset(datasets.GeneratorBasedBuilder):
    """wikiann is an NER tagging dataset consisting of Wikipedia articles annotated with LOC, PER, and ORG tags
    for multiple Indonesian language. If the language is not specified, it loads the Indonesian subset."""

    label_classes = ["B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "O"]

    BUILDER_CONFIGS = [seacrowd_config_constructor(lang, "source", _SOURCE_VERSION) for lang in LANGUAGES_MAP] + [seacrowd_config_constructor(lang, "seacrowd_seq_label", _SEACROWD_VERSION) for lang in LANGUAGES_MAP]

    DEFAULT_CONFIG_NAME = "wikiann_ind_source"

    def _info(self):
        if self.config.schema == "source":
            features = datasets.Features({"index": datasets.Value("string"), "tokens": [datasets.Value("string")], "ner_tag": [datasets.Value("string")]})
        elif self.config.schema == "seacrowd_seq_label":
            features = schemas.seq_label_features(self.label_classes)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def get_lang(self, name):
        return name.removesuffix("_source").removesuffix("_seacrowd_seq_label").removeprefix("wikiann_")

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        path = Path(dl_manager.download_and_extract(_URL))
        lang = LANG_CODES[self.get_lang(self.config.name)]
        wikiann_dl_dir = path / f"{lang}.tar.gz"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"split": "dev", "filepath": dl_manager.iter_archive(wikiann_dl_dir)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"split": "test", "filepath": dl_manager.iter_archive(wikiann_dl_dir)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split": "train", "filepath": dl_manager.iter_archive(wikiann_dl_dir)},
            ),
            datasets.SplitGenerator(
                name=NamedSplit("extra"),
                gen_kwargs={"split": "extra", "filepath": dl_manager.iter_archive(wikiann_dl_dir)},
            ),
        ]

    def _generate_examples(self, filepath: Path, split):
        """Based on https://github.com/huggingface/datasets/blob/main/datasets/wikiann/wikiann.py"""
        fps = filepath
        tokens = []
        ner_tags = []
        langs = []
        guid_index = 0
        for k, file in fps:
            if k == split:
                for line in file:
                    line = line.decode("utf-8")
                    if line == "" or line == "\n":
                        if tokens:
                            if self.config.schema == "source":
                                yield guid_index, {"index": str(guid_index), "tokens": tokens, "ner_tag": ner_tags}
                            elif self.config.schema == "seacrowd_seq_label":
                                yield guid_index, {"id": str(guid_index), "tokens": tokens, "labels": ner_tags}
                            else:
                                raise ValueError(f"Invalid config: {self.config.name}")
                            guid_index += 1
                            tokens = []
                            ner_tags = []
                            langs = []
                    else:
                        # wikiann data is tab separated
                        splits = line.split("\t")
                        # strip out en: prefix
                        langs.append(splits[0].split(":")[0])
                        tokens.append(":".join(splits[0].split(":")[1:]))
                        if len(splits) > 1:
                            ner_tags.append(splits[-1].replace("\n", ""))
                        else:
                            # examples have no label in test set
                            ner_tags.append("O")
