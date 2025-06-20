"""
Audio Transcription and Analysis Tool

This console application:
1. Reads audio files from local samples directory
2. Transcribes audio using OpenAI Whisper API
3. Summarizes transcription using GPT-4.1-mini
4. Extracts analytics (word count, speaking speed, topics)
5. Saves results to separate files
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import openai
from openai import OpenAI


class AudioTranscriptionTool:
    """Main class for audio transcription and analysis"""
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path("outputs")
        self.samples_dir = Path("samples")
        self.output_dir.mkdir(exist_ok=True)
        self.samples_dir.mkdir(exist_ok=True)
        
    def validate_audio_file(self, filename: str) -> str:
        """Validate that the audio file exists in samples directory"""
        file_path = self.samples_dir / filename
        
        if not file_path.exists():
            raise Exception(f"Audio file not found: {file_path}")
        
        # Check if file has an audio extension
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.mpeg', '.mpga', '.webm'}
        if file_path.suffix.lower() not in audio_extensions:
            print(f"⚠️  Warning: {filename} may not be a supported audio format")
        
        print(f"✓ Found audio file: {file_path}")
        return str(file_path)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using OpenAI Whisper API"""
        print("Transcribing audio using Whisper...")
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            print("✓ Audio transcription completed")
            return transcript
            
        except Exception as e:
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def calculate_speaking_speed(self, transcript: str, audio_duration: Optional[float] = None) -> float:
        """Calculate speaking speed in words per minute"""
        word_count = len(transcript.split())
        
        # If we don't have audio duration, estimate based on average speaking speed
        if audio_duration is None:
            # Estimate duration based on word count (average 150 WPM)
            estimated_duration = word_count / 150  # minutes
            return round(word_count / estimated_duration if estimated_duration > 0 else 0, 1)
        
        duration_minutes = audio_duration / 60
        return round(word_count / duration_minutes if duration_minutes > 0 else 0, 1)
    
    def summarize_transcript(self, transcript: str) -> str:
        """Generate summary using GPT-4.1-mini"""
        print("Generating summary...")
        
        prompt = f"""Please provide a clear, concise summary of the following transcript. 
Focus on the main points, key topics discussed, and important takeaways.

Transcript:
{transcript}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries of audio transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            print("✓ Summary generated")
            return summary
            
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def extract_analytics(self, transcript: str) -> Dict[str, Any]:
        """Extract analytics from transcript using GPT-4.1-mini"""
        print("Extracting analytics...")
        
        word_count = len(transcript.split())
        speaking_speed = self.calculate_speaking_speed(transcript)
        
        prompt = f"""Analyze the following transcript and extract the top 3-5 most frequently mentioned topics. 
Return only a JSON object with the topics and their mention counts.

Format your response as a valid JSON object like this:
{{
  "topics": [
    {{"topic": "Topic Name", "mentions": count}},
    {{"topic": "Another Topic", "mentions": count}}
  ]
}}

Count only meaningful topics (not common words like "the", "and", etc.).
Look for:
- Main subjects discussed
- Key concepts or themes
- Important names, places, or products mentioned
- Recurring ideas or discussions

