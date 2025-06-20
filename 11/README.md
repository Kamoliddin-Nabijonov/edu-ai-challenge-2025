# Audio Transcription and Analysis Tool

A powerful console application that processes local audio files, transcribes them using OpenAI's Whisper API, summarizes the content using GPT-4.1-mini, and extracts meaningful insights including word count, speaking speed, and frequently mentioned topics.

## Features

- **Local Audio Processing**: Processes audio files from a local samples directory
- **High-Quality Transcription**: Uses OpenAI's Whisper API for accurate speech-to-text
- **Intelligent Summarization**: Generates concise summaries using GPT-4.1-mini
- **Analytics Extraction**: Calculates word count, speaking speed (WPM), and identifies key topics
- **File Output**: Saves transcription, summary, and analytics to separate files with timestamps
- **Console Display**: Shows results directly in the terminal
- **Multiple Format Support**: Supports various audio formats (MP3, WAV, M4A, FLAC, etc.)

## Requirements

- Python 3.7 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- Audio files in supported formats

## Installation

### 1. Clone or Download the Project

```bash
# Create a new directory for the project
mkdir audio-transcription-tool
cd audio-transcription-tool

# Copy all project files to this directory:
# - main.py
# - requirements.txt
# - README.md
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up OpenAI API Key

You have two options for providing your OpenAI API key:

**Option A: Environment Variable (Recommended)**
```bash
# On macOS/Linux:
export OPENAI_API_KEY="your-api-key-here"

# On Windows:
set OPENAI_API_KEY=your-api-key-here
```

**Option B: Command Line Argument**
```bash
python main.py --file "audio.mp3" --api-key "your-api-key-here"
```

### 4. Create Samples Directory and Add Audio Files

**IMPORTANT**: Before running the application, you must create a `samples/` directory and place your audio files there:

```bash
# Create the samples directory
mkdir samples

# Copy your audio files to the samples directory
cp /path/to/your/audio.mp3 samples/
cp /path/to/your/podcast.wav samples/
```

## Usage

### Basic Usage

```bash
python main.py --file "your-audio-file.mp3"
```

### With API Key Argument

```bash
python main.py --file "podcast.wav" --api-key "your-api-key-here"
```

### Help

```bash
python main.py --help
```

## Supported Audio Formats

The application supports various audio formats that OpenAI Whisper accepts:
- **MP3** (.mp3)
- **WAV** (.wav)
- **M4A** (.m4a)
- **FLAC** (.flac)
- **OGG** (.ogg)
- **MP4** (.mp4)
- **MPEG** (.mpeg)
- **MPGA** (.mpga)
- **WEBM** (.webm)

## Directory Structure

After setup, your project should look like this:

```
audio-transcription-tool/
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── samples/            # Directory for your audio files (YOU CREATE THIS)
│   ├── podcast.mp3
│   ├── interview.wav
│   └── speech.m4a
└── outputs/            # Directory for output files (auto-created)
    ├── transcription_*.md
    ├── summary_*.md
    └── analysis_*.json
```

## Output Files

The application creates an `outputs/` directory and saves three files for each transcription:

1. **transcription_[filename]_YYYYMMDD_HHMMSS.md** - Full transcript of the audio
2. **summary_[filename]_YYYYMMDD_HHMMSS.md** - AI-generated summary
3. **analysis_[filename]_YYYYMMDD_HHMMSS.json** - Analytics data including:
   - Source file name and generation timestamp
   - Word count
   - Speaking speed (words per minute)
   - Top 3+ frequently mentioned topics with mention counts

## Example Output

### Console Output
```
🎵 Audio Transcription and Analysis Tool
==================================================
Processing: podcast-episode.mp3

✓ Found audio file: samples/podcast-episode.mp3
Transcribing audio using Whisper...
✓ Audio transcription completed
Generating summary...
✓ Summary generated
Extracting analytics...
✓ Analytics extracted
✓ Transcription saved to: outputs/transcription_podcast-episode_20250116_143022.md
✓ Summary saved to: outputs/summary_podcast-episode_20250116_143022.md
✓ Analytics saved to: outputs/analysis_podcast-episode_20250116_143022.json

============================================================
AUDIO PROCESSING COMPLETE
============================================================

🎵 SOURCE FILE: podcast-episode.mp3

