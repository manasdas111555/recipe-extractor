"""
UPA-1305: Media Downloader Info NameError Regression Suite
==========================================================
Verifies that download_worker_media correctly assigns and handles `info`
from yt-dlp extract_info(download=True) without raising NameError or
masking errors.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from backend.app.workers.media_downloader import (
    download_worker_media,
    managed_worker_download,
)


class TestMediaDownloaderRegression(unittest.TestCase):
    """Targeted regression tests for UPA-1305."""

    def test_download_worker_media_assigns_and_processes_info_success(self):
        """Verify download_worker_media extracts info with download=True and returns file path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            fake_media = tmp_path / "worker_test_media.mp4"
            fake_media.write_bytes(b"dummy mp4 video bytes")

            with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
                mock_ydl = MagicMock()
                mock_ydl.__enter__.return_value = mock_ydl
                # Pre-flight returns duration within limit
                mock_ydl.extract_info.side_effect = [
                    {"duration": 30, "id": "test_video"},  # download=False
                    {"duration": 30, "id": "test_video", "ext": "mp4"},  # download=True
                ]
                mock_ydl.prepare_filename.return_value = str(fake_media)
                mock_ydl_cls.return_value = mock_ydl

                success, result_path = download_worker_media(
                    "https://www.instagram.com/reel/C_test123/",
                    output_dir=tmp_path
                )

                self.assertTrue(success)
                self.assertEqual(os.path.abspath(result_path), str(fake_media.resolve()))
                # Verify extract_info was called with download=True
                download_calls = [
                    call for call in mock_ydl.extract_info.call_args_list
                    if call[1].get("download") is True
                ]
                self.assertTrue(len(download_calls) >= 1, "extract_info(download=True) was never called!")

    def test_download_worker_media_fails_without_name_error_when_info_is_none(self):
        """Verify that when extract_info returns None, no NameError is raised and failure is clean."""
        with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
            mock_ydl = MagicMock()
            mock_ydl.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.return_value = None
            mock_ydl_cls.return_value = mock_ydl

            success, err_msg = download_worker_media("https://www.instagram.com/reel/C_empty/")

            self.assertFalse(success)
            self.assertNotIn("name 'info' is not defined", err_msg)
            self.assertIn("Failed to locate downloaded media stream file", err_msg)

    def test_download_worker_media_propagates_ytdlp_exception_without_name_error(self):
        """Verify that actual downstream errors (e.g. rate limit / network error) propagate truthfully."""
        with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
            mock_ydl = MagicMock()
            mock_ydl.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.side_effect = Exception("HTTP 429 Too Many Requests: Rate limited by Instagram")
            mock_ydl_cls.return_value = mock_ydl

            success, err_msg = download_worker_media("https://www.instagram.com/reel/C_ratelimit/")

            self.assertFalse(success)
            self.assertNotIn("name 'info' is not defined", err_msg)
            self.assertIn("HTTP 429 Too Many Requests", err_msg)

    def test_download_worker_media_exceeding_duration_triggers_cleanup(self):
        """Verify that post-download duration guardrail deletes candidate and rejects >90s video."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            fake_long_media = tmp_path / "long_video.mp4"
            fake_long_media.write_bytes(b"dummy long video bytes")

            with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
                mock_ydl = MagicMock()
                mock_ydl.__enter__.return_value = mock_ydl
                # Pre-flight skipped / missing duration, but download=True returns duration=120
                mock_ydl.extract_info.side_effect = [
                    {},  # download=False
                    {"duration": 120, "id": "long_video", "ext": "mp4"},  # download=True
                ]
                mock_ydl.prepare_filename.return_value = str(fake_long_media)
                mock_ydl_cls.return_value = mock_ydl

                success, err_msg = download_worker_media(
                    "https://www.instagram.com/reel/C_toolong/",
                    output_dir=tmp_path,
                    max_duration=90
                )

                self.assertFalse(success)
                self.assertIn("exceeds maximum allowed limit", err_msg)
                self.assertFalse(fake_long_media.exists(), "Downloaded long media file was not cleaned up!")

    def test_managed_worker_download_deterministic_cleanup(self):
        """Verify managed_worker_download context manager cleans up file upon block exit."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            fake_stream = tmp_path / "stream_cleanup_test.mp4"
            fake_stream.write_bytes(b"stream bytes for cleanup test")

            with patch("backend.app.workers.media_downloader.download_worker_media", return_value=(True, str(fake_stream))):
                with managed_worker_download("https://www.instagram.com/reel/C_clean/") as (ok, fpath):
                    self.assertTrue(ok)
                    self.assertTrue(os.path.exists(fpath))

                # After exiting the context manager block, file must be unlinked
                self.assertFalse(fake_stream.exists(), "managed_worker_download failed to delete temporary file!")


if __name__ == "__main__":
    unittest.main()
