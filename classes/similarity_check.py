from classes.LLM import Model
import torch
import pickle

class SimilarityCheck:
    def __init__(self):
        self.llm = Model()

        embeddingsFilePath = "embeddings.pkl"
        promptListFilePath = "promptList.pkl"
        embeddingsArr = self.loadPickleFile(embeddingsFilePath)
        self.promptList = self.loadPickleFile(promptListFilePath)
        self.embeddingsVector = torch.tensor(embeddingsArr)


    def loadPickleFile(self, filePath):
        with open(filePath, 'rb') as f:
            embeddingsList = pickle.load(f)
        return embeddingsList 


    def getCosineSimilarity(self, query):
        queryEmbedding = self.llm.createEmbedding(query)
        queryVector = torch.tensor(queryEmbedding).unsqueeze(0)

        cosineSimilarity = torch.nn.functional.cosine_similarity(
            self.embeddingsVector, queryVector, dim=1
        )
        return cosineSimilarity
    

    def checkSimilarity(self, query):
        cosineSimilarity = self.getCosineSimilarity(query)
        values, indices = cosineSimilarity.topk(5)
        topPrompts = [self.promptList[idx] for idx in indices]
        return topPrompts


if __name__ == "__main__":
    similarityCheck = SimilarityCheck()
    query = "Shop Drawing for Site Grading plan"
    similarityScores = similarityCheck.getCosineSimilarity(query)
    print("Cosine Similarity Scores:", similarityScores)
    print("Top 5 Similarity Scores:", similarityScores.topk(5).values)
    print("Top 5 Indices:", similarityScores.topk(5).indices)
    print("Top 5 Similarity Scores Prompts")
    print(similarityCheck.checkSimilarity(query))