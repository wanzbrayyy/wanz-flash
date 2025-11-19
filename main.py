import sys
from src.data_loader import DatasetScraper
from src.preprocessor import DataPreprocessor
from src.trainer import ModelTrainer
from src.inference import CodeGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [scrape|process|train|test]")
        return

    command = sys.argv[1]

    if command == "scrape":
        print("--- Step 1: Scraping GitHub ---")
        scraper = DatasetScraper()
        scraper.run()

    elif command == "process":
        print("--- Step 2: Preprocessing Data ---")
        processor = DataPreprocessor()
        processor.clean_and_merge()

    elif command == "train":
        print("--- Step 3: Training Model ---")
        trainer = ModelTrainer()
        trainer.train()

    elif command == "test":
        print("--- Step 4: Testing Inference ---")
        generator = CodeGenerator()
        prompt = "import React from 'react';\n// Component for Navigation Bar\nconst Navbar ="
        print("\nResult:\n" + "="*30)
        print(generator.generate(prompt))
        print("="*30)

    else:
        print("Invalid command. Available: scrape, process, train, test")

if __name__ == "__main__":
    main()