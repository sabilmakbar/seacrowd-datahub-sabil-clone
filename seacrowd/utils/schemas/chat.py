"""
Conversational Chat Schema
"""
import datasets

features = datasets.Features(
    {
        "id": datasets.Value("string"),
        "input": datasets.Sequence({
            "role": datasets.Value("string"),
            "content": datasets.Value("string"),
        }),
        "output": datasets.Value("string"),

        # the schema of 'meta' aren't specified either to allow some flexibility
        "meta": {}

        # notes on how to use this field of 'meta'
        # you can choose two of options:
        # 1. defining as empty dict if you don't think it's usable in `_generate_examples`, or
        # 2. defining meta as dict of key with intended colname meta and its val with dataset.Features class
        #    in `_info` Dataloader method then populate it with the values in `_general_examples` Dataloader method
    }
)