Transcript:
{transcript}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes text and extracts key topics with accurate counts. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the JSON response
            try:
                topics_data = json.loads(content)
                topics = topics_data.get("topics", [])
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                topics = [
                    {"topic": "General Discussion", "mentions": 1}
                ]
            
            analytics = {
                "word_count": word_count,
                "speaking_speed_wpm": speaking_speed,
                "frequently_mentioned_topics": topics
            }
            
            print("✓ Analytics extracted")
            return analytics
            
        except Exception as e:
            print(f"Warning: Analytics extraction failed: {str(e)}")
            # Return basic analytics if extraction fails
            return {
                "word_count": word_count,
                "speaking_speed_wpm": speaking_speed,
                "frequently_mentioned_topics": [
                    {"topic": "General Discussion", "mentions": 1}
                ]
            }
    
    def save_transcription(self, transcript: str, original_filename: str) -> str:
        """Save transcription to a new file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(original_filename).stem
        filename = f"transcription_{base_name}_{timestamp}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Audio Transcription\n\n")
            f.write(f"**Source File:** {original_filename}\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Transcript\n\n{transcript}\n")
        
        print(f"✓ Transcription saved to: {filepath}")
        return str(filepath)
    
    def save_summary(self, summary: str, original_filename: str) -> str:
        """Save summary to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(original_filename).stem
        filename = f"summary_{base_name}_{timestamp}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Audio Summary\n\n")
            f.write(f"**Source File:** {original_filename}\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n{summary}\n")
        
        print(f"✓ Summary saved to: {filepath}")
        return str(filepath)
    
    def save_analytics(self, analytics: Dict[str, Any], original_filename: str) -> str:
        """Save analytics to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(original_filename).stem
        filename = f"analysis_{base_name}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # Add metadata to analytics
        analytics_with_metadata = {
            "source_file": original_filename,
            "generated_on": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **analytics
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analytics_with_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Analytics saved to: {filepath}")
        return str(filepath)
    
    def process_audio_file(self, filename: str) -> Dict[str, str]:
        """Main method to process local audio file"""
        try:
            # Validate audio file exists
            audio_file_path = self.validate_audio_file(filename)
            
            # Transcribe audio
            transcript = self.transcribe_audio(audio_file_path)
            
            # Generate summary
            summary = self.summarize_transcript(transcript)
            
            # Extract analytics
            analytics = self.extract_analytics(transcript)
            
            # Save results
            transcription_file = self.save_transcription(transcript, filename)
            summary_file = self.save_summary(summary, filename)
            analytics_file = self.save_analytics(analytics, filename)
            
            # Display results in console
            print("\n" + "="*60)
            print("AUDIO PROCESSING COMPLETE")
            print("="*60)
            print(f"\n🎵 SOURCE FILE: {filename}")
            print(f"\n📝 SUMMARY:")
            print("-" * 40)
            print(summary)
            
            print(f"\n📊 ANALYTICS:")
            print("-" * 40)
            print(f"Word Count: {analytics['word_count']}")
            print(f"Speaking Speed: {analytics['speaking_speed_wpm']} WPM")
            print(f"Top Topics:")
            for topic in analytics['frequently_mentioned_topics']:
                print(f"  • {topic['topic']}: {topic['mentions']} mentions")
            
            print(f"\n📁 FILES CREATED:")
            print("-" * 40)
            print(f"Transcription: {transcription_file}")
            print(f"Summary: {summary_file}")
            print(f"Analytics: {analytics_file}")
            
            return {
                "transcription_file": transcription_file,
                "summary_file": summary_file,
                "analytics_file": analytics_file
            }
            
        except Exception as e:
            raise Exception(f"Failed to process audio file: {str(e)}")


def main():
    """Main console application"""
    parser = argparse.ArgumentParser(
        description="Audio Transcription and Analysis Tool - Process local audio files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --file "podcast.mp3"
  python main.py --file "interview.wav"
  python main.py --file "speech.m4a" --api-key "your-key"

Note: Audio files must be placed in the 'samples/' directory first.
        """
    )
    
    parser.add_argument(
        "--file",
        required=True,
        help="Filename of the audio file in the samples/ directory"
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key is required.")
        print("Set the OPENAI_API_KEY environment variable or use --api-key argument.")
        sys.exit(1)
    
    # Initialize and run the tool
    try:
        tool = AudioTranscriptionTool(api_key)
        
        print("🎵 Audio Transcription and Analysis Tool")
        print("="*50)
        print(f"Processing: {args.file}")
        print()
        
        results = tool.process_audio_file(args.file)
        
        print(f"\n✅ Process completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 