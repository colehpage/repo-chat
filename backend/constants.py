# Import the LLM predictor
from llama_index import LLMPredictor

# Import the models
from langchain.chat_models import ChatOpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModeModel

# import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# Import the github repository reader
from llama_hub.github_repo import GithubRepositoryReader

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

REPO_DEFAULTS = {
    'owner': "colehpage",
    'repo': "gostow",
    'filter_directories': None,
    'filter_file_extensions': None,
    'commit_sha': None
}