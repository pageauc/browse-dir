# browse-dir.py a Flask Media Directory Browser 

### Introduction

I developed this app completely from scratch using only DeepSeek generative AI prompts for the coding. I did add the import from config.py feature myself and the mobile switch. I started this project as an optional replacement for my https://github.com/pageauc/speed-camera and https://github.com/pageauc/pi-timolo2 projects

I called my DeepSeek AI assistant Codey. It was a rewarding and at times frustrating experience. I started from scratch using just prompts and no example starting code.

It is a python3 flask application that allows browsing media files in a web frame.
A directory listing of files/folders is displayed in the Right Frame.
File content Eg images are displayed in the Left Frame. Use up/down arrows or mouse to scroll the listing.
Content will automatically be displayed in the Left Frame.
A folder breadcrumb in the top left corner allows easy navigation to a previous folder.
The frame divider can be repositioned using the mouse <-->. The position will be saved between folders and run sessions.
Use the Right Frame pull down to change the listing sort. This will also be saved between folders.

### Installation

This was developed for a Raspberry Pi but should run on other platforms. You should not need to install any dependencies since flask is
already installed on Bullseye and Bookworm.

Open a terminal or SSH session and clone the github repository.

    cd ~
    git clone https://github.com/pageauc/browse-dir.git
    cd browse-dir
    chmod +x browse-dir.py
	
Edit the config.py settings	
	
	nano config.py
	
Edit the WEB_SERVER_PORT, WEB_SERVER_ROOT, WEB_PAGE_TITLE as required.
The WEB_SERVER_ROOT can be a relative or absolute path to the location of the media.
To exit and save nano changes Press Ctrl-x y  

To launch the web server

    ./browse-dir.py
	
From a browser on your local network paste the flask url eg

    http://192.168.1.178:5010
	
![webserver browser screen shot](browse-dir.png)
	
	

### Credits

Claude Pageau developed this application from scatch using DeepSeek AI over approx three chat sessions.  
I called my assistant Codey. It was a rewarding and at times frustrating experience. I started from scratch using just prompts and no example starting code.


   