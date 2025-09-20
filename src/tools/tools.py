def trim_video(video_s3_uri: str, start_time: float, end_time: float) -> dict:
    """
    Trim a video between start_time and end_time.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.

    Returns:
        dict: Contains a success message and the S3 URI of the trimmed video.
    """
    return {
        "message": "Video trimmed successfully",
        "media": "s3://mock-bucket/output/trimmed_video.mp4"
    }


def split_video(video_s3_uri: str, split_time: float) -> dict:
    """
    Split a video into two clips at a specific time.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        split_time (float): Time in seconds to split the video.

    Returns:
        dict: Contains a success message and a list of S3 URIs of the two resulting clips.
    """
    return {
        "message": "Video split successfully",
        "media": [
            "s3://mock-bucket/output/split_part1.mp4",
            "s3://mock-bucket/output/split_part2.mp4"
        ]
    }


def merge_clips(clip1_s3_uri: str, clip2_s3_uri: str) -> dict:
    """
    Merge two video clips sequentially.

    Args:
        clip1_s3_uri (str): S3 URI of the first video clip.
        clip2_s3_uri (str): S3 URI of the second video clip.

    Returns:
        dict: Contains a success message and the S3 URI of the merged video.
    """
    return {
        "message": "Clips merged successfully",
        "media": "s3://mock-bucket/output/merged_video.mp4"
    }


def crop_frame(video_s3_uri: str, x: int, y: int, width: int, height: int) -> dict:
    """
    Crop a video frame to a specific region.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        x (int): X coordinate of the top-left corner.
        y (int): Y coordinate of the top-left corner.
        width (int): Width of the cropped area.
        height (int): Height of the cropped area.

    Returns:
        dict: Contains a success message and the S3 URI of the cropped video.
    """
    return {
        "message": "Video cropped successfully",
        "media": "s3://mock-bucket/output/cropped_video.mp4"
    }


def resize_video(video_s3_uri: str, target_width: int, target_height: int) -> dict:
    """
    Resize a video to the target dimensions.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        target_width (int): Desired width in pixels.
        target_height (int): Desired height in pixels.

    Returns:
        dict: Contains a success message and the S3 URI of the resized video.
    """
    return {
        "message": "Video resized successfully",
        "media": "s3://mock-bucket/output/resized_video.mp4"
    }


def change_resolution(video_s3_uri: str, width: int, height: int) -> dict:
    """
    Change the resolution of a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        width (int): Target width in pixels.
        height (int): Target height in pixels.

    Returns:
        dict: Contains a success message and the S3 URI of the video with new resolution.
    """
    return {
        "message": "Video resolution changed successfully",
        "media": "s3://mock-bucket/output/resolution_changed_video.mp4"
    }


def adjust_frame_rate(video_s3_uri: str, target_fps: int) -> dict:
    """
    Adjust the frame rate of a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        target_fps (int): Desired frames per second.

    Returns:
        dict: Contains a success message and the S3 URI of the frame rate-adjusted video.
    """
    return {
        "message": "Frame rate adjusted successfully",
        "media": "s3://mock-bucket/output/frame_rate_adjusted_video.mp4"
    }


def color_correct(video_s3_uri: str, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0) -> dict:
    """
    Apply basic color correction to a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        brightness (float): Brightness factor (default 1.0 = no change).
        contrast (float): Contrast factor (default 1.0 = no change).
        saturation (float): Saturation factor (default 1.0 = no change).

    Returns:
        dict: Contains a success message and the S3 URI of the color-corrected video.
    """
    return {
        "message": "Color correction applied successfully",
        "media": "s3://mock-bucket/output/color_corrected_video.mp4"
    }


def add_transition(clip1_s3_uri: str, clip2_s3_uri: str, transition_type: str, duration: float) -> dict:
    """
    Add a transition effect between two video clips.

    Args:
        clip1_s3_uri (str): S3 URI of the first video clip.
        clip2_s3_uri (str): S3 URI of the second video clip.
        transition_type (str): Type of transition (e.g., "fade", "wipe").
        duration (float): Duration of the transition in seconds.

    Returns:
        dict: Contains a success message and the S3 URI of the video with transition applied.
    """
    return {
        "message": "Transition added successfully",
        "media": "s3://mock-bucket/output/transition_video.mp4"
    }


def add_overlay(video_s3_uri: str, overlay_image_s3_uri: str, x: int, y: int) -> dict:
    """
    Overlay an image on top of a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        overlay_image_s3_uri (str): S3 URI of the overlay image.
        x (int): X coordinate position of the overlay.
        y (int): Y coordinate position of the overlay.

    Returns:
        dict: Contains a success message and the S3 URI of the video with overlay applied.
    """
    return {
        "message": "Overlay added successfully",
        "media": "s3://mock-bucket/output/overlay_video.mp4"
    }


