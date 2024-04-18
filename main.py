from pytube import YouTube, Playlist
from math import ceil
import sys
import os
from multiprocessing import Process, current_process, cpu_count
from moviepy.editor import AudioFileClip


# Function to sanitize directory names
def sanitize_directory_name(name):
    import re
    # First, replace specific problematic characters
    invalid_char_replacement = {
        "<": "", ">": "", ":": "-", "\"": "", "/": "", "\\": "", "|": "", "?": "", "*": ""
    }
    for invalid_char, replacement in invalid_char_replacement.items():
        name = name.replace(invalid_char, replacement)

    # Remove all non-ASCII characters, should work in most cases, I still got some japanese songs that couldn't download
    # properly for some reason

    name = re.sub(r'[^\x00-\x7F]+', '', name)
    return name


# This function will suppress the console output, moviepy is annoying, it prints a progress bar that is so fkin annoying
# I had to do this to remove it.
def silence_console(func):
    def wrapper(*args, **kwargs):
        # Redirect stdout and stderr to devnull during the function execution
        with open(os.devnull, 'w') as f:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = f
            sys.stderr = f
            try:
                return func(*args, **kwargs)
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

    return wrapper


@silence_console
def convert_to_mp3(temp_filename, final_filename):
    audio_clip = AudioFileClip(temp_filename)
    audio_clip.write_audiofile(final_filename)
    audio_clip.close()


def downloader(video_links, download_directory, download_type):
    process = current_process().name
    for video_url in video_links:
        try:
            yt = YouTube(video_url)
            if download_type == 'video':
                ys = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
                filename = ys.download(output_path=download_directory)
                print(f"{process} --> " + os.path.join(download_directory, os.path.basename(filename)).encode('utf-8',
                                                                                                              'replace').decode(
                    'utf-8') + ' Downloaded')
            elif download_type == 'audio':
                ys = yt.streams.filter(only_audio=True).get_audio_only()
                temp_filename = ys.download(output_path=download_directory)
                temp_basename = os.path.splitext(os.path.basename(temp_filename))[0] + '.mp3'
                final_filename = os.path.join(download_directory, sanitize_directory_name(temp_basename))
                convert_to_mp3(temp_filename, final_filename)
                os.remove(temp_filename)  # Remove the original download if conversion is successful, if it does'nt
                # happen, you will just have a duplicate file, not a big deal, just delete it later
                print(f"{process} --> " + final_filename.split('/')[-1].encode('utf-8', 'replace').decode(
                    'utf-8') + ' Downloaded')
            else:
                raise ValueError("Invalid download type specified. Choose 'audio' or 'video'.")
        except Exception as e:
            error_message = f"Failed to download {video_url}: {e}".encode('utf-8', 'ignore').decode('utf-8')
            print(error_message)


def main():
    # Get playlist URL from the user
    try:
        playlist_url = input("Enter Playlist URL: ")
        download_type = input("Download 'audio' or 'video'? ").lower()
        assert download_type in ['audio', 'video'], "Invalid download type."
        p = Playlist(playlist_url)
    except Exception as e:
        print(f"Failed to load playlist or invalid input: {e}")
        sys.exit(1)

    # Display playlist information
    print(
        f"Playlist Name : {p.title}\nChannel Name  : {p.owner}\nTotal Videos  : {p.length}\nTotal Views   : {p.views}")

    # Prepare directory for downloads
    playlist_name_sanitized = sanitize_directory_name(p.title)
    download_directory = os.path.join(os.getcwd(), playlist_name_sanitized)
    os.makedirs(download_directory, exist_ok=True)

    # Collect video links
    try:
        links = list(p.video_urls)
    except Exception as e:
        print(f"Failed to collect video URLs: {e}")
        sys.exit(1)

    # Calculate the number of links per process
    num_processes = cpu_count()  # Number of CPU cores
    print(f"Found {num_processes} processes, using {num_processes // 2} processes")
    size = ceil(len(links) / (num_processes // 2))
    split_link = lambda links, size: [links[i:i + size] for i in range(0, len(links), size)]
    link_parts = split_link(links, size)

    print("Downloading Started...\n")

    # Creating and starting processes
    processes = []
    for index, part in enumerate(link_parts):
        process = Process(target=downloader, args=(part, download_directory, download_type),
                          name=f"Process-{index + 1}")
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All downloads completed.")


if __name__ == "__main__":
    main()
