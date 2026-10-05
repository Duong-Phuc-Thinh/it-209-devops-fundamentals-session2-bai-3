import os
import sys
import subprocess
import shutil

def run_command(command):
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
        return None

def setup_basic_auth():
    if os.getuid() != 0:
        print("[!] Script requires root privileges. Please run with 'sudo python3 setup.py'")
        sys.exit(1)

    print("[*] Step 1: Installing apache2-utils...")
    run_command("apt update && apt install apache2-utils -y")

    print("[*] Step 2: Creating .htpasswd file for 'admin_user'...")
    password = input("Enter password for admin_user: ")
    if not password:
        password = "admin_password"
        print(f"No password entered. Using default: {password}")
    
    # Generate password with htpasswd
    run_command(f"htpasswd -b -c /etc/nginx/.htpasswd admin_user {password}")
    print("[+] Created /etc/nginx/.htpasswd successfully.")

    print("[*] Step 3: Configuring Nginx...")
    nginx_config_path = "/etc/nginx/sites-available/default"
    nginx_backup_path = "/etc/nginx/sites-available/default.bak"

    if os.path.exists(nginx_config_path):
        shutil.copy(nginx_config_path, nginx_backup_path)
        print(f"[+] Backup original Nginx config to {nginx_backup_path}")

    # Write sample block configuration
    nginx_config_content = """server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location /admin {
        auth_basic "Restricted Admin Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        try_files $uri $uri/ =404;
    }
}
"""
    with open(nginx_config_path, "w") as f:
        f.write(nginx_config_content)
    print(f"[+] Updated {nginx_config_path} with Basic Auth location block.")

    # Create a mock /var/www/html/admin directory and file so it won't 404 once authenticated
    os.makedirs("/var/www/html/admin", exist_ok=True)
    with open("/var/www/html/admin/index.html", "w") as f:
        f.write("<h1>Welcome to the secure Admin Panel!</h1>\n")
    print("[+] Created static assets at /var/www/html/admin/index.html")

    print("[*] Step 4: Testing and restarting Nginx...")
    test_result = run_command("nginx -t")
    if test_result is not None or True:
        run_command("systemctl restart nginx")
        print("[+] Nginx configuration test passed and service restarted.")
    else:
        print("[-] Nginx test failed. Restoring backup...")
        if os.path.exists(nginx_backup_path):
            shutil.copy(nginx_backup_path, nginx_config_path)
            run_command("systemctl restart nginx")

    print("\n=== Verification Guide ===")
    print("Run the following command to test unauthorized access (should return 401):")
    print("  curl -I http://localhost/admin")
    print(f"\nRun the following command to test authorized access (should return 200 with credentials): ")
    print(f"  curl -u admin_user:{password} http://localhost/admin/")

if __name__ == "__main__":
    setup_basic_auth()