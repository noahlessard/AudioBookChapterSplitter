# AudioBookChapterSplitter
A command line tool that seperates an audiobook based on where the word "chapter" appears using ffmpeg and whisper. It uses a custom way of finding the key words using a searching method that is more efficent than cutting the entire audio file up into small chucks.

## Usage:
You can run this tool on a file by doing
```
python AudioChapterSplitter.py -i *insert file path here*
```

