"""
SpeechText Schema
"""
import datasets

features = datasets.Features(
    {
        "id": datasets.Value("string"),
        "path": datasets.Value("string"),
        "audio": datasets.Audio(),
        "text": datasets.Value("string"),
        "speaker_id": datasets.Value("string"),
        "metadata": {
            "speaker_age": datasets.Value("int64"),
            "speaker_gender": datasets.Value("string"),
        }
    }
)
