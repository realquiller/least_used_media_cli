import os
import time
import argparse
import random
import platform
import subprocess

from datetime import datetime


# Absolute path to the folder where the python script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "least_used_config.txt")

# Load the source folder from the config file
def load_source_path():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file '{CONFIG_FILE}' not found.")
        print("Please create it and insert the path to your Stream folder.")
        exit(1)

    with open(CONFIG_FILE, "r") as f:
        path = f.read().strip()
        if not path:
            print(f"❌ '{CONFIG_FILE}' is empty. Insert the full path to your Stream folder.")
            exit(1)
        if not os.path.exists(path):
            print(f"❌ The path in '{CONFIG_FILE}' does not exist: {path}")
            exit(1)
        return os.path.normpath(path)
    
# Parsing logic here! (path gets cleaned)
def parse_arguments(source_folder):
    parser = argparse.ArgumentParser(description="Stream file usage analyzer.")
    parser.add_argument("-l", "--limit", type=int, default=20, help="Number of results to show.")
    parser.add_argument("-f", "--folder", type=str, default="", help="Subfolder path inside Stream.")
    parser.add_argument("-n", "--newest", type=int, help="Minimum number of days since last access.")
    parser.add_argument("-r", "--random", action="store_true", help="Pick one random file from the result.")
    parser.add_argument("-e", "--extension", nargs="+", help="Filter by file extensions (e.g., -e .mp3 .wav)")
    parser.add_argument("-i", "--ignore-recent", type=int, default=0, help="Ignore files accessed in the last N days (e.g. --ignore-recent 2)")
    parser.add_argument("--log-to", type=str, default="", help="It will log the results to a file.")
    parser.add_argument("-p", "--play", action="store_true", help="Play/open the selected files.")

    args = parser.parse_args()

    limit_value = args.limit
    cleaned_path = os.path.normpath(args.folder)
    newest_threshold = args.newest
    use_random = args.random
    extensions = args.extension
    ignore_recent = args.ignore_recent
    log_to = args.log_to
    play = args.play
    
    target_path = os.path.join(source_folder, cleaned_path)

    return limit_value, target_path, newest_threshold, use_random, extensions, ignore_recent, log_to, play


# Multiplatform file opener    
def open_file(filepath):
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filepath])
        else:  # Linux
            subprocess.run(["xdg-open", filepath])
        print(f"▶️ Opened: {filepath}")
    except Exception as e:
        print(f"❌ Failed to open {filepath}: {e}")



# This function sets the new limit threshold in days (e. g. not 0 but 2, 5, or even 10 days)
def filter_by_newest(usage_data, days_threshold):
    now = time.time()
    min_age_seconds = days_threshold * 86400  # 1 day = 86400 seconds
    return [(file, atime) for file, atime in usage_data if (now - atime) >= min_age_seconds]


# This function ignores files accessed in the last N days
def filter_out_recent(usage_data, ignore_days):
    now = time.time()
    threshold = ignore_days * 86400
    return [(f, t) for f, t in usage_data if (now - t) >= threshold]

# This function picks a random file
def pick_random_file(usage_data):
    return random.choice(usage_data) if usage_data else None

# This function truncates long names
def shorten_name(name, width=80):
    return name if len(name) <= width else name[:width - 3] + "..."

# This function gets all files
def get_all_files(folder_path, extensions=None):
    all_files = []
    longest_name_len = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if extensions and not any(file.lower().endswith(ext.lower()) for ext in extensions):
                continue  # skip if extension doesn't match

            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                all_files.append(full_path)
                base_name_len = len(shorten_name(os.path.basename(file)))
                if base_name_len > longest_name_len:
                    longest_name_len = base_name_len
    return all_files, longest_name_len

# This function gets human readable time
def human_readable_time(epoch_time):
    dt = datetime.fromtimestamp(epoch_time)
    days_ago = (datetime.now() - dt).days
    return f"{dt.strftime('%Y-%m-%d')} ({days_ago} days ago)"

# This function analyzes file usage
def analyze_usage(files):
    usage_data = []
    for file in files:
        try:
            atime = os.stat(file).st_atime #Access time
            usage_data.append((file, atime))
        except Exception as e:
            print(f"Could not access file info for {file}: {e}")
    return sorted(usage_data, key=lambda x: x[1]) # Least recently accessed first

# This function prints the report (both to console and log file if specified)
def print_report(usage_data, longest_name_len, log_to=None, limit=20):
    print(f"\n Least Recently accessed files:\n")
    if not log_to:
        for file, atime in usage_data[:limit]:
            print(f" - {shorten_name(os.path.basename(file)):{longest_name_len}} | Last used: {human_readable_time(atime)}")

    
    if log_to:
        os.makedirs(os.path.dirname(log_to), exist_ok=True)
        with open(log_to, "w") as f:
            f.write(f"Log generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for file, atime in usage_data[:limit]:
                line = f" - {shorten_name(os.path.basename(file)):{longest_name_len}} | Last used: {human_readable_time(atime)}"
                print(line)
                f.write(line + "\n")

def main():
    source_folder = load_source_path()
    limit_value, target_path, newest_threshold, use_random, extensions, ignore_recent, log_to, play = parse_arguments(source_folder)
    
    print(f"Analyzing '{target_path}' folder...")
    all_files, longest_name_len = get_all_files(target_path, extensions)
    print(f"Longest name of the file is {longest_name_len} characters.")
    print(f"Found {len(all_files)} files.")

    usage_data = analyze_usage(all_files)

    # Apply ignore recent filter
    if ignore_recent > 0:
        print(f"Ignoring files accessed in the last {ignore_recent} days...")
        usage_data = filter_out_recent(usage_data, ignore_recent)

    # Apply newest filter if provided
    if newest_threshold:
        print(f"Filtering to only include files unused for at least {newest_threshold} days...")
        usage_data = filter_by_newest(usage_data, newest_threshold)

    if not usage_data:
        print("No files found after filtering.")
        return
    
    # Apply random mode
    if use_random:
        print(f"\n 🎲 Random mode activated — showing {limit_value} neglected files (shuffled, then sorted by last use):")
        random.shuffle(usage_data)
        usage_data = sorted(usage_data[:limit_value], key=lambda x: x[1])  # sort oldest → newest
        print_report(usage_data, longest_name_len, log_to, limit=limit_value)
        return

    # Apply play mode
    if play:
        print(f"\n🎵 Playing {limit_value} file(s)...")
        for file, _ in usage_data[:limit_value]:
            open_file(file)

    print_report(usage_data, longest_name_len, log_to, limit=limit_value)

if __name__ == "__main__":
    main()

