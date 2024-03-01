import logging
import os
from llama_hub.github_repo import GithubClient, GithubRepositoryReader
from constants import REPO_DEFAULTS
import pickle

DATA_DIR = "./data/pickled_docs"  # directory containing the documents to index

def load_pickle(filename, directory):
    """
    Load the pickled documents.

    Args:
        filename (str): The name of the pickle file.
        directory (str): The directory where the pickle file is located.

    Returns:
        The loaded pickled documents.
    """
    logger = logging.getLogger("uvicorn")
    
    with open(os.path.join(directory, filename), "rb") as f:
        logger.info(f"Loading pickled documents from {filename}")
        return pickle.load(f)


def save_pickle(obj, filename, directory):
    """
    Save the pickled documents.

    Parameters:
    obj (object): The object to be pickled.
    filename (str): The name of the file to save the pickled object.
    directory (str): The directory where the file will be saved.

    Returns:
    None
    """
    logger = logging.getLogger("uvicorn")
    
    with open(os.path.join(directory, filename), "wb") as f:
        logger.info(f"Saving pickled documents to {filename}")
        pickle.dump(obj, f)

def get_input_with_default(prompt: str, default: str) -> str:
    """
    Helper function to get user input with a default value.

    Args:
        prompt (str): The prompt message to display to the user.
        default (str): The default value to use if the user doesn't enter anything.

    Returns:
        str: The user input or the default value if no input is provided.
    """
    value = input(f"{prompt} (press enter for default): ")
    return value if value else default

def get_repo_info(defaults=False) -> dict:
    """
    Prompts the user to enter information about a GitHub repository and returns this information as a dictionary.

    Args:
        defaults (bool): Flag indicating whether to use default values for repository information.

    Returns:
        dict: A dictionary containing the repository information entered by the user.

    """
    DEFAULT_OWNER = REPO_DEFAULTS.get("owner")
    DEFAULT_REPO = REPO_DEFAULTS.get("repo")
    DEFAULT_COMMIT_SHA = REPO_DEFAULTS.get("commit_sha")
    DEFAULT_FILTER_DIRECTORIES = REPO_DEFAULTS.get("filter_directories")
    DEFAULT_FILTER_EXTENSIONS = REPO_DEFAULTS.get("filter_file_extensions")

    if defaults:
        return {
            'owner': DEFAULT_OWNER,
            'repo': DEFAULT_REPO,
            'filter_directories': DEFAULT_FILTER_DIRECTORIES,
            'filter_file_extensions': DEFAULT_FILTER_EXTENSIONS,
            'commit_sha': DEFAULT_COMMIT_SHA
        }

    print("Please enter the following information about the repository you would like to index.")
    
    owner = get_input_with_default("Owner", DEFAULT_OWNER)
    repo = get_input_with_default("Repo", DEFAULT_REPO)
    commit_sha = get_input_with_default("Commit SHA", DEFAULT_COMMIT_SHA)
    
    filter_dirs_input = get_input_with_default("Filter Directories", "")
    filter_directories = filter_dirs_input.split(",") if filter_dirs_input else DEFAULT_FILTER_DIRECTORIES

    filter_ext_input = get_input_with_default("File Extensions", "")
    filter_file_extensions = filter_ext_input.split(",") if filter_ext_input else DEFAULT_FILTER_EXTENSIONS
    
    print(f"Owner: {owner}")
    print(f"Repo: {repo}")
    print(f"Commit SHA: {commit_sha}")
    print(f"Filter Directories: {filter_directories}")
    print(f"Filter File Extensions: {filter_file_extensions}")

    return {
        'owner': owner,
        'repo': repo,
        'filter_directories': (filter_directories, GithubRepositoryReader.FilterType.INCLUDE) if filter_directories else ([], GithubRepositoryReader.FilterType.EXCLUDE),
        'filter_file_extensions': (filter_file_extensions, GithubRepositoryReader.FilterType.INCLUDE) if filter_file_extensions else ([], GithubRepositoryReader.FilterType.EXCLUDE),
        'commit_sha': commit_sha
    }