📝 SUMMARY:
----------------------------------------
The speaker discusses the importance of customer onboarding 
in SaaS businesses, highlighting key strategies for improving 
user retention and reducing churn rates...

📊 ANALYTICS:
----------------------------------------
Word Count: 1280
Speaking Speed: 132 WPM
Top Topics:
  • Customer Onboarding: 6 mentions
  • Q4 Roadmap: 4 mentions
  • AI Integration: 3 mentions

📁 FILES CREATED:
----------------------------------------
Transcription: outputs/transcription_podcast-episode_20250116_143022.md
Summary: outputs/summary_podcast-episode_20250116_143022.md
Analytics: outputs/analysis_podcast-episode_20250116_143022.json

✅ Process completed successfully!
```

### Analytics JSON Format
```json
{
  "source_file": "podcast-episode.mp3",
  "generated_on": "2025-01-16 14:30:22",
  "word_count": 1280,
  "speaking_speed_wpm": 132,
  "frequently_mentioned_topics": [
    { "topic": "Customer Onboarding", "mentions": 6 },
    { "topic": "Q4 Roadmap", "mentions": 4 },
    { "topic": "AI Integration", "mentions": 3 }
  ]
}
```

## Error Handling

The application includes comprehensive error handling:

- **File not found**: If the audio file doesn't exist in samples/ directory
- **API errors**: If OpenAI API calls fail
- **File errors**: If file operations fail
- **Unsupported formats**: Warning for potentially unsupported audio formats
- **Permission issues**: If file access is restricted

## API Costs

This application uses OpenAI APIs which incur costs:
- **Whisper API**: ~$0.006 per minute of audio
- **GPT-4.1-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

Typical costs for a 10-minute audio file: ~$0.10-0.20

## Troubleshooting

### Common Issues

**1. "OpenAI API key is required" Error**
```
Error: OpenAI API key is required.
Set the OPENAI_API_KEY environment variable or use --api-key argument.
```
**Solution**: Make sure you've set your OpenAI API key using one of the methods described above.

**2. "Audio file not found" Error**
```
Error: Audio file not found: samples/your-file.mp3
```
**Solution**: 
- Ensure the `samples/` directory exists
- Verify your audio file is actually in the `samples/` directory
- Check the filename spelling and extension

**3. "Failed to transcribe audio" Error**
```
Error: Failed to transcribe audio: The file size exceeds the maximum allowed size
```
**Solution**: OpenAI Whisper has a 25MB file size limit. Use a smaller audio file or compress the audio.

**4. Module Not Found Error**
```
ModuleNotFoundError: No module named 'openai'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

**5. Empty samples directory**
```
Error: Audio file not found: samples/
```
**Solution**: Create the samples directory and add your audio files:
```bash
mkdir samples
cp your-audio-file.mp3 samples/
```

### File Format Warnings

If you see a warning like:
```
⚠️  Warning: your-file.txt may not be a supported audio format
```

This means the file extension is not recognized as a typical audio format. The application will still attempt to process it, but ensure your file is actually an audio file.

## Step-by-Step Example

Here's a complete example from start to finish:

1. **Set up the project:**
   ```bash
   mkdir my-audio-project
   cd my-audio-project
   # Copy main.py, requirements.txt, README.md here
   pip install -r requirements.txt
   ```

2. **Set your API key:**
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

3. **Create samples directory and add audio:**
   ```bash
   mkdir samples
   cp ~/Desktop/my-podcast.mp3 samples/
   ```

4. **Run the application:**
   ```bash
   python main.py --file "my-podcast.mp3"
   ```

5. **Check your results:**
   ```bash
   ls outputs/
   # You'll see three new files with timestamps
   ```

## Security Notes

- **Never commit your API key to version control**
- Keep your audio files in the local `samples/` directory
- Output files are saved locally in the `outputs/` directory
- API keys are not logged or saved anywhere

## Limitations

- Maximum audio file size: 25MB (OpenAI Whisper limit)
- Audio files must be placed in local `samples/` directory before processing
- Processing time depends on audio length and API response times
- Speaking speed calculation is estimated if actual audio duration isn't available

## Contributing

This is a simple, focused tool designed to be easy to understand and modify. Feel free to:
- Add support for subdirectories in samples/
- Implement batch processing for multiple files
- Add more analytics features
- Improve error handling

## License

This project is provided as-is for educational and practical use. 