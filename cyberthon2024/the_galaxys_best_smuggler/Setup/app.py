from flask import Flask, render_template, redirect, url_for, session
import threading
import subprocess
import os
import random

app = Flask(__name__)
app.secret_key = 'Th15_i5_a_s3cr3T'
sem = threading.Semaphore()

PORT_MIN = 1000
PORT_MAX = 10000

ports = []

def remove_ports(game, proxy):
    global ports
    ports.remove(game)
    ports.remove(proxy)

def start_instance(game, proxy):
    subprocess.run(["sh", "./run-compose.sh", f"instance{game}", proxy, game], cwd="/app")
    # Schedule removal of ports after 5 minutes
    threading.Timer(300, remove_ports, args=(game, proxy)).start()

@app.route('/generate', methods=['GET'])
def generate():
    global sem
    sem.acquire()
    global ports

    game, proxy = random.sample(range(PORT_MIN, PORT_MAX), 2)
    while game in ports or proxy in ports:
        game, proxy = random.sample(range(PORT_MIN, PORT_MAX), 2)

    ports.append(game)
    ports.append(proxy)
    game = str(game)
    proxy = str(proxy)

    app.logger.warning(game + " " + proxy)

    thread = threading.Thread(target=start_instance, args=(game, proxy))
    thread.start()
    sem.release()

    session['game'] = game
    session['proxy'] = proxy
    return redirect(url_for('instancer'))

    
@app.route('/', methods=['GET'])
def instancer():
    game = session.get('game')
    proxy = session.get('proxy')
    session.clear()
    return render_template('index.html', game=game, proxy=proxy)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)