def init_github_client():
    """
    Initialize the github client.

    This function retrieves the GitHub token from the environment variable GITHUB_TOKEN
    and creates a GitHub client using the token.

    Raises:
        EnvironmentError: If the GITHUB_TOKEN environment variable is not set.

    Returns:
        GithubClient: The initialized GitHub client.
    """
    logger = logging.getLogger("uvicorn")
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("Please set the GITHUB_TOKEN environment variable.")
    
    github_client = GithubClient(github_token)
    return github_client

def pull_docs_from_github(github_client, repo, pickle_filename, pickle_docs_dir, debug=False):
    """Pull the docs from Github and save them

    Args:
        github_client (GitHubClient): The GitHub client object.
        repo (Repository): The repository object containing owner, repo, filter_directories, filter_file_extensions, and commit_sha.
        pickle_filename (str): The filename to save the pickle file.
        debug (bool, optional): Whether to enable debug mode. Defaults to False.

    Returns:
        list: The list of documents pulled from Github.
    """
    logger = logging.getLogger("uvicorn")
    
    logger.info(f"Pulling docs from Github. Repo: {repo.repo}")
    loader = GithubRepositoryReader(
        github_client,
        owner=repo.owner,
        repo=repo.repo,
        use_parser=False,
        filter_directories=repo.filter_directories,
        filter_file_extensions=repo.filter_file_extensions,
        verbose=debug,
        concurrent_requests=10,
    )
    
    print(repo)

    # Load the docs from the commit sha if requested, otherwise load from main
    # if repo.commit_sha:
    #     docs = loader.load_data(commit=repo.commit_sha)
    # else:
    docs = loader.load_data(branch="main")

    # Save the docs to a pickle file
    documents = docs
    save_pickle(documents, pickle_filename, pickle_docs_dir)

    logger.info(f"Successfully pulled {len(documents)} documents from Github.")

    return documents

def process_repo(repo, debug=False):
    """Process the repository.

    Args:
        repo (Repo): The repository object.
        debug (bool, optional): Flag indicating whether to enable debug mode. Defaults to False.

    Returns:
        tuple: A tuple containing the documents and the index storage path.
    """
    logger = logging.getLogger("uvicorn")

    # CREATE THE PICKLE DOCS DIRECTORY IF IT DOESN'T EXIST
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    github_client = init_github_client()

    # Create the filepath for the index storage
    index_storage_path = f'./storage/index_storage/{repo.owner}/{repo.repo}/'

    logger.info(f"Processing repo: {repo.owner}/{repo.repo}")
    # Create the filename for the pickled docs
    if repo.commit_sha:
        pickle_filename = f"{repo.owner}-{repo.repo}-{repo.commit_sha}-docs.pkl"
    else:
        pickle_filename = f"{repo.owner}-{repo.repo}-MAIN-docs.pkl"

    # Create the filepath for the pickled docs
    docs_filepath = os.path.join(DATA_DIR, pickle_filename)
    
    # Load the pickled docs if they exist
    # TODO: handle the case where the pickled docs exist but the index storage does not
    # TODO: handle the case where the pickled docs exist but the vector storage does not
    # TODO: handle the case where the pickled docs exist but the repo has changed....
    if os.path.exists(docs_filepath):
        logger.info(f"Path exists: {docs_filepath}")
        documents = load_pickle(pickle_filename, DATA_DIR)
        logger.info("# of Documents loaded from storage: " + str(len(documents)))
    else:
        logger.info(f"File does not exist: {docs_filepath}")
        documents = pull_docs_from_github(github_client, repo, pickle_filename, DATA_DIR, debug=debug)
        logger.info("# of Documents pulled from repo: " + str(len(documents)))

    return documents, index_storage_path