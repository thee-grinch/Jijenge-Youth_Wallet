from fabric import Connection, task


page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <style>
        /* Add your CSS styles here */
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 {
            color: #333;
            text-align: center;
        }

        p {
            color: #666;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Website</h1>
        <p>This is a basic HTML landing page.</p>
    </div>

    <script>
        // Add your JavaScript code here
        console.log("Hello, world!");
    </script>
</body>
</html>

'''
conn_kwargs = {
    "host": "18.207.142.2",
    "user": "ubuntu",
    "connect_kwargs": {
        "key_filename": '/home/mordecai/.ssh/id_rsa',
    },
}
my_server_block = '''
server {
    listen 80;
    listen [::]:80;
    server_name www.jijenge.muvandii.tech jijenge.muvandii.tech;
    root /var/jijenge;
    index index.html index.htm index.nginx-debian.html;
    location /app {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

    }
}
'''

@task
def recreate(c):
    conn = Connection(**conn_kwargs)
    # conn.run('sudo rm /etc/nginx/sites-enabled/jijenge')
    # conn.run('sudo rm /etc/nginx/sites-available/jijenge')
    conn.run('sudo touch /etc/nginx/sites-available/jijenge')
    conn.run(f'echo "{my_server_block}" | sudo tee /etc/nginx/sites-available/jijenge')
    conn.run('sudo ln -s /etc/nginx/sites-available/jijenge /etc/nginx/sites-enabled')
    conn.run('sudo nginx -t')
    conn.run('sudo service nginx restart')

@task
def add(c):
    conn = Connection(**conn_kwargs)
    conn.run('sudo mkdir -p /var/jijenge')
    conn.run(f'echo "{page}" | sudo tee /var/jijenge/index.html')
@task
def list(c):
    conn = Connection(**conn_kwargs)
    conn.run('pwd')
    conn.run('ls ~/Jijenge-Youth_Wallet')
    # conn.run('ls /var/jijenge')

@task
def install(c):
    conn = Connection(**conn_kwargs)
    conn.run('sudo apt update')
    conn.run('sudo apt install --upgrade python3')
    conn.run('sudo apt install python3-pip')

@task
def clone(c):
    conn = Connection(**conn_kwargs)
    conn.run('sudo rm -rf Jijenge-Youth_Wallet')
    result = conn.run('git clone https://github.com/thee-grinch/Jijenge-Youth_Wallet.git')
    if result.failed:
        conn.run('git -C Jijenge-Youth_Wallet pull')
    else:
         conn.run('cd Jijenge-Youth_Wallet && cd app && pip install -r requirements.txt && uvicorn app:app --reload')

@task
def check(c):
    conn = Connection(**conn_kwargs)
    conn.run('ps aux | grep uvicorn')
    # conn.run('sudo service nginx restart')
@task
def run(c):
    conn = Connection(**conn_kwargs)
    conn.run('cd Jijenge-Youth_Wallet && cd app && pip3 install -r requirements.txt && uvicorn app:app --reload')
    conn.run('sudo nginx -t')
    conn.run('sudo service nginx restart')

@task
def nginx(c):
    conn = Connection(**conn_kwargs)
    conn.run('sudo apt update')
    conn.run('sudo apt install nginx')

@task
def update(c):
    conn = Connection(**conn_kwargs)
    conn.local('commit "update"')
    conn.run('cd Jijenge-Youth_Wallet && git pull')