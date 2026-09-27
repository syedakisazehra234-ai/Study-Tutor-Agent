from crewai import Memory


def create_memory():

    memory = Memory(
        embedder={
            "provider": "huggingface",
            "config": {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2"
            },
        }
    )

    return memory
