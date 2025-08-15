import json
import pickle
import numpy as np
from tqdm import tqdm

from LLM import Model


class EmbeddingsCreator:
    def __init__(self, promptsList=[]):
        self.llm = Model()
        self.promptsList = promptsList


    def createEmbeddingList(self):
        embeddingList = []
        for prompt in tqdm(self.promptsList, desc="Creating embeddings"):
            embeddingList.append(self.llm.createEmbedding(prompt))
            
        return np.array(embeddingList)


    def saveEmbeddingList(self, embeddingsList, filePath):
        with open(filePath, 'wb') as f:
            pickle.dump(embeddingsList, f)
        print(f"Embeddings saved to {filePath}")


    def loadEmbeddingList(self, filePath):
        with open(filePath, 'rb') as f:
            embeddingsList = pickle.load(f)
        return embeddingsList


if __name__ == "__main__":
    with open('records.json', 'rb') as f:
        records = json.load(f)
    promptsList = [record['prompt'] for record in records]
    print(f"Total prompts: {len(promptsList)}")
    print("Creating embeddings...")
    # Create an instance of EmbeddingsCreator with the prompts list
    embeddingsCreator = EmbeddingsCreator(promptsList=promptsList)

    embeddingsList = embeddingsCreator.createEmbeddingList()
    embeddingsCreator.saveEmbeddingList(embeddingsList, "embeddings.pkl")
    print(f"Embeddings shape: {embeddingsList.shape}")
    print("Embeddings creation completed.")