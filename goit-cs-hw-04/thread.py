import concurrent.futures
import time
from collections import defaultdict
import os


# Function for serching words in files
def search_keywords(file_paths, keywords):
    result = defaultdict(list)
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file_path)
        except Exception as e:
            print(f"Error during file processing {file_path}: {e}")
    return result


def main(file_list, keywords, num_threads=3):
    # Distribute our file list into chunks
    chunk_size = len(file_list) // num_threads
    chunks = [
        file_list[i : i + chunk_size] for i in range(0, len(file_list), chunk_size)
    ]
    # Add remainig files into last chunk
    if len(file_list) % num_threads != 0:
        chunks[-1].extend(file_list[num_threads * chunk_size :])

    # Countdown
    start_time = time.time()
    #  Create pool threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create dict with Future obj from rec func search_keywords
        future_to_chunk = {
            executor.submit(search_keywords, chunk, keywords): chunk for chunk in chunks
        }
        results = defaultdict(list)

        # Processing of results
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_results = future.result()
            for keyword, paths in chunk_results.items():
                results[keyword].extend(paths)

    # Coundownd ends
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Searching time: {elapsed_time:.2f} seconds")
    return results


if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_list = [os.path.join(script_dir, f"file{i}.txt") for i in range(1, 7)]
    keywords = ["wake", "Wednesdays", "helpful"]

    # # Starting programm
    results = main(file_list, keywords)

    for keyword, files in results.items():
        # Use os.path.basename to each file in files list
        file_names = [os.path.basename(file) for file in files]
        print(f"{keyword}: {file_names}")
