from flask import Flask, request, jsonify
import supabase
import os
from process_video import process_cricket_video
from config import SUPABASE_URL, SUPABASE_KEY

app = Flask(__name__)

# Connect to Supabase
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        # Get video URL from request
        data = request.get_json()
        video_url = data.get("video_url")

        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400

        # Download video from Supabase Storage
        video_path = "input_video.mp4"
        response = supabase_client.storage.from_("videos").download(video_url)

        with open(video_path, "wb") as f:
            f.write(response)

        # Process the video
        output_video_path = process_cricket_video(video_path)

        # Upload the processed video back to Supabase
        with open(output_video_path, "rb") as f:
            supabase_client.storage.from_("processed_videos").upload("processed_" + video_url, f)

        # Return the processed video URL
        processed_video_url = f"{SUPABASE_URL}/storage/v1/object/public/processed_videos/processed_{video_url}"
        return jsonify({"message": "Processing complete", "processed_video_url": processed_video_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '_main_':
    app.run(debug=True)