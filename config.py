import os
BASE_OUTPUT_DIR = "dataset/raw"
PROCESSED_DATA_DIR = "dataset/processed"
TRAIN_FILE = os.path.join(PROCESSED_DATA_DIR, "train_dataset.txt")
MODEL_OUTPUT_DIR = "models/wanz-flash"
SEARCH_QUERIES = {
    "nextjs": "nextjs component language:TypeScript stars:>1000",
    "react": "react component language:TypeScript stars:>1000"
}
FILE_EXTENSIONS = [".tsx", ".ts", ".js", ".jsx", ".css"]
MAX_REPOS_PER_FRAMEWORK = 5
MAX_FILES_PER_REPO = 30
MAX_FILE_SIZE_BYTES = 500_000
BASE_MODEL_NAME = "distilgpt2" 
BATCH_SIZE = 4
NUM_EPOCHS = 3
LEARNING_RATE = 2e-5
BLOCK_SIZE = 1000 