from pathlib import Path
from huggingface_hub import hf_hub_download


# =====================================================
# Configuration
# =====================================================

REPO_ID = "eksakstri/nifty50-rag-data"
REPO_TYPE = "dataset"

LOCAL_DIR = Path("embeddings")
LOCAL_DIR.mkdir(parents=True, exist_ok=True)


FILES = [

    "corpus.faiss",

    "chunk_metadata.json",

    "company_summaries.md",

    "nifty50_snapshot.json",

    "option_chain.csv"

]


# =====================================================
# Downloader
# =====================================================

def download_assets(force=False):

    print("\nChecking required assets...\n")

    for filename in FILES:

        local_file = LOCAL_DIR / filename

        if local_file.exists() and not force:

            print(f"[✓] {filename}")

            continue

        print(f"Downloading {filename}...")

        downloaded_path = hf_hub_download(

            repo_id=REPO_ID,

            repo_type=REPO_TYPE,

            filename=filename,

            local_dir=LOCAL_DIR,

            local_dir_use_symlinks=False

        )

        print(f"Saved -> {downloaded_path}")

    print("\nAll assets are ready.\n")


# =====================================================

if __name__ == "__main__":

    download_assets()