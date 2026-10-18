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

import yt_dlp

from backend.app.services.downloader import download_via_ytdlp
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

    def _get_worker_and_service_format_selectors(self):
        worker_fmt = None
        service_fmt = None

        with patch("yt_dlp.YoutubeDL") as mock_ydl_cls:
            mock_ydl = MagicMock()
            mock_ydl.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.return_value = None
            mock_ydl_cls.return_value = mock_ydl

            download_worker_media("https://www.instagram.com/reel/De8smJtvao0/")
            self.assertTrue(mock_ydl_cls.called)
            worker_fmt = mock_ydl_cls.call_args[0][0]["format"]

        with patch("yt_dlp.YoutubeDL") as mock_ydl_cls, \
             patch("backend.app.services.downloader.download_instagram_fallback", return_value=(False, "mocked")):
            mock_ydl = MagicMock()
            mock_ydl.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.return_value = None
            mock_ydl_cls.return_value = mock_ydl

            with tempfile.TemporaryDirectory() as tmpdir:
                download_via_ytdlp("https://www.instagram.com/reel/De8smJtvao0/", Path(tmpdir))
            self.assertTrue(mock_ydl_cls.called)
            service_fmt = mock_ydl_cls.call_args[0][0]["format"]

        return worker_fmt, service_fmt

    def test_portrait_video_with_separate_audio_selection(self):
        """Scenario 1: Sanitized 360x640 portrait video + M4A audio pair is selected."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        # Sanitized format fixture matching the Instagram Reel De8smJtvao0 format catalog
        sanitized_formats = [
            {"format_id": "vid_360x640", "url": "https://example.com/v360.mp4", "ext": "mp4", "width": 360, "height": 640, "vcodec": "avc1.4d401f", "acodec": "none"},
            {"format_id": "prog_unknown", "url": "https://example.com/p.mp4", "ext": "mp4", "width": None, "height": None, "vcodec": "unknown", "acodec": "unknown"},
            {"format_id": "vid_540x960", "url": "https://example.com/v540.mp4", "ext": "mp4", "width": 540, "height": 960, "vcodec": "avc1.4d401f", "acodec": "none"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": sanitized_formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 1, "Expected exactly 1 selected format stream/pair")
        match = selected[0]
        req = match.get("requested_formats", [])
        self.assertEqual(len(req), 2, "Expected separate video and audio streams to be merged")
        self.assertEqual(req[0]["format_id"], "vid_360x640")
        self.assertEqual(req[1]["format_id"], "audio_m4a")
        self.assertEqual(match["format_id"], "vid_360x640+audio_m4a")

        # Also verify pre-merged portrait format (360x640 with both vcodec and acodec)
        premerged_portrait = [
            {"format_id": "pre_360x640", "url": "https://example.com/pre_portrait.mp4", "ext": "mp4", "width": 360, "height": 640, "vcodec": "avc1.4d401f", "acodec": "mp4a.40.2"}
        ]
        ctx_pre = {"formats": premerged_portrait, "incomplete_formats": False}
        selected_pre = list(selector(ctx_pre))
        self.assertEqual(len(selected_pre), 1)
        self.assertEqual(selected_pre[0]["format_id"], "pre_360x640")

    def test_landscape_format_compatibility_selection(self):
        """Scenario 2: Known-dimension 640x360 landscape format remains selectable."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        landscape_formats = [
            {"format_id": "vid_640x360", "url": "https://example.com/vl360.mp4", "ext": "mp4", "width": 640, "height": 360, "vcodec": "avc1.4d401f", "acodec": "none"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": landscape_formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 1)
        req = selected[0].get("requested_formats", [])
        self.assertEqual(len(req), 2)
        self.assertEqual(req[0]["format_id"], "vid_640x360")
        self.assertEqual(req[1]["format_id"], "audio_m4a")

        # Also verify pre-merged landscape format
        premerged_landscape = [
            {"format_id": "pre_640x360", "url": "https://example.com/pre_land.mp4", "ext": "mp4", "width": 640, "height": 360, "vcodec": "avc1.4d401f", "acodec": "mp4a.40.2"}
        ]
        ctx_pre = {"formats": premerged_landscape, "incomplete_formats": False}
        selected_pre = list(selector(ctx_pre))
        self.assertEqual(len(selected_pre), 1)
        self.assertEqual(selected_pre[0]["format_id"], "pre_640x360")

    def test_resolution_ceiling_rejects_higher_resolution_formats(self):
        """Scenario 3: When only formats exceeding 360p ceiling exist, selector rejects all of them."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        # Higher portrait and landscape resolutions (540p, 720p, 1080p)
        highres_formats = [
            {"format_id": "vid_540x960", "url": "https://example.com/v540.mp4", "ext": "mp4", "width": 540, "height": 960, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "vid_720x1280", "url": "https://example.com/v720.mp4", "ext": "mp4", "width": 720, "height": 1280, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "vid_1080x1920", "url": "https://example.com/v1080.mp4", "ext": "mp4", "width": 1080, "height": 1920, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "vid_1280x720", "url": "https://example.com/vl720.mp4", "ext": "mp4", "width": 1280, "height": 720, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "vid_1920x1080", "url": "https://example.com/vl1080.mp4", "ext": "mp4", "width": 1920, "height": 1080, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": highres_formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 0, f"Expected 0 matches for high-res formats, got: {selected}")

    def test_unknown_dimensions_formats_rejected(self):
        """Scenario 4: Formats with unknown/missing dimensions (width/height=None) are rejected."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        unknown_dim_formats = [
            {"format_id": "prog_1", "url": "https://example.com/p1.mp4", "ext": "mp4", "width": None, "height": None, "vcodec": "unknown", "acodec": "unknown"},
            {"format_id": "prog_2", "url": "https://example.com/p2.mp4", "ext": "mp4", "width": None, "height": None, "vcodec": "unknown", "acodec": "unknown"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": unknown_dim_formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 0, f"Expected 0 matches for unknown dimension formats, got: {selected}")

    def test_reject_1280x360_landscape_width_bound_exceeded(self):
        """Reject 1280x360 format because width exceeds landscape bound (width<=640)."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        formats = [
            {"format_id": "vid_1280x360", "url": "https://example.com/v1280x360.mp4", "ext": "mp4", "width": 1280, "height": 360, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 0, f"Expected 1280x360 to be rejected, got: {selected}")

        premerged = [
            {"format_id": "pre_1280x360", "url": "https://example.com/pre.mp4", "ext": "mp4", "width": 1280, "height": 360, "vcodec": "avc1", "acodec": "mp4a.40.2"}
        ]
        ctx_pre = {"formats": premerged, "incomplete_formats": False}
        selected_pre = list(selector(ctx_pre))
        self.assertEqual(len(selected_pre), 0, f"Expected pre-merged 1280x360 to be rejected, got: {selected_pre}")

    def test_reject_360x960_portrait_height_bound_exceeded(self):
        """Reject 360x960 format because height exceeds portrait bound (height<=640)."""
        worker_fmt, _ = self._get_worker_and_service_format_selectors()
        ydl = yt_dlp.YoutubeDL({"format": worker_fmt})
        selector = ydl.build_format_selector(worker_fmt)

        formats = [
            {"format_id": "vid_360x960", "url": "https://example.com/v360x960.mp4", "ext": "mp4", "width": 360, "height": 960, "vcodec": "avc1", "acodec": "none"},
            {"format_id": "audio_m4a", "url": "https://example.com/a.m4a", "ext": "m4a", "width": None, "height": None, "vcodec": "none", "acodec": "mp4a.40.2"},
        ]
        ctx = {"formats": formats, "incomplete_formats": False}
        selected = list(selector(ctx))
        self.assertEqual(len(selected), 0, f"Expected 360x960 to be rejected, got: {selected}")

        premerged = [
            {"format_id": "pre_360x960", "url": "https://example.com/pre.mp4", "ext": "mp4", "width": 360, "height": 960, "vcodec": "avc1", "acodec": "mp4a.40.2"}
        ]
        ctx_pre = {"formats": premerged, "incomplete_formats": False}
        selected_pre = list(selector(ctx_pre))
        self.assertEqual(len(selected_pre), 0, f"Expected pre-merged 360x960 to be rejected, got: {selected_pre}")

    def test_worker_and_service_format_selectors_consistent_and_guarded(self):
        """Scenario 5: Worker and service downloader apply identical dual-bounded format rules."""
        worker_fmt, service_fmt = self._get_worker_and_service_format_selectors()
        expected_fmt = (
            "bestvideo[height<=360][width<=640][ext=mp4]+bestaudio[ext=m4a]/"
            "bestvideo[width<=360][height<=640][ext=mp4]+bestaudio[ext=m4a]/"
            "bestvideo[height<=360][width<=640]+bestaudio/"
            "bestvideo[width<=360][height<=640]+bestaudio/"
            "best[height<=360][width<=640][ext=mp4]/"
            "best[width<=360][height<=640][ext=mp4]/"
            "best[height<=360][width<=640]/"
            "best[width<=360][height<=640]"
        )
        self.assertEqual(worker_fmt, expected_fmt)
        self.assertEqual(service_fmt, expected_fmt)
        self.assertEqual(worker_fmt, service_fmt)

        for fmt in (worker_fmt, service_fmt):
            self.assertIn("height<=360", fmt)
            self.assertIn("width<=640", fmt)
            self.assertIn("width<=360", fmt)
            self.assertIn("height<=640", fmt)
            self.assertNotIn("?", fmt, "Selector must not use '?' unknown-dimension fallback")
            self.assertFalse(fmt.endswith("/best"), "Selector must not end with unconstrained /best")
            self.assertNotIn("/best/", fmt)
            self.assertNotIn("bestvideo/", fmt)


if __name__ == "__main__":
    unittest.main()
