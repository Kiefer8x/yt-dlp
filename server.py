from flask import Flask, request, jsonify, render_template
import subprocess
import json
import sys
import re
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__, static_folder='.', static_url_path='', template_folder='.')

# Run the local yt_dlp module using the current python interpreter, bypassing SSL checks
YT_DLP_CMD = [sys.executable, "-m", "yt_dlp", "--no-check-certificate"]

# Download Queue State
tasks = {}
executor = ThreadPoolExecutor(max_workers=5)

def run_download(task_id, cmd):
    tasks[task_id]['status'] = 'Downloading'
    try:
        # We add --newline to ensure we get line-by-line output for parsing
        if '--newline' not in cmd:
            cmd.append('--newline')
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            # Keep the last 50 log lines to avoid memory leaks but retain error context
            tasks[task_id]['log'].append(line)
            if len(tasks[task_id]['log']) > 50:
                tasks[task_id]['log'].pop(0)
            
            # Parse progress percentage
            if '[download]' in line and '%' in line:
                pct_match = re.search(r'([0-9.]+)%', line)
                if pct_match:
                    tasks[task_id]['progress'] = float(pct_match.group(1))
                
                spd_match = re.search(r'at\s+([0-9.a-zA-Z/]+)', line)
                if spd_match:
                    tasks[task_id]['speed'] = spd_match.group(1)
                    
                eta_match = re.search(r'ETA\s+([0-9:]+)', line)
                if eta_match:
                    tasks[task_id]['eta'] = eta_match.group(1)

            # Catch ffmpeg missing error and alert the UI
            if 'ffmpeg is not installed' in line.lower():
                tasks[task_id]['log'].append("CRITICAL: FFMPEG is missing! Audio & Video will not merge. Please install ffmpeg.")

        process.wait()
        if process.returncode == 0:
            tasks[task_id]['status'] = 'Completed'
            tasks[task_id]['progress'] = 100.0
        else:
            tasks[task_id]['status'] = 'Error'
    except Exception as e:
        tasks[task_id]['status'] = 'Error'
        tasks[task_id]['log'].append(str(e))

