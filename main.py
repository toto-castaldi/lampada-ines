import network
import socket
import machine
import neopixel
import time
import json

# Import WiFi credentials from configuration file
from wifi_config import SSID, PASSWORD

LED_PIN = 0
NUM_LEDS = 44
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# INTERNAL LED
led = machine.Pin("LED", machine.Pin.OUT)

def connect_wifi():
    """WIFI CONNECTION"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("connection...")
    while not wlan.isconnected():
        led.toggle()
        time.sleep(0.1)
    
    led.on()  # INTERNAL LED ON WHEN CONNECTED
    print(f"Connected! IP: {wlan.ifconfig()[0]}")
    return wlan.ifconfig()[0]

def clear_strip():
    np.fill((0, 0, 0))
    np.write()

def set_color(r, g, b):
    np.fill((r, g, b))
    np.write()

def rainbow_effect():
    for j in range(10): 
        for i in range(NUM_LEDS):
            pixel_index = (i * 256 // NUM_LEDS) + j * 25
            color = wheel(pixel_index & 255)
            np[i] = color
        np.write()
        time.sleep(0.05)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def web_page():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>I colori delle emozioni</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; text-align: center; background-color: #1e1e1e; color: white; }
        .container { max-width: 400px; margin: 0 auto; padding: 20px; }
        button { 
            background-color: #4CAF50; 
            border: none; 
            color: white; 
            padding: 15px 32px; 
            margin: 10px;
            font-size: 16px; 
            border-radius: 8px;
            cursor: pointer;
            width: 150px;
            transition: filter 0.2s;
        }
        button:hover {
            filter: brightness(0.85);
        }
        .gioia { background-color: #F5CC16; }
        .rabbia { background-color: #F22E02; }
        .paura { background-color: #E599F2; }
        .disgusto { background-color: #CEDB16; }
        .tristezza { background-color: #0748B8; }
        .ansia { background-color: #F28A02; }
        .noia { background-color: #7F00BA; }
        .rainbow { background: linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #00ff00, #0080ff, #8000ff); }
        .off { background-color: #555; }
        input[type="color"] { width: 60px; height: 40px; border: none; border-radius: 5px; margin: 10px; }
        .color-section { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>I colori delle emozioni</h1>
        <p><button onclick="sendCommand('gioia')" class="gioia">Gioia</button></p>
        <p><button onclick="sendCommand('rabbia')" class="rabbia">Rabbia</button></p>
        <p><button onclick="sendCommand('paura')" class="paura">Paura</button></p>
        <p><button onclick="sendCommand('disgusto')" class="disgusto">Disgusto</button></p>
        <p><button onclick="sendCommand('tristezza')" class="tristezza">Tristezza</button></p>
        <p><button onclick="sendCommand('ansia')" class="ansia">Ansia</button></p>
        <p><button onclick="sendCommand('noia')" class="noia">Noia</button></p>

        <button onclick="sendCommand('rainbow')" class="rainbow">Arcobaleno</button>
        <button onclick="sendCommand('off')" class="off">Spegni</button>
        
        <div class="color-section">
            <h2>Colore Personalizzato</h2>
            <input type="color" id="colorPicker" value="#ff0000">
            <button onclick="sendCustomColor()">Applica</button>
        </div>
    </div>
    
    <script>
        function sendCommand(cmd) {
            fetch('/' + cmd);
        }
        
        function sendCustomColor() {
            const color = document.getElementById('colorPicker').value;
            const r = parseInt(color.substr(1,2), 16);
            const g = parseInt(color.substr(3,2), 16);
            const b = parseInt(color.substr(5,2), 16);
            fetch(`/custom?r=${r}&g=${g}&b=${b}`);
        }
    </script>
</body>
</html>"""
    return html

def handle_request(conn, request):
    """Gestisce le richieste web"""
    try:
        request = request.decode('utf-8')
        
        if 'GET /' in request:
            if 'GET /gioia' in request:
                set_color(245, 204, 22)
                response = "OK"            
            elif 'GET /rabbia' in request:
                set_color(242, 46, 2)
                response = "OK"
            elif 'GET /paura' in request:
                set_color(229, 153, 242)
                response = "OK"
            elif 'GET /disgusto' in request:
                set_color(22, 184, 7)
                response = "OK"
            elif 'GET /tristezza' in request:
                set_color(7, 72, 184)
                response = "OK"
            elif 'GET /ansia' in request:
                set_color(242, 138, 2)
                response = "OK"
            elif 'GET /noia' in request:
                set_color(127, 0, 186)
                response = "OK"
            elif 'GET /rainbow' in request:
                rainbow_effect()
                response = "OK"
            elif 'GET /off' in request:
                clear_strip()
                response = "OK"
            elif 'GET /custom' in request:
                try:
                    query = request.split('?')[1].split(' ')[0]
                    params = {}
                    for param in query.split('&'):
                        key, value = param.split('=')
                        params[key] = int(value)
                    set_color(params['r'], params['g'], params['b'])
                    response = "OK"
                except:
                    response = "Error"
            else:
                response = web_page()
        else:
            response = "Not Found"
        
        if response == "OK" or response == "Error":
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/plain\n')
            conn.send('Connection: close\n\n')
            conn.send(response)
        else:
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.send(response)
            
    except Exception as e:
        print(f"Error: {e}")

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    
    print("Server UP on port 80")
    
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connected from {addr}")
            request = conn.recv(1024)
            handle_request(conn, request)
            conn.close()
        except Exception as e:
            print(f"Server error: {e}")
            conn.close()

def main():
    try:
        clear_strip()
        
        ip = connect_wifi()
        
        start_server()
        
    except KeyboardInterrupt:
        clear_strip()
        print("\nServer stop")
    except Exception as e:
        clear_strip()
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
