from langchain_huggingface import HuggingFaceEmbeddings

from config import settings


embedding_model = HuggingFaceEmbeddings(

    model_name=settings.embedding_model

)