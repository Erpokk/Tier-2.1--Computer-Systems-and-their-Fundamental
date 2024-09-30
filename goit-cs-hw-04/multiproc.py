import multiprocessing
import time
from collections import defaultdict
import os


# Function for serching words in files
def search_keywords(file_paths, keywords, queue):
    result = defaultdict(list)
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file_path)
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
    queue.put(result)


def main(file_list, keywords, num_process=3):
    # Distribute our file list into chunks
    chunk_size = len(file_list) // num_process
    chunks = [
        file_list[i : i + chunk_size] for i in range(0, len(file_list), chunk_size)
    ]
    # Add remainig files into last chunk
    if len(file_list) % num_process != 0:
        chunks[-1].extend(file_list[num_process * chunk_size :])

    queue = multiprocessing.Queue()
    start_time = time.time()
    # Creating and starting process
    processes = []
    for chunk in chunks:
        p = multiprocessing.Process(
            target=search_keywords, args=(chunk, keywords, queue)
        )
        processes.append(p)
        p.start()

    results = defaultdict(list)
    # Waiting for procces ending
    for p in processes:
        p.join()

    # Getting result from queue
    while not queue.empty():
        chunk_results = queue.get()
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
