import os
import config
class DataPreprocessor:
    def __init__(self):
        self.raw_dir = config.BASE_OUTPUT_DIR
        self.output_file = config.TRAIN_FILE
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def clean_and_merge(self):
        print(f"Processing data from {self.raw_dir}...")
        file_count = 0
        
        with open(self.output_file, "w", encoding="utf-8") as outfile:
            for root, _, files in os.walk(self.raw_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in config.FILE_EXTENSIONS):
                        file_path = os.path.join(root, file)
                        self._append_file_content(file_path, outfile)
                        file_count += 1
        
        print(f"Preprocessing complete. {file_count} files merged into {self.output_file}")

    def _append_file_content(self, file_path, outfile):
        try:
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
            ext = os.path.splitext(file_path)[1]
            header = f"\n\n### FILE: {os.path.basename(file_path)} ({ext}) ###\n"
            
            outfile.write(header)
            outfile.write(content)
            outfile.write("\n<|endoftext|>\n")
            
        except Exception as e:
            print(f"Skipping {file_path}: {e}")