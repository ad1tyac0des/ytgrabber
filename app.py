import os
import yt_dlp
import inquirer

class YouTubeDownloader:
    def __init__(self):
        self.video_info = None
        self.download_path = os.path.join(os.getcwd(), 'downloads')
        
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def get_video_url(self):
        while True:
            url = input("Enter Video URL: ").strip()
            if url:
                return url
            print("URL cannot be empty. Please try again.")

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
                
                for f in info_dict.get('formats', []):
                    try:
                        height = f.get('height')
                        width = f.get('width')
                        
                        if not height or not width:
                            continue
                        
                        resolution = f'{height}p'
                        file_ext = f.get('ext', 'Unknown')
                        fps = f.get('fps', 'Unknown')
                        filesize = f.get('filesize', 0) or 0
                        
                        formats.append({
                            'format_id': f.get('format_id'),
                            'resolution': resolution,
                            'ext': file_ext,
                            'fps': fps,
                            'filesize': self.format_filesize(filesize)
                        })
                    
                    except Exception as format_error:
                        print(f"Skipping problematic format: {format_error}")
                
                return {
                    'title': title,
                    'formats': formats
                }
        
        except Exception as e:
            print(f"Detailed Error fetching video information: {e}")
            import traceback
            traceback.print_exc()
            return None

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

    def select_download_mode(self):
        questions = [
            inquirer.List('mode',
                          message="Download Mode",
                          choices=['Best Quality', 'Manual Selection'],
            ),
        ]
        return inquirer.prompt(questions)['mode']

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

    def select_download_format(self, formats):
        if not formats:
            print("No downloadable formats found!")
            return None

        format_choices = [
            f"[{f['resolution']}] {f['ext']} - {f['filesize']} (FPS: {f['fps']})" 
            for f in formats
        ]
        
        questions = [
            inquirer.List('format',
                          message="Select Download Format",
                          choices=format_choices,
            ),
        ]
        
        answers = inquirer.prompt(questions)
        
        selected_index = format_choices.index(answers['format'])
        return formats[selected_index]

    def select_download_type(self):
        questions = [
            inquirer.List('type',
                          message="Select Download Type",
                          choices=['Video', 'Audio (MP3)'],
            ),
        ]
        
        answers = inquirer.prompt(questions)
        return answers['type']

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

    def download_video(self, url, selected_format, download_type, audio_quality=None):
        try:
            if download_type == 'Audio (MP3)':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                }
            else:
                ydl_opts = {
                    'format': f'{selected_format["format_id"]}+bestaudio/best',
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n✅ Download complete! File saved in {self.download_path}")
        
        except Exception as e:
            print(f"❌ Download failed: {e}")
            import traceback
            traceback.print_exc()

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
            
            if download_type == 'Audio (MP3)':
                audio_quality = self.select_audio_quality()
                print(f"\n⬇️ Downloading audio in {audio_quality}kbps quality...")
                self.download_video(url, None, download_type, audio_quality)
                return

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
            self.download_video(url, selected_format, download_type)

        except KeyboardInterrupt:
            print("\n\n Download cancelled by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()

def main():
    print(f"+{'-'*36} YouTube Video Downloader {'-'*36}+\n")
    downloader = YouTubeDownloader()
    downloader.run()

if __name__ == "__main__":
    main()