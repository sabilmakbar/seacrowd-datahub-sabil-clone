# %%
import importlib
import pkgutil

import seacrowd.sea_datasets as dataset_collections


def import_all_dataloader_info(package, var_to_check: str):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    lang_infos = {}
    module_import_error = []
    lang_import_error = []

    for _, name, _ in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name + '.' + name
        print(f"Checking dataloader {full_name}...")
        try:
            lang_infos[name] = getattr(importlib.import_module(full_name), var_to_check)
        except ModuleNotFoundError:
            print(f"Package {full_name} can't be imported!")
            module_import_error.append(full_name)
            continue
        except AttributeError:
            print(f"Can't find '{var_to_check}' var in module {full_name}")
            lang_import_error.append(full_name)
            continue

    return lang_infos, module_import_error, lang_import_error


# %%
dataset_langs, module_import_err, lang_import_err = import_all_dataloader_info(dataset_collections, "_LANGUAGES")
dataset_tasks, module_import_err, task_import_err = import_all_dataloader_info(dataset_collections, "_SUPPORTED_TASKS")
dataset_license, module_import_err, license_import_err = import_all_dataloader_info(dataset_collections, "_LICENSE")

# %%
