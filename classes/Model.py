

from sentence_transformers import SentenceTransformer
from torch import cosine_similarity


class Model:
    def __init__(self, modelName):
        self.LLMModel = SentenceTransformer(modelName)

    
    def getQueryEmbedding(self, query):
        return self.LLMModel.encode(query)
    

    def cosinSimilarity(self, queryEmbedding, docEmbedding):
        return cosine_similarity(docEmbedding, queryEmbedding) #, dim=1)