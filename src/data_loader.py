import os
import requests
from github import Github
from dotenv import load_dotenv
import config

class DatasetScraper:
    def __init__(self):
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not found in environment variables.")
        
        self.g = Github(token)
        print("GitHub client initialized.")

    def save_file(self, repo_name, file_path, content, framework):
        full_path = os.path.join(config.BASE_OUTPUT_DIR, framework, repo_name, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"[Error] Write failed for {full_path}: {e}")

    def download_repo_contents(self, repo, framework):
        print(f"Processing repo: {repo.full_name}")
        count = 0
        try:
            contents = repo.get_contents("")
            queue = []
            if isinstance(contents, list):
                queue.extend(contents)
            else:
                queue.append(contents)

            while queue and count < config.MAX_FILES_PER_REPO:
                file_content = queue.pop(0)
                
                if file_content.type == "dir":
                    try:
                        queue.extend(repo.get_contents(file_content.path))
                    except:
                        pass
                
                elif file_content.type == "file":
                    if any(file_content.name.endswith(ext) for ext in config.FILE_EXTENSIONS):
                        self._process_single_file(repo, file_content, framework)
                        count += 1

        except Exception as e:
            print(f"[Error] Accessing {repo.full_name}: {e}")

    def _process_single_file(self, repo, file_content, framework):
        content = None
        try:
            if file_content.size < config.MAX_FILE_SIZE_BYTES:
                content = file_content.decoded_content.decode('utf-8')
            else:
                print(f"Skipping large file: {file_content.path}")
                return
        except:
            if file_content.download_url:
                resp = requests.get(file_content.download_url)
                if resp.status_code == 200:
                    content = resp.text

        if content:
            self.save_file(repo.full_name, file_content.path, content, framework)

    def run(self):
        for framework, query in config.SEARCH_QUERIES.items():
            print(f"\n--- Searching: {framework} ---")
            framework_dir = framework.lower()
            
            try:
                repos = self.g.search_repositories(query=query, sort="stars", order="desc")
                for i, repo in enumerate(repos):
                    if i >= config.MAX_REPOS_PER_FRAMEWORK:
                        break
                    self.download_repo_contents(repo, framework_dir)
            except Exception as e:
                print(f"[Error] Search failed for {framework}: {e}")