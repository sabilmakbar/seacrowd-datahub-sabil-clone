# %%
import os

# %%
path_dir = "/Users/salsabil.akbar/.cache/huggingface/datasets/downloads"
for path in os.listdir(path_dir):
    size = os.stat(os.path.join(path_dir, path)).st_size
    if size > 0:
        print(f"This path {path} has size of {size}")

# %%