CREATE = """
CREATE TABLE IF NOT EXISTS videos (
    video_id TEXT PRIMARY KEY,
    timestamp STRING,
    original_name TEXT,
    total_frames INTEGER,
    detected_frames INTEGER,
    percent REAL
)
"""

UPDATE = "UPDATE videos SET total_frames=?, detected_frames=?, percent=? WHERE video_id=?"

UPLOAD_VIDEO = """
INSERT INTO videos (video_id, timestamp, original_name, total_frames, detected_frames, percent)
VALUES (?, ?, ?, 0, 0, 0.0)
"""

SELECT_VIDEO = """
SELECT original_name, timestamp, total_frames, detected_frames, percent
FROM videos WHERE video_id = ?
"""

SELECT_ALL = """
SELECT original_name, timestamp, total_frames, detected_frames, percent
FROM videos
ORDER BY timestamp DESC
"""