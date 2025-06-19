import pickle
import numpy as np
from tqdm import tqdm

from classes.LLM import Model


class EmbeddingsCreator:
    def __init__(self, promptsList=[]):
        self.llm = Model()
        self.promptsList = promptsList


    def createEmbeddingList(self):
        embeddingList = []
        for prompt in tqdm(self.promptsList, desc="Creating embeddings"):
            embeddingList.append(self.llm.createEmbedding(prompt))
            break

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
    with open('promptList_text.pkl', 'rb') as f:
        promptsList = pickle.load(f)
    embeddingsCreator = EmbeddingsCreator(promptsList=promptsList)
    embeddingsList = embeddingsCreator.createEmbeddingList()
    embeddingsCreator.saveEmbeddingList(embeddingsList, "embeddings.pkl")