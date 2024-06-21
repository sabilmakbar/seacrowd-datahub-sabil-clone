# Datasheet Reviewer SOP

Generally, the objective of datasheet review is to ensure that:

### 1. The dataset is available and accessible.
FAQs:
1. Can the dataset be free-upon-request?
    * Yes. For example, we can approve datasets that are hosted on hubs such as HuggingFace, but are gated by required acknowledgements to terms and conditions. The dataset must indicate that it is free-upon-request.

### 2. There must be no duplicate datasheets.
FAQs:
1. What if a contributor submitted a new datasheet for `X` but a datasheet for `X` is already approved?
    * *Is the new datasheet more complete and better than the existing datasheet?*  
      **Yes** → Proceed with the normal review process, change the existing datasheet’s status to “Deprecated”.  
      **No** → Reject.

2. What if more than one contributor submitted new datasheets of the same dataset, and all of them have not yet been approved? (After 23 Nov)
    * Pick one that is relatively better than the others, fix the incorrect/inconsistent parts, then “Approve”.

3. What if more than one contributor submitted new datasheets of the same dataset, and all of them have not yet been approved (Before 23 Nov)
    * Pick one that is more complete than the others, fix any incorrect/inconsistent parts, then “Approve”.
    * For the others, use “sharing points” status.
    * Split the obtained points of the datasheet between the contributors. It doesn’t have to be an equal split. The contributor who gives more complete information can receive higher points.
        * For example, for a datasheet worth 6 points, the assignment could be: contributor 1 gets 3 points, contributor 2 gets 2 points, contributor 3 gets 1 point.
        * We may simplify this by accepting only a subset of identical submissions that have the most complete information and set a ratio split of points (e.g., 7:3).

### 3. The information provided in the datasheet is correct, the information aligns with the dataset, and the dataset is relevant to SEA.
FAQs:
1. What should I do if the datasheet has incorrect or missing information?
    * There are multiple ways to correct this:
        * Ask the contributor to fix it (with some guidance) using the edit link (column AU in the approval sheet).
        * Reviewer uses the edit link (column AU) to fix it themselves.
        * **[NOT RECOMMENDED]** Reviewer uses a hidden sheet (_raw) to directly edit in the cells. This is only recommended when a large number of data per subset of the total dataset must be edited.

2. What should I check and how should I proceed?
    * See the checklist below.

## Approval Checklist
Check the following before approving:
1. Data availability (is it free and open-source or is it private?)
2. Dataset splits (if train, validation, or test are available)
3. Dataset size (in lines, disk size, or any provided metric)
4. Dataset license
5. Task type (whether the data can be represented as the mentioned task)
6. Paper (whether it directs to the correct publication. Archival version has higher priority)
7. Languages (list of all languages it supports)

## What to do next?
1. Change the status to **Rejected**, **Approved**, or **Sharing Points**.
2. Add notes and obtained points (in column BB in the approval sheet)
3. Check the scoring guide and see which languages gets additional points (if any).
4. Add the dataloader name (use Python snake case)
5. Wait for a GitHub issue to be generated for the approved datasheet.


# Dataloader Reviewer SOP

The objective of datasheet review is to ensure that all dataloaders in SEACrowd conform to the HF Dataloader Structure and SEACrowd-defined schema and config and follow a similar code format and/or style.

### Dataloader Check
1. Metadata correctness. (ensure Tasks, Languages, HOME_URL, DATA_URL is used). Make sure the dataloader also has `__init__.py`.
2. All subsets are implemented correctly to respective dataloader issue and according to SEACrowd Schema definition (has both `source` and `seacrowd` schema -- if a given task has its SEACrowd Schema, else can raise it to reviewers/mods).
3. Pass the test scripts defined in `tests` folder.
4. Pass manual check.
   a. Perform a sampling of configs based on Lang and/or Task combinations
   b. Execute `datasets.load_dataset` check based on config list (a)
   c. Check on the dataset schema & few first examples for plausibility.
5. Follows some general rules/conventions:
    a. Use `PascalCase` for the dataloader class name (optional: "Dataset" can be appended to the Dataloader class name; see `templates/template.py` for example).
    b. Use lowercase word characters (regex identifier: `\w`) for schema column names, including the `source` schema if the original dataset doesn't follow it.
6. The code aligns with the `black` formatter. Hint:
use this `make check_file=seacrowd/sea_datasets/{dataloader}/{dataloader}.py`
7. Follows Dataloader Config Rules (will be described in the following)

### Dataloader Config Rules
Based on the compulsory Dataloader Configs listed on Datasheet Issue, the dataset are divided into 4 different types:
1. Single Subset, Single Task (Type 1)
2. Multiple Subsets, Single Task (Type 2)
3. Single Subset, Multiple Task (Type 3)
4. Multiple Subsets, Multiple Task (Type 4)

    **Note for Multilingual Dataset:**
   
    For a multilingual dataset, generally, it falls under multiple subsets type (since one language is considered as a standalone subset of the dataloder) unless it's influencing the label heavily or it doesn't make sense to split the data based on the languages (for instance, in the case of Lang Identification or Linguistic Features/Unit Identification).

Based on aforementioned types, the checklist for Config Correctness is as follows:
1. For type 1 & 3, both config of `f”{_DATASETNAME}_source”` and `f”{_DATASETNAME}_seacrowd_{TASK_TO_SCHEMA}”` must be implemented.
2. For type 2 and 4, the dataloader config in (1) generally shouldn't be implemented (case-by-case checking can be done if needed). Consequently, it must cover all listed subsets in Dataloader Issue.
3. The formatting for config names that have multiple subsets are
    1. `f”{_DATASETNAME}_{subset_name}_source”` 
    2. `f”{_DATASETNAME}_{subset_name}_seacrowd_{TASK_TO_SCHEMA}”`

      **If the subset name contains language info, the lang identifier should be in a `ISO_639_3` lang code.**
3. For point (2), since it won't pass the test-cases using the default args, a custom arg must be provided by the Dataloader PR creator (or Dataloader Issue Assignee) to ensure the reproducibility of Testing among reviewers. The reviewers can add the testing args if necessary.

## Approval and Dataloader Reviewer Assignment Process 
1. Every dataloader requires 2 reviewers per issue (the assignee must not review their own dataloader).
2. Once the second reviewer is approved, the PR can be merged to the `master` branch using the `squash and merge` strategy for a cleaner commit history.
3. For the Reviewers' Assignment, there are two possible ways:
   1. @holylovenia will assign and monitor reviewers once a week to maintain and balance the load and overall pace. It will prioritize dataloaders used for experiments, then on reverse chronological order based on PR created time.
   2. Any reviewers can take any unassigned PR as long as the review can be done promptly.
