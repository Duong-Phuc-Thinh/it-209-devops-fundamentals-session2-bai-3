import os
import subprocess
import sys

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        sys.exit(res.returncode)
    print(res.stdout)

def main():
    print("Setting up Nginx Web Server for PTIT DevOps Course...")

    # 1. Update and install nginx
    run_cmd("sudo apt update -y")
    run_cmd("sudo apt install nginx -y")

    # 2. Create web root directory
    web_dir = "/var/www/ptit-web/html"
    run_cmd(f"sudo mkdir -p {web_dir}")

    # 3. Copy index.html
    if os.path.exists("index.html"):
        run_cmd(f"sudo cp index.html {web_dir}/index.html")
    else:
        with open(f"{web_dir}/index.html", "w") as f:
            f.write("<!DOCTYPE html><html><body><h1>Welcome to PTIT DevOps Course - Session 02</h1></body></html>")

    # 4. Set directory permissions
    run_cmd("sudo chmod -R 755 /var/www/ptit-web")

    # 5. Deploy server block config
    conf_dest = "/etc/nginx/sites-available/ptit-web.conf"
    if os.path.exists("ptit-web.conf"):
        run_cmd(f"sudo cp ptit-web.conf {conf_dest}")

    # 6. Create symlink to sites-enabled
    run_cmd(f"sudo ln -sf {conf_dest} /etc/nginx/sites-enabled/")

    # 7. Remove default site to prevent port 80 conflict
    run_cmd("sudo rm -f /etc/nginx/sites-enabled/default")

    # 8. Test configuration syntax
    run_cmd("sudo nginx -t")

    # 9. Reload Nginx service
    run_cmd("sudo systemctl reload nginx")

    print("Nginx Web Server configured successfully!")

if __name__ == "__main__":
    main()
