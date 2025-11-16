from sentence_transformers import SentenceTransformer


class Model:
    def __init__(self):
        model_path = "stella_en_1.5B_v5"
        self.embeddingModel = SentenceTransformer(model_path)


    def createEmbedding(self, prompt):
        return self.embeddingModel.encode(prompt)


if __name__ == "__main__":
    print("Running from LLM.py File...")
    llm = Model()
    prompt = "Hello World!"
    promptEmbedding = llm.createEmbedding(prompt)
    print("Prompt:", prompt)
    print("Prompt Embedding Type:", type(promptEmbedding))
    print("Prompt Embedding:", promptEmbedding)
