# test_least_used.py
import subprocess
import sys
import time
from least_used import (
    filter_by_newest,
    filter_out_recent,
    shorten_name,
    human_readable_time,
)

def test_shorten_name_truncates_long_names():
    name = "a_very_long_filename_that_needs_to_be_shortened.mp3"
    result = shorten_name(name, width=20)
    assert result.endswith("...") and len(result) == 20

def test_filter_by_newest_filters_correctly():
    now = time.time()
    files = [
        ("old_file.mp3", now - 90 * 86400),
        ("new_file.mp3", now - 2 * 86400)
    ]
    filtered = filter_by_newest(files, days_threshold=30)
    assert len(filtered) == 1 and filtered[0][0] == "old_file.mp3"

def test_filter_out_recent_ignores_too_new():
    now = time.time()
    files = [
        ("file1", now - 86400),  # 1 day ago
        ("file2", now - 5 * 86400)
    ]
    result = filter_out_recent(files, ignore_days=3)
    assert len(result) == 1 and result[0][0] == "file2"

def test_human_readable_time_format():
    past = time.time() - (3 * 86400)  # 3 days ago
    result = human_readable_time(past)
    assert "days ago" in result
    assert "(" in result and ")" in result

def test_invalid_flag_crashes_gracefully():
    result = subprocess.run(
        [sys.executable, "least_used.py", "--notarealflag"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "error" in result.stderr.lower()

