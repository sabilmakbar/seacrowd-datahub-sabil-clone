# %%

# %%
import json
from itertools import product

import datasets
from datasets import load_dataset

def unit_tests_seawiki_load_dset(dset: datasets.Dataset | datasets.DatasetDict):
  if isinstance(dset, datasets.DatasetDict):
    if len(dset.keys()) != 1:
      raise AssertionError("Unexpected #keys!")
    if list(dset.keys()) != ["train"]:
      raise AssertionError("Unexpected keys name!")
  
    dset = dset["train"]

  if dset.num_rows <= 0:
    raise AssertionError("The number of datasets isn't expected!")

if __name__ == "__main__":
  default_config_templates = ["sea_wiki_source", "sea_wiki_seacrowd", "sea_wiki_source_ssp", "sea_wiki_source_t2t", "sea_wiki_seacrowd_ssp", "sea_wiki_seacrowd_t2t"]
  for default_config in default_config_templates:
    print(f"Running `load_dataset` for default config {default_config}")
    dset = load_dataset(
      "/Users/salsabil.akbar/Documents/seacrowd-datahub-sabil-clone/seacrowd/sea_datasets/sea_wiki/sea_wiki.py",
      default_config
    )
    unit_tests_seawiki_load_dset(dset)

  with open("seacrowd/sea_datasets/sea_wiki/lang_config.json", "r") as f:
    langs = list(json.load(f).keys())

  config_templates = ["sea_wiki_source_{lang}_ssp", "sea_wiki_source_{lang}_t2t", "sea_wiki_seacrowd_{lang}_ssp", "sea_wiki_seacrowd_{lang}_t2t"]

  for _config, lang in product(config_templates, langs):
    config = _config.format(lang=lang)
    print(f"Running `load_dataset` for config {config} and lang {lang}")
    load_dataset(
      "/Users/salsabil.akbar/Documents/seacrowd-datahub-sabil-clone/seacrowd/sea_datasets/sea_wiki/sea_wiki.py",
      config
    )
    unit_tests_seawiki_load_dset(dset)