# Force allow Cross-Origin requests to prevent "Failed to fetch" errors
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/discover', methods=['POST', 'OPTIONS'])
def discover():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        cmd = YT_DLP_CMD + ['-j', '--no-playlist', url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        info = json.loads(result.stdout)
        formats = info.get('formats', [])
        
        found_res = set()
        available_video_containers = set()
        available_video_codecs = set()
        available_audio_formats = set()
        
        for f in formats:
            # 1. Resolutions & Framerates
            height = f.get('height')
            fps = f.get('fps')
            if height and isinstance(height, (int, float)):
                fps_val = round(fps) if fps else 30
                found_res.add((int(height), fps_val))
            
            ext = f.get('ext')
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')

            # 2. Video Formats & Codecs (Only if it has video)
            if vcodec != 'none':
                if ext: available_video_containers.add(ext)
                if vcodec:
                    base_vc = vcodec.split('.')[0]
                    if 'av01' in base_vc: base_vc = 'av1'
                    elif 'hev' in base_vc or 'h265' in base_vc: base_vc = 'h265'
                    elif 'avc' in base_vc or 'h264' in base_vc: base_vc = 'h264'
                    available_video_codecs.add(base_vc)

            # 3. Audio Formats (If it contains audio)
            if acodec != 'none':
                if ext: available_audio_formats.add(ext)

        # Base standard resolutions to always show
        standard_res = {(4320, 60), (4320, 30), (2160, 60), (2160, 30), (1440, 60), (1440, 30), 
                        (1080, 60), (1080, 30), (720, 60), (720, 30), (480, 30), (360, 30), (240, 30), (144, 30)}
        
        all_res_tuples = sorted(list(standard_res.union(found_res)), key=lambda x: (x[0], x[1]), reverse=True)
        
        def format_res(h, f):
            name = f"{h}p"
            if h >= 4320: name = "8K"
            elif h >= 2160: name = "4K"
            if f > 30: name += f"{f}fps"
            return name

        all_resolutions = [format_res(h, f) for h, f in all_res_tuples]
        available_resolutions = [format_res(h, f) for h, f in found_res]

        all_v_exts = sorted(list({'mp4', 'webm', 'mkv', 'flv', 'avi', 'mov'}.union(available_video_containers)))
        all_v_codecs = sorted(list({'av1', 'h265', 'h264', 'vp9', 'vp8'}.union(available_video_codecs)))
        all_a_exts = sorted(list({'m4a', 'aac', 'mp3', 'ogg', 'opus', 'flac', 'wav'}.union(available_audio_formats)))

        return jsonify({
            'allResolutions': all_resolutions,
            'availableResolutions': available_resolutions,
            'allVideoContainers': all_v_exts,
            'availableVideoContainers': list(available_video_containers),
            'allVideoCodecs': all_v_codecs,
            'availableVideoCodecs': list(available_video_codecs),
            'allAudioFormats': all_a_exts,
            'availableAudioFormats': list(available_audio_formats),
            'title': info.get('title', 'Unknown Title')
        })

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return jsonify({'error': f'yt-dlp error: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download', methods=['POST', 'OPTIONS'])
def download():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    title = data.get('title', 'Unknown Video')
    resolutions = data.get('resolutions', [])
    video_containers = data.get('videoContainers', [])
    video_codecs = data.get('videoCodecs', [])
    audio_formats = data.get('audioFormats', [])
    extras = data.get('extras', {})

    cmd = YT_DLP_CMD + ['--no-colors'] # Strip terminal colors for clean web logs

    if extras.get('playlist'):
        cmd.append('--yes-playlist')
    else:
        cmd.append('--no-playlist')
        
    if extras.get('embedSubs'):
        cmd.extend(['--write-subs', '--embed-subs'])
    if extras.get('embedMetadata'):
        cmd.append('--embed-metadata')
    if extras.get('embedThumbnail'):
        cmd.append('--embed-thumbnail')
    if extras.get('splitChapters'):
        cmd.append('--split-chapters')

    if extras.get('audioOnly'):
        cmd.append('-x')
        if audio_formats:
            cmd.extend(['--audio-format', audio_formats[0]])
        cmd.extend(['-f', 'bestaudio/best'])
    else:
        sort_prefs = []
        if resolutions:
            max_res = 0
            max_fps = 0
            for r in resolutions:
                h = 0
                if '8K' in r: h = 4320
                elif '4K' in r: h = 2160
                else:
                    m = re.search(r'(\d+)p', r)
                    if m: h = int(m.group(1))
                
                fps_m = re.search(r'(\d+)fps', r)
                f = int(fps_m.group(1)) if fps_m else 30
                
                if h > max_res:
                    max_res, max_fps = h, f
                elif h == max_res and f > max_fps:
                    max_fps = f
                    
            if max_res > 0:
                sort_prefs.append(f'res:{max_res}')
                if max_fps > 30:
                    sort_prefs.append(f'fps:{max_fps}')
                
        if video_codecs:
            sort_prefs.append(f'vcodec:{video_codecs[0]}')
        if video_containers:
            sort_prefs.append(f'ext:{video_containers[0]}')
            # Force yt-dlp to merge the audio and video into the selected container
            cmd.extend(['--merge-output-format', video_containers[0]])
            
        if audio_formats:
            sort_prefs.append(f'aext:{audio_formats[0]}')
            
        if sort_prefs:
            cmd.extend(['-S', ','.join(sort_prefs)])
            
        cmd.extend(['-f', 'bestvideo*+bestaudio/best'])

    cmd.append(url)

    # Generate unique ID and add to queue
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        'id': task_id,
        'title': title,
        'url': url,
        'status': 'Queued',
        'progress': 0.0,
        'speed': '0MiB/s',
        'eta': '--:--',
        'log': []
    }
    
    # Submit to the thread pool (Max 5 concurrent)
    executor.submit(run_download, task_id, cmd)
    
    return jsonify({'status': 'Success', 'task_id': task_id, 'message': 'Added to queue'})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True, port=5001)