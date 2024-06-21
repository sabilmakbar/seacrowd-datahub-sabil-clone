# %%
from datasets import load_dataset

import datasets

datasets.logging.set_verbosity(datasets.logging.INFO)
from seacrowd.sea_datasets.tha_lotus.tha_lotus import ThaiLOTUS as DSetClasstoTest
# from seacrowd.sea_datasets.bloom_speech.bloom_speech import BloomSpeechDataset as DSetClasstoTest

dset_class = DSetClasstoTest(config_name="tha_lotus_unidrection_clean_source")
# dset_class = DSetClasstoTest()

print(f"All schema: {list(dset_class.builder_configs.keys())}")

# %%
parent_dir = "seacrowd/sea_datasets"
dset_name = "tha_lotus"
path_name = f"{parent_dir}/{dset_name}/{dset_name}.py"

# cfg_list = [cfg for cfg in dset_class.builder_configs.keys() if "seacrowd" in cfg]

# dset = load_dataset(path_name, name = cfg_list[0])

# print(f"Max len of label: {max([val for _, val in label_info])}")
# import re
# lang_to_skip = ["ind", "tha", "msa", "vie"]
for config_name in dset_class.builder_configs.keys():
    print(f"Using config name of: '{config_name}'")
    if "source" in config_name:
        dset = load_dataset(path_name, name = config_name) #, download_mode="force_redownload")
    #     pass
    else:
        dset = load_dataset(path_name, name = config_name)

# %%
# train_dset = load_dataset("/Users/salsabil.akbar/Documents/seacrowd-datahub-sabil-clone/seacrowd/sea_datasets/indowiki/indowiki.py", split="train")
# train_lab = set(train_dset["relation"])

# val_dset = load_dataset("/Users/salsabil.akbar/Documents/seacrowd-datahub-sabil-clone/seacrowd/sea_datasets/indowiki/indowiki.py", split="train")
# val_lab = set(val_dset["relation"])

# test_dset = load_dataset("/Users/salsabil.akbar/Documents/seacrowd-datahub-sabil-clone/seacrowd/sea_datasets/indowiki/indowiki.py", split="train")
# test_lab = set(test_dset["relation"])
# # %%

# print(len(train_lab.difference(val_lab)))
# print(len(train_lab.difference(test_lab)))

# print(len(val_lab.difference(train_lab)))
# print(len(val_lab.difference(test_lab)))

# print(len(test_lab.difference(train_lab)))
# print(len(test_lab.difference(val_lab)))

# len(train_lab)
# # %%
