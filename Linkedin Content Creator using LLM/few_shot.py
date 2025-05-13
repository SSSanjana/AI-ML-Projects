# few_shot.py
import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        """
        Initializes the FewShotPosts class by loading the JSON post data
        and preparing metadata like length categories and unique tags.
        """
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        """
        Loads the LinkedIn posts from a JSON file, categorizes them by length,
        and extracts all unique tags.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Error loading JSON file: {e}")
            return

        self.df = pd.json_normalize(posts)

        # Categorize by length
        self.df['length'] = self.df['line_count'].apply(self.categorize_length)

        # Safely collect unique tags
        self.df['tags'] = self.df['tags'].apply(lambda x: x if isinstance(x, list) else [])
        all_tags = sum(self.df['tags'], [])
        self.unique_tags = sorted(set(all_tags))

    def categorize_length(self, line_count):
        """
        Categorizes a post based on its line count.
        """
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length, language, tag):
        """
        Returns a list of posts matching the specified length, language, and tag.
        """
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient='records')

    def get_tags(self):
        """
        Returns a list of all unique tags found in the dataset.
        """
        return self.unique_tags

# Example usage
if __name__ == "__main__":
    fs = FewShotPosts()
    print("📌 Available Tags:", fs.get_tags())

    sample_posts = fs.get_filtered_posts(length="Medium", language="Hinglish", tag="Job Search")
    print(f"📝 Found {len(sample_posts)} posts:\n", sample_posts)
