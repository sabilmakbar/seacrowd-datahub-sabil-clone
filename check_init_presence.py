# %%
import os
from pathlib import Path

# %%
_curr_dir = Path(__file__).parent.as_posix()

_dataset_folder_path = os.path.join(_curr_dir, "seacrowd", "sea_datasets")
# %%
for dset_file in sorted(os.listdir(_dataset_folder_path)):
    _full_path = os.path.join(_dataset_folder_path, dset_file)
    if not os.path.isdir(_full_path):
        print(f"Skipping {_full_path} as it's not a folder...")
        continue
    if "__init__.py" not in os.listdir(_full_path):
        print(f"{dset_file} doesn't have __init__.py")
        os.system(f"touch {_full_path}/__init__.py")

# %%
# from seacrowd.sea_datasets.phoatis.phoatis import _LICENSE
# %%
