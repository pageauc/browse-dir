#!/usr/bin/python3
import os
import sys
import subprocess
from flask import Flask, render_template, send_from_directory, abort, request, make_response, url_for
from datetime import datetime
# from werkzeug.utils import secure_filename

try:
    from config import WEB_SERVER_PORT, WEB_SERVER_ROOT, WEB_PAGE_TITLE, WEB_MOBILE_ON
except ImportError as e:
    print(f"ERROR : Import Failed {str(e)}")
    sys.exit(1)

if WEB_MOBILE_ON:
    target_html = 'browse-dir-mobile.html'
else:
    target_html = 'browse-dir.html'
    
web_media_path = os.path.abspath(WEB_SERVER_ROOT)

app = Flask(__name__)

# ===== SECURITY CONFIG =====
WEB_SECURITY_HIGH = False  # Toggle for production

# ===== APP CONFIG =====
app.config.update({
    'EXTERNAL_DIR': web_media_path,  # Absolute path for safety
    'PAGE_TITLE': WEB_PAGE_TITLE,
    'IMG_BIGGER': 1.5,
    'CACHE_TIMEOUT': 3600,
    'SECRET_KEY': 'your-secure-key-here'  # Change for production!
})

if WEB_SECURITY_HIGH:
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# ===== UTILITIES =====
def get_disk_status():
    """Returns storage information for the media directory"""
    try:
        result = subprocess.run(["df", "-h", app.config['EXTERNAL_DIR']],
                              capture_output=True, text=True)
        parts = result.stdout.split("\n")[1].split()
        return f"Storage: {parts[4]} used ({parts[2]}/{parts[1]}) | Free: {parts[3]}"
    except Exception as e:
        app.logger.error(f"Disk status error: {str(e)}")
        return "Storage info unavailable"

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return datetime.fromtimestamp(value).strftime(format)

def validate_media_path(path):
    """Securely validate paths within EXTERNAL_DIR"""
    abs_path = os.path.abspath(os.path.join(app.config['EXTERNAL_DIR'], path))
    if not abs_path.startswith(app.config['EXTERNAL_DIR']):
        abort(403, "Access denied")
    return abs_path

# ===== ROUTES =====
@app.route('/')
def index():
    return browse()

@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    # Calculate parent path before validation
    parent_path = '/'.join(subpath.split('/')[:-1]) if subpath else None

    try:
        abs_path = validate_media_path(subpath)

        if not os.path.exists(abs_path):
            abort(404)
        if not os.path.isdir(abs_path):
            abort(400, "Not a directory")

        # Get sort preference
        sort_option = request.cookies.get('sort_preference', 'date_desc')
        sort_key, reverse = {
            'date_desc': ('create_time', True),
            'date_asc': ('create_time', False),
            'name_asc': ('name', False),
            'name_desc': ('name', True)
        }.get(sort_option, ('create_time', True))

        # Build directory listing
        items = []
        for item in os.listdir(abs_path):
            try:
                item_path = os.path.join(abs_path, item)
                stat = os.stat(item_path)
                items.append({
                    'name': item,
                    'rel_path': os.path.join(subpath, item) if subpath else item,
                    'path': os.path.join(subpath, item),  # For backward compatibility
                    'is_file': os.path.isfile(item_path),
                    'mod_time': stat.st_mtime,
                    'create_time': stat.st_ctime,
                    'size': stat.st_size
                })
            except OSError as e:
                app.logger.warning(f"Skipping {item}: {str(e)}")

        # Sort items
        items.sort(key=lambda x: x[sort_key], reverse=reverse)

        return render_template(
            target_html,
            items=items,
            current_path=subpath,
            parent_path=parent_path,  # Passed to template
            page_title=app.config['PAGE_TITLE'],
            img_bigger=app.config['IMG_BIGGER'],
            footer_info=get_disk_status(),
            current_sort=sort_option
        )

    except Exception as e:
        app.logger.error(f"Browse error: {str(e)}")
        abort(500)

@app.route('/files/<path:filename>')
def files(filename):
    try:
        abs_path = validate_media_path(filename)
        if not os.path.exists(abs_path):
            abort(404)
        return send_from_directory(
            app.config['EXTERNAL_DIR'],
            filename,
            conditional=True
        )
    except Exception as e:
        app.logger.error(f"File serve error: {str(e)}")
        abort(500)

if __name__ == '__main__':
    print(f"Media directory: {app.config['EXTERNAL_DIR']}")
    print(f"Security mode: {'HIGH' if WEB_SECURITY_HIGH else 'LOW'}")
    app.run(host="0.0.0.0", port=WEB_SERVER_PORT, debug=not WEB_SECURITY_HIGH)