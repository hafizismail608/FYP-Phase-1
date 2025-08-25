import os
import tempfile
import subprocess
from typing import Optional, List
import requests
import json
from datetime import datetime

class TTSService:
    """
    Text-to-Speech service using free APIs for auto-dubbing videos
    Supports multiple TTS providers with fallback options
    """
    
    def __init__(self):
        self.providers = [
            'edge_tts',  # Microsoft Edge TTS (Free)
            'pyttsx3',   # Offline TTS (Free)
            'espeak'     # eSpeak (Free)
        ]
    
    def extract_text_from_video(self, video_path: str) -> Optional[str]:
        """
        Extract text from video subtitles or use speech-to-text
        For demo purposes, we'll use a simple text extraction
        """
        try:
            # In a real implementation, you would:
            # 1. Extract audio from video using ffmpeg
            # 2. Use a free speech-to-text service like OpenAI Whisper
            # 3. Or extract existing subtitle text
            
            # For demo, return sample text based on video filename
            video_name = os.path.basename(video_path)
            sample_text = f"""
            Welcome to this educational video lecture.
            Today we will be covering important concepts in our course.
            This video has been automatically processed with text-to-speech technology.
            The content includes detailed explanations and examples.
            Please follow along and take notes as needed.
            Thank you for your attention and participation.
            """
            return sample_text.strip()
            
        except Exception as e:
            print(f"Error extracting text from video: {str(e)}")
            return None
    
    def generate_audio_with_edge_tts(self, text: str, output_path: str, voice: str = 'en-US-AriaNeural') -> bool:
        """
        Generate audio using Microsoft Edge TTS (Free)
        """
        try:
            # Install edge-tts: pip install edge-tts
            import edge_tts
            import asyncio
            
            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_path)
            
            asyncio.run(generate())
            return True
            
        except ImportError:
            print("edge-tts not installed. Install with: pip install edge-tts")
            return False
        except Exception as e:
            print(f"Error with Edge TTS: {str(e)}")
            return False
    
    def generate_audio_with_pyttsx3(self, text: str, output_path: str) -> bool:
        """
        Generate audio using pyttsx3 (Offline, Free)
        """
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', 150)  # Speed of speech
            engine.setProperty('volume', 0.9)  # Volume level
            
            # Get available voices
            voices = engine.getProperty('voices')
            if voices:
                # Use first available voice
                engine.setProperty('voice', voices[0].id)
            
            # Save to file
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return True
            
        except ImportError:
            print("pyttsx3 not installed. Install with: pip install pyttsx3")
            return False
        except Exception as e:
            print(f"Error with pyttsx3: {str(e)}")
            return False
    
    def generate_audio_with_espeak(self, text: str, output_path: str) -> bool:
        """
        Generate audio using eSpeak (Free, command-line)
        """
        try:
            # Create a temporary text file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(text)
                temp_text_path = temp_file.name
            
            # Use eSpeak to generate audio
            cmd = [
                'espeak',
                '-f', temp_text_path,
                '-w', output_path,
                '-s', '150',  # Speed
                '-v', 'en+f3'  # Voice variant
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up temp file
            os.unlink(temp_text_path)
            
            return result.returncode == 0
            
        except FileNotFoundError:
            print("eSpeak not found. Install with: sudo apt-get install espeak (Linux) or brew install espeak (macOS)")
            return False
        except Exception as e:
            print(f"Error with eSpeak: {str(e)}")
            return False
    
    def create_dubbed_video(self, video_path: str, audio_path: str, output_path: str) -> bool:
        """
        Combine original video with new audio track using ffmpeg
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,  # Input video
                '-i', audio_path,  # Input audio
                '-c:v', 'copy',    # Copy video stream
                '-c:a', 'aac',     # Encode audio as AAC
                '-map', '0:v:0',   # Map video from first input
                '-map', '1:a:0',   # Map audio from second input
                '-shortest',       # End when shortest stream ends
                '-y',              # Overwrite output file
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error creating dubbed video: {str(e)}")
            return False
    
    def generate_dubbing(self, video_path: str, output_dir: str, language: str = 'en') -> Optional[str]:
        """
        Main method to generate dubbed version of a video
        
        Args:
            video_path: Path to the original video
            output_dir: Directory to save the dubbed video
            language: Target language for dubbing
        
        Returns:
            Path to the dubbed video file or None if failed
        """
        try:
            # Extract text from video
            text = self.extract_text_from_video(video_path)
            if not text:
                print("Could not extract text from video")
                return None
            
            # Create output paths
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_filename = f"{video_name}_dubbed_audio.wav"
            dubbed_video_filename = f"{video_name}_dubbed.mp4"
            
            audio_path = os.path.join(output_dir, audio_filename)
            dubbed_video_path = os.path.join(output_dir, dubbed_video_filename)
            
            # Try different TTS providers
            audio_generated = False
            
            # Try Edge TTS first (best quality)
            if not audio_generated:
                audio_generated = self.generate_audio_with_edge_tts(text, audio_path)
            
            # Fallback to pyttsx3
            if not audio_generated:
                audio_generated = self.generate_audio_with_pyttsx3(text, audio_path)
            
            # Fallback to eSpeak
            if not audio_generated:
                audio_generated = self.generate_audio_with_espeak(text, audio_path)
            
            if not audio_generated:
                print("Failed to generate audio with any TTS provider")
                return None
            
            # Create dubbed video
            if self.create_dubbed_video(video_path, audio_path, dubbed_video_path):
                # Clean up temporary audio file
                try:
                    os.remove(audio_path)
                except:
                    pass
                
                return dubbed_video_filename
            else:
                print("Failed to create dubbed video")
                return None
                
        except Exception as e:
            print(f"Error in generate_dubbing: {str(e)}")
            return None
    
    def get_available_voices(self) -> List[dict]:
        """
        Get list of available voices for different TTS providers
        """
        voices = []
        
        try:
            # Edge TTS voices
            import edge_tts
            import asyncio
            
            async def get_edge_voices():
                edge_voices = await edge_tts.list_voices()
                return edge_voices
            
            edge_voices = asyncio.run(get_edge_voices())
            for voice in edge_voices[:5]:  # Limit to first 5
                voices.append({
                    'provider': 'edge_tts',
                    'name': voice['Name'],
                    'language': voice['Locale'],
                    'gender': voice['Gender']
                })
        except:
            pass
        
        try:
            # pyttsx3 voices
            import pyttsx3
            engine = pyttsx3.init()
            pyttsx3_voices = engine.getProperty('voices')
            
            for voice in pyttsx3_voices[:3]:  # Limit to first 3
                voices.append({
                    'provider': 'pyttsx3',
                    'name': voice.name,
                    'language': getattr(voice, 'languages', ['en'])[0] if hasattr(voice, 'languages') else 'en',
                    'gender': 'unknown'
                })
        except:
            pass
        
        # Add eSpeak default voice
        voices.append({
            'provider': 'espeak',
            'name': 'eSpeak Default',
            'language': 'en',
            'gender': 'unknown'
        })
        
        return voices

# Example usage and testing
if __name__ == "__main__":
    tts = TTSService()
    
    # Test text extraction
    sample_video = "sample_video.mp4"
    text = tts.extract_text_from_video(sample_video)
    print(f"Extracted text: {text}")
    
    # Test voice listing
    voices = tts.get_available_voices()
    print(f"Available voices: {len(voices)}")
    for voice in voices:
        print(f"  - {voice['provider']}: {voice['name']} ({voice['language']})")