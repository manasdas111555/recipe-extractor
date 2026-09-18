import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple

def get_ffmpeg_path() -> str:
    """Returns path to ffmpeg executable or 'ffmpeg' if in system PATH."""
    ffmpeg_bin = shutil.which("ffmpeg")
    return ffmpeg_bin or "ffmpeg"

def extract_audio_from_video(video_path: Path, output_mp3_path: Path = None) -> Tuple[bool, Path, str]:
    """
    Extracts audio track from a video file into an MP3 file using FFmpeg.
    Returns (success, mp3_path, error_message).
    """
    video_path = Path(video_path)
    if not video_path.exists():
        return False, None, f"Video file not found: {video_path}"

    if output_mp3_path is None:
        output_mp3_path = video_path.with_suffix(".mp3")
    else:
        output_mp3_path = Path(output_mp3_path)

    ffmpeg_bin = get_ffmpeg_path()
    cmd = [
        ffmpeg_bin,
        "-y",               # Overwrite existing
        "-i", str(video_path),
        "-vn",              # Disable video recording
        "-acodec", "libmp3lame",
        "-q:a", "4",        # Good variable bitrate quality
        str(output_mp3_path)
    ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if proc.returncode == 0 and output_mp3_path.exists() and output_mp3_path.stat().st_size > 0:
            return True, output_mp3_path, ""
        return False, None, f"FFmpeg audio extraction failed: {proc.stderr.decode('utf-8', errors='ignore')[:300]}"
    except Exception as e:
        return False, None, f"FFmpeg execution error: {str(e)}"

def extract_keyframes(video_path: Path, output_dir: Path = None, num_frames: int = 5) -> Tuple[bool, List[Path], str]:
    """
    Extracts representative keyframe images across the video duration using FFmpeg.
    Returns (success, list_of_image_paths, error_message).
    """
    video_path = Path(video_path)
    if not video_path.exists():
        return False, [], f"Video file not found: {video_path}"

    if output_dir is None:
        output_dir = video_path.parent / f"frames_{video_path.stem}"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_pattern = str(output_dir / "frame_%02d.jpg")

    ffmpeg_bin = get_ffmpeg_path()
    # Extract evenly spaced frames (approx 1 frame every 6 seconds, max num_frames)
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(video_path),
        "-vf", "fps=1/6,scale=720:-1",
        "-vframes", str(num_frames),
        "-q:v", "3",
        out_pattern
    ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        frames = sorted(list(output_dir.glob("frame_*.jpg")))
        if frames:
            return True, frames, ""
        return False, [], f"FFmpeg keyframe extraction produced no frames: {proc.stderr.decode('utf-8', errors='ignore')[:300]}"
    except Exception as e:
        return False, [], f"FFmpeg keyframe execution error: {str(e)}"
