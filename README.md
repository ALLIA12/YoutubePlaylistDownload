
# YouTube Playlist Downloader

This Python script allows you to download entire playlists from YouTube either as video files or as audio files. It utilizes multiprocessing to speed up the download process by downloading multiple files in parallel.

## Features

- **Download entire YouTube playlists** as video or audio files.
- **Parallel downloading** using Python's `multiprocessing` to utilize multiple CPU cores.
- **File name sanitization** to ensure valid and safe file names for the downloaded files.
- **Suppression of console output** for clean execution logs, especially useful when converting videos to audio to avoid clutter from progress bars.

## Prerequisites

To run this script, you need Python installed on your system along with the following Python libraries:
- `pytube`: For fetching content from YouTube.
- `moviepy`: For converting video files to audio files.

You can install these dependencies via pip:

```bash
pip install pytube moviepy
```

## Setup

1. Clone this repository or download the script to your local machine.
2. Navigate to the directory containing the script.
3. Ensure that you have the required dependencies installed.

## Usage

To run the script, execute the following command in the terminal:

```bash
python main.py
```

You will be prompted to:
1. **Enter the URL of the YouTube playlist** you wish to download.
2. **Choose the download type** ('audio' or 'video').

The script will then start downloading the playlist content into a directory named after the playlist title, which will be sanitized to remove problematic characters and ensure compatibility with your filesystem.

### Directory Structure

Downloads will be organized in the following directory structure:

```
current_working_directory/
│
└───downloaded_playlist_name/
    │   downloaded_file_1
    │   downloaded_file_2
    │   ...
```

### Notes

- The script handles filename sanitization by removing non-ASCII characters and replacing problematic characters in file and directory names.
- Audio downloads will automatically convert video files to MP3 format and delete the original files to conserve space.
- Errors during download (e.g., due to unavailable videos) will be logged to the console.

## Troubleshooting

If downloads fail due to encoding issues or API changes from YouTube, check if there are updates available for the `pytube` library or consider adjusting the error handling in the script.

