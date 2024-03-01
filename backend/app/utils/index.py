import logging
import os
from types import SimpleNamespace
import chromadb

from llama_index import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    ServiceContext,
    GPTVectorStoreIndex,
)

from llama_index.storage.index_store import SimpleIndexStore
from llama_index.llms import OpenAI
from llama_index.vector_stores import ChromaVectorStore

# Import the LLM predictor
from llama_index import LLMPredictor

# Import the models
from langchain.chat_models import ChatOpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModeModel

# import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# Import the github repository reader
from llama_hub.github_repo import GithubRepositoryReader

from app.utils.repo import process_repo

# DEFINE THE MODEL AND PARAMETERS
# MODEL_NAME = "gpt-4"
MODEL_NAME = "gpt-3.5-turbo"
CHUNK_SIZE_LIMIT = 512
CHUNK_OVERLAP = 200  # default
MAX_TOKENS = None  # Set to None to use model's maximum

# TODO: investigate modes and models for this purpose
# MODES: SIMILARITY_MODE or TEXT_SEARCH_MODE
# MODELS: DAVINCI or CURIE or BABBAGE or ADA or TEXT_EMBED_ADA_002
# EMBED_MODEL = OpenAIEmbedding(mode=OpenAIEmbeddingMode.SIMILARITY_MODE, model=OpenAIEmbeddingModeModel.TEXT_EMBED_ADA_002)

# USE HUGGINGFACE EMBEDDINGS FOR NOW INSTEAD OF OPENAI ABOVE
EMBED_MODEL = HuggingFaceEmbeddings()

LLM_PREDICTOR = LLMPredictor(
    # TODO: COSTS BUT BETTER, SWAP LATER MOST LIKELY
    llm=ChatOpenAI(
        temperature=0.5,
        model_name=MODEL_NAME,
        max_tokens=MAX_TOKENS
    )
)

CHROMADB_DIR = "./storage/vector_storage/chromadb/" # directory to cache the generated index

REPO_DEFAULTS = {
    'owner': "colehpage",
    'repo': "hyperdx",
    'filter_directories': None,
    'filter_file_extensions': None,
    'commit_sha': None
}

# service_context = ServiceContext.from_defaults(
#     llm=OpenAI(model="gpt-3.5-turbo")
# )

def initialize_service_context(llm_predictor, embed_model, chunk_size_limit, chunk_overlap):
    """
    Initializes the service context with the given parameters.

    Args:
        llm_predictor: The language model predictor.
        embed_model: The embedding model.
        chunk_size_limit: The limit of chunk size.
        chunk_overlap: The overlap between chunks.

    Returns:
        The initialized service context.
    """
    # return ServiceContext.from_defaults(
    #     llm_predictor=llm_predictor,
    #     embed_model=embed_model,
    #     # node_parser=SentenceSplitter(
    #     #     separator=" ",
    #     #     chunk_size=chunk_size_limit,
    #     #     chunk_overlap=chunk_overlap,
    #     # ),
    # )
    return ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo")
    )
    
    
def initialize_storage_context(chroma_collection, index_storage_path):
    """
    Create an index using the given documents, service context, storage context, repository information, and index storage path.

    Parameters:
        documents (list): A list of documents to be indexed.
        service_context (ServiceContext): The service context object.
        storage_context (StorageContext): The storage context object.
        repo (Repo): The repository object containing the repo info.
        index_storage_path (str): The path to the index storage.

    Returns:
        GPTVectorStoreIndex: The created index.
    """
    logger = logging.getLogger("uvicorn")
    
    if os.path.exists(index_storage_path):
        logger.info("Retrieving the vector store context")
        storage_context = StorageContext.from_defaults(
            vector_store=ChromaVectorStore(chroma_collection=chroma_collection),
            index_store=SimpleIndexStore.from_persist_dir(persist_dir=index_storage_path),
        )
        return storage_context, True
    else:
        logger.info("Creating the vector store context")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return storage_context, False
    
def create_index(documents, service_context, storage_context, repo, index_storage_path):
    """
    Create an index using the given documents, service context, storage context, repository information, and index storage path.

    Parameters:
        documents (list): A list of documents to be indexed.
        service_context (ServiceContext): The service context object.
        storage_context (StorageContext): The storage context object.
        repo (Repo): The repository object containing the repo info.
        index_storage_path (str): The path to the index storage.

    Returns:
        GPTVectorStoreIndex: The created index.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Creating the vector store index")
    index = GPTVectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=service_context,
    )
    index.set_index_id(f'{repo.owner}_{repo.repo}')
    index.storage_context.persist(index_storage_path)
    return index

def load_index(service_context, storage_context):
    """
    Loads the index from storage.

    Args:
        service_context: The service context.
        storage_context: The storage context.

    Returns:
        The loaded index.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Retrieving the vector store index")
    index = load_index_from_storage(
        service_context=service_context, 
        storage_context=storage_context
    )
    return index

def process_repository(repo_info):
    """
    Process a repository by performing various operations.

    Args:
        repo_info (dict): Information about the repository.

    Returns:
        tuple: A tuple containing the repository object, the processed documents, and the index storage path.
    """
    repo = SimpleNamespace(**repo_info)
    documents, index_storage_path = process_repo(repo)
    return repo, documents, index_storage_path
    
def get_index():    
    logger = logging.getLogger("uvicorn")
    repo_info = REPO_DEFAULTS

    # Process the repo
    logger.info("Processing the repository")
    repo, documents, index_storage_path = process_repository(repo_info)
        
    chroma_client = chromadb.PersistentClient(path=CHROMADB_DIR)
    chroma_collection = chroma_client.get_or_create_collection(f'{repo.owner}_{repo.repo}')
    
    # Initialize service context
    logger.info("Initializing the service context")
    service_context = initialize_service_context(LLM_PREDICTOR, EMBED_MODEL, CHUNK_SIZE_LIMIT, CHUNK_OVERLAP)
    
    # Initialize storage context
    logger.info("Initializing the storage context")
    storage_context, index_exists = initialize_storage_context(chroma_collection, index_storage_path)
    
    # Create or load the index
    if index_exists:
        logger.info(f"Loading index from {index_storage_path}...")
        index = load_index(service_context=service_context, storage_context=storage_context)
        logger.info(f"Finished loading index from {index_storage_path}")
    else:
        index = create_index(documents=documents, service_context=service_context, storage_context=storage_context, repo=repo, index_storage_path=index_storage_path)
        logger.info(f"Finished creating new index. Stored in {index_storage_path}")
    
    # # check if storage already exists
    # if not os.path.exists(STORAGE_DIR):
    #     logger.info("Creating new index")
    #     # load the documents and create the index
    #     documents = SimpleDirectoryReader(DATA_DIR).load_data()
    #     index = VectorStoreIndex.from_documents(documents,service_context=service_context)
    #     # store it for later
    #     index.storage_context.persist(STORAGE_DIR)
    #     logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")
    # else:
    #     # load the existing index
    #     logger.info(f"Loading index from {STORAGE_DIR}...")
    #     storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    #     index = load_index_from_storage(storage_context,service_context=service_context)
    #     logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index
