import os
import yt_dlp
import inquirer
import re

class YouTubeDownloader:
    # Initialize the downloader and create downloads directory
    def __init__(self):
        self.video_info = None
        self.download_path = os.path.join(os.getcwd(), 'downloads')
        print(f"\nDefault download folder: {self.download_path}")
        
        # Ask for custom download path
        custom_path = input("\nEnter custom download path (press Enter to use default): ").strip()
        if custom_path:
            if os.path.isabs(custom_path):
                self.download_path = custom_path
            else:
                self.download_path = os.path.abspath(custom_path)
            print(f"Download folder set to: {self.download_path}")
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_path):
            try:
                os.makedirs(self.download_path)
                print(f"Created download directory: {self.download_path}")
            except Exception as e:
                print(f"Error creating directory: {e}")
                print("Falling back to default download path...")
                self.download_path = os.path.join(os.getcwd(), 'downloads')
                os.makedirs(self.download_path, exist_ok=True)

    # Prompt user for video URL and validate input
    def get_video_url(self):
        while True:
            url = input("Enter Video URL: ").strip()
            if url:
                return url
            print("URL cannot be empty. Please try again.")

    # Extract video information and available formats using yt-dlp
    def fetch_video_info(self, url):
        try:
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                
                title = info_dict.get('title', 'Unknown Title')
                formats = []
                resolution_formats = {}  # Dictionary to store best format for each resolution
                
                for f in info_dict.get('formats', []):
                    try:
                        height = f.get('height')
                        width = f.get('width')
                        filesize = f.get('filesize', 0) or 0
                        
                        if not height or not width or filesize == 0:
                            continue
                        
                        resolution = f'{height}p'
                        file_ext = f.get('ext', 'Unknown')
                        fps = f.get('fps', 'Unknown')
                        
                        # Keep only the format with largest filesize for each resolution
                        if resolution not in resolution_formats or filesize > resolution_formats[resolution]['filesize_raw']:
                            resolution_formats[resolution] = {
                                'format_id': f.get('format_id'),
                                'resolution': resolution,
                                'ext': file_ext,
                                'fps': fps,
                                'filesize': self.format_filesize(filesize),
                                'filesize_raw': filesize  # Store raw filesize for comparison
                            }
                    
                    except Exception as format_error:
                        print(f"Skipping problematic format: {format_error}")
                
                # Convert dictionary values to list, excluding the raw filesize
                formats = [{k: v for k, v in fmt.items() if k != 'filesize_raw'} 
                          for fmt in resolution_formats.values()]
                
                return {
                    'title': title,
                    'formats': formats
                }
        
        except Exception as e:
            print(f"Detailed Error fetching video information: {e}")
            import traceback
            traceback.print_exc()
            return None

    # Convert bytes to human-readable file size (B, KB, MB, GB, TB)
    def format_filesize(self, size):
        try:
            size = float(size)
            if size == 0:
                return "Unknown"
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except (TypeError, ValueError):
            return "Unknown"

    # Let user choose between Best Quality or Manual Selection mode
    def select_download_mode(self):
        questions = [
            inquirer.List('mode',
                          message="Download Mode",
                          choices=['Best Quality', 'Manual Selection'],
            ),
        ]
        return inquirer.prompt(questions)['mode']

    # Find the highest quality format based on resolution and file size
    def get_best_format(self, formats):
        sorted_formats = sorted(
            formats,
            key=lambda x: (
                int(x['resolution'].replace('p', '')),
                float(x['filesize'].split()[0]) if x['filesize'] != 'Unknown' else 0
            ),
            reverse=True
        )
        return sorted_formats[0] if sorted_formats else None

    # Display available formats and let user select one
    def select_download_format(self, formats):
        if not formats:
            print("No downloadable formats found!")
            return None

        # Sort formats by resolution (highest to lowest) and filesize
        sorted_formats = sorted(
            formats,
            key=lambda x: (
                int(x['resolution'].replace('p', '')),
                float(x['filesize'].split()[0]) if x['filesize'] != 'Unknown' else 0
            ),
            reverse=True
        )
        
        format_choices = [
            f"[{f['resolution']}] {f['ext']} - {f['filesize']} (FPS: {f['fps']})" 
            for f in sorted_formats
        ]
        
        questions = [
            inquirer.List('format',
                          message="Select Download Format",
                          choices=format_choices,
            ),
        ]
        
        answers = inquirer.prompt(questions)
        
        selected_index = format_choices.index(answers['format'])
        return sorted_formats[selected_index]  # Return from sorted formats

    # Let user choose between video or audio-only download
    def select_download_type(self):
        questions = [
            inquirer.List('type',
                          message="Select Download Type",
                          choices=['Video', 'Video Clip', 'Audio (MP3)', 'Audio Clip (MP3)'],
            ),
        ]
        
        answers = inquirer.prompt(questions)
        return answers['type']

    # Let user select MP3 audio quality (bitrate)
    def select_audio_quality(self):
        questions = [
            inquirer.List('quality',
                          message="Select Audio Quality",
                          choices=[
                              'Best Quality (320 kbps)',
                              'Very High Quality (256 kbps)',
                              'High Quality (192 kbps)',
                              'Standard Quality (128 kbps)',
                              'Low Quality (64 kbps)'
                          ],
            ),
        ]
        answer = inquirer.prompt(questions)['quality']
        return answer.split('(')[1].split('k')[0].strip()  # Extract kbps value

    def parse_timestamp(self, time_str):
        """Convert various time formats to seconds"""
        try:
            # Remove any whitespace
            time_str = time_str.strip()
            
            # Try HH:MM:SS format
            if re.match(r'^\d{1,2}:\d{1,2}:\d{1,2}$', time_str):
                h, m, s = map(int, time_str.split(':'))
                return h * 3600 + m * 60 + s
            
            # Try MM:SS format
            elif re.match(r'^\d{1,2}:\d{1,2}$', time_str):
                m, s = map(int, time_str.split(':'))
                return m * 60 + s
            
            # Try SS format
            elif re.match(r'^\d+$', time_str):
                return int(time_str)
            
            raise ValueError("Invalid time format")
        except Exception:
            return None

    def get_clip_timestamps(self):
        """Get and validate start and end times for the clip"""
        while True:
            start_time = input("\nEnter clip start time (HH:MM:SS, MM:SS, or SS): ").strip()
            start_seconds = self.parse_timestamp(start_time)
            
            if start_seconds is None:
                print("Invalid start time format. Please try again.")
                continue
                
            end_time = input("Enter clip end time (HH:MM:SS, MM:SS, or SS): ").strip()
            end_seconds = self.parse_timestamp(end_time)
            
            if end_seconds is None:
                print("Invalid end time format. Please try again.")
                continue
                
            if end_seconds <= start_seconds:
                print("End time must be greater than start time. Please try again.")
                continue
                
            return start_seconds, end_seconds

    # Download the video/audio with selected format and options
    def download_video(self, url, selected_format, download_type, audio_quality=None, clip_times=None):
        try:
            # Handle both Audio (MP3) and Audio Clip (MP3)
            if download_type in ['Audio (MP3)', 'Audio Clip (MP3)']:
                if clip_times and download_type == 'Audio Clip (MP3)':
                    start_time, end_time = clip_times
                    filename_template = f'%(title)s - [mp3-{audio_quality}kbps] [{start_time}-{end_time}sec].%(ext)s'
                else:
                    filename_template = f'%(title)s - [mp3-{audio_quality}kbps].%(ext)s'

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                    'outtmpl': os.path.join(self.download_path, filename_template),
                }

                # Add clip options if it's an audio clip
                if clip_times and download_type == 'Audio Clip (MP3)':
                    start_time, end_time = clip_times
                    ydl_opts.update({
                        'download_ranges': lambda info_dict, ydl: [{
                            'start_time': start_time,
                            'end_time': end_time
                        }],
                        'force_keyframes_at_cuts': True,
                    })
            else:
                # Existing video download code remains the same
                resolution = selected_format["resolution"]
                ext = selected_format["ext"]
                fps = selected_format["fps"]
                
                if clip_times:
                    start_time, end_time = clip_times
                    filename_template = f'%(title)s - [{resolution}-{fps}fps] [{start_time}-{end_time}sec].%(ext)s'
                else:
                    filename_template = f'%(title)s - [{resolution}-{fps}fps].%(ext)s'

                ydl_opts = {
                    'format': f'{selected_format["format_id"]}+bestaudio/best',
                    'outtmpl': os.path.join(self.download_path, filename_template),
                    'merge_output_format': 'mp4'
                }

                if clip_times:
                    start_time, end_time = clip_times
                    ydl_opts.update({
                        'download_ranges': lambda info_dict, ydl: [{
                            'start_time': start_time,
                            'end_time': end_time
                        }],
                        'force_keyframes_at_cuts': True,
                    })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n✅ Download complete! File saved in {self.download_path}")
        
        except Exception as e:
            print(f"❌ Download failed: {e}")
            import traceback
            traceback.print_exc()

    # Main execution flow coordinating all download steps
    def run(self):
        try:
            url = self.get_video_url()

            print("\n Fetching video information...")
            video_info = self.fetch_video_info(url)
            
            if not video_info or not video_info.get('formats'):
                print("No downloadable formats found. The video might be restricted or unavailable.")
                return

            print(f"\n Video: {video_info['title']}")

            download_type = self.select_download_type()
            
            # Handle both Audio (MP3) and Audio Clip (MP3)
            if download_type in ['Audio (MP3)', 'Audio Clip (MP3)']:
                audio_quality = self.select_audio_quality()
                clip_times = None
                if download_type == 'Audio Clip (MP3)':
                    clip_times = self.get_clip_timestamps()
                print(f"\n⬇️ Downloading audio in {audio_quality}kbps quality...")
                self.download_video(url, None, download_type, audio_quality, clip_times)
                return

            # Handle clip download
            clip_times = None
            if download_type == 'Video Clip':
                clip_times = self.get_clip_timestamps()
                download_type = 'Video'  # Reset to video type for processing

            download_mode = self.select_download_mode()
            
            if download_mode == 'Best Quality':
                selected_format = self.get_best_format(video_info['formats'])
                print(f"\nSelected format: [{selected_format['resolution']}] {selected_format['ext']} - {selected_format['filesize']} (FPS: {selected_format['fps']})")
            else:
                selected_format = self.select_download_format(video_info['formats'])

            if not selected_format:
                print("No format selected. Exiting.")
                return

            print("\n⬇️ Downloading video...")
            self.download_video(url, selected_format, download_type, clip_times=clip_times)

        except KeyboardInterrupt:
            print("\n\n Download cancelled by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()

# Entry point of the script
def main():
    print(f"+{'-'*36} YouTube Video Downloader {'-'*36}+\n")
    downloader = YouTubeDownloader()
    downloader.run()

if __name__ == "__main__":
    main()