def add_subtitles(video_s3_uri: str, subtitles_s3_uri: str) -> dict:
    """
    Add subtitles to a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        subtitles_s3_uri (str): S3 URI of the subtitle file (.srt or .vtt).

    Returns:
        dict: Contains a success message and the S3 URI of the video with subtitles added.
    """
    return {
        "message": "Subtitles added successfully",
        "media": "s3://mock-bucket/output/subtitled_video.mp4"
    }


def add_captions(video_s3_uri: str, text: str, start_time: float, end_time: float, x: int, y: int) -> dict:
    """
    Add custom captions as text on the video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        text (str): Caption text to display.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
        x (int): X coordinate position of the text.
        y (int): Y coordinate position of the text.

    Returns:
        dict: Contains a success message and the S3 URI of the video with captions added.
    """
    return {
        "message": "Captions added successfully",
        "media": "s3://mock-bucket/output/captioned_video.mp4"
    }


def add_soundtrack(video_s3_uri: str, audio_s3_uri: str, start_time: float = 0.0) -> dict:
    """
    Add a soundtrack to a video.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        audio_s3_uri (str): S3 URI of the audio file.
        start_time (float): Start time in seconds for the audio (default 0.0).

    Returns:
        dict: Contains a success message and the S3 URI of the video with soundtrack added.
    """
    return {
        "message": "Soundtrack added successfully",
        "media": "s3://mock-bucket/output/soundtrack_video.mp4"
    }


def adjust_volume(video_s3_uri: str, volume_factor: float) -> dict:
    """
    Adjust the volume of a video's audio track.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        volume_factor (float): Volume multiplier (1.0 = no change, 0.5 = half volume, 2.0 = double volume).

    Returns:
        dict: Contains a success message and the S3 URI of the volume-adjusted video.
    """
    return {
        "message": "Volume adjusted successfully",
        "media": "s3://mock-bucket/output/volume_adjusted_video.mp4"
    }


def remove_background_noise(audio_s3_uri: str) -> dict:
    """
    Remove background noise from an audio file.

    Args:
        audio_s3_uri (str): S3 URI of the input audio.

    Returns:
        dict: Contains a success message and the S3 URI of the cleaned audio.
    """
    return {
        "message": "Background noise removed successfully",
        "media": "s3://mock-bucket/output/cleaned_audio.mp3"
    }


def generate_thumbnail(video_s3_uri: str, timestamp: float) -> dict:
    """
    Generate a thumbnail image from a video at a specific timestamp.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        timestamp (float): Time in seconds to capture the thumbnail.

    Returns:
        dict: Contains a success message and the S3 URI of the generated thumbnail.
    """
    return {
        "message": "Thumbnail generated successfully",
        "media": "s3://mock-bucket/output/thumbnail.png"
    }


def add_intro(video_s3_uri: str, intro_clip_s3_uri: str) -> dict:
    """
    Add an intro clip before the main video.

    Args:
        video_s3_uri (str): S3 URI of the main video.
        intro_clip_s3_uri (str): S3 URI of the intro video.

    Returns:
        dict: Contains a success message and the S3 URI of the video with intro added.
    """
    return {
        "message": "Intro added successfully",
        "media": "s3://mock-bucket/output/intro_added_video.mp4"
    }


def add_outro(video_s3_uri: str, outro_clip_s3_uri: str) -> dict:
    """
    Add an outro clip after the main video.

    Args:
        video_s3_uri (str): S3 URI of the main video.
        outro_clip_s3_uri (str): S3 URI of the outro video.

    Returns:
        dict: Contains a success message and the S3 URI of the video with outro added.
    """
    return {
        "message": "Outro added successfully",
        "media": "s3://mock-bucket/output/outro_added_video.mp4"
    }


def export_video(video_s3_uri: str, output_format: str, output_s3_uri: str) -> dict:
    """
    Export a video to a given format and location.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        output_format (str): Desired format (e.g., "mp4", "mov").
        output_s3_uri (str): Destination S3 URI for the exported video.

    Returns:
        dict: Contains a success message and the S3 URI of the exported video.
    """
    return {
        "message": "Video exported successfully",
        "media": f"{output_s3_uri.rstrip('/')}/exported_video.{output_format}"
    }


def change_format(video_s3_uri: str, output_format: str) -> dict:
    """
    Change the format of a video file.

    Args:
        video_s3_uri (str): S3 URI of the input video.
        output_format (str): Desired format (e.g., "mp4", "avi", "mov").

    Returns:
        dict: Contains a success message and the S3 URI of the converted video.
    """
    return {
        "message": "Video format changed successfully",
        "media": f"s3://mock-bucket/output/converted_video.{output_format}"
    }
