import network
import time
import machine

class WiFiManager:
    def __init__(self, led_pin="LED"):
        self.led = machine.Pin(led_pin, machine.Pin.OUT)
        self.hotspot_mode = False
        self.ap_ssid = "LampadaInesConfig"
        self.ap_password = "12345678"
        self.connection_timeout = 30
        self.ip_address = None
        
    def connect(self):
        """Try to connect to WiFi, fallback to hotspot mode if timeout"""
        try:
            # Import WiFi credentials
            from wifi_config import SSID, PASSWORD
            
            # Try normal WiFi connection
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(SSID, PASSWORD)
            
            print("Connecting to WiFi...")
            start_time = time.time()
            
            while not wlan.isconnected():
                self.led.toggle()
                time.sleep(0.1)
                
                # Check timeout
                if time.time() - start_time > self.connection_timeout:
                    print("WiFi connection timeout! Starting hotspot mode...")
                    wlan.active(False)
                    self.hotspot_mode = True
                    return self.start_hotspot()
            
            # Connected successfully
            self.led.on()
            self.ip_address = wlan.ifconfig()[0]
            print(f"Connected! IP: {self.ip_address}")
            return self.ip_address
            
        except ImportError:
            print("WiFi config not found! Starting hotspot mode...")
            self.hotspot_mode = True
            return self.start_hotspot()
    
    def start_hotspot(self):
        """Start Access Point mode for configuration"""
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=self.ap_ssid, password=self.ap_password)
        
        # Wait for AP to be active
        time.sleep(2)
        
        self.ip_address = ap.ifconfig()[0]
        print(f"Hotspot mode active!")
        print(f"SSID: {self.ap_ssid}")
        print(f"Password: {self.ap_password}")
        print(f"Connect to http://{self.ip_address} to configure")
        
        # Blink LED pattern to indicate hotspot mode
        for _ in range(10):
            self.led.on()
            time.sleep(0.1)
            self.led.off()
            time.sleep(0.1)
        self.led.on()
        
        return self.ip_address
    
    def save_wifi_config(self, ssid, password):
        """Save WiFi configuration to file"""
        try:
            with open('wifi_config.py', 'w') as f:
                f.write(f'SSID = "{ssid}"\n')
                f.write(f'PASSWORD = "{password}"\n')
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_config_page(self):
        """Return HTML configuration page"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Lampada Ines - Configurazione</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; text-align: center; background-color: #1e1e1e; color: white; padding: 20px; }
        .container { max-width: 400px; margin: 0 auto; }
        input[type="text"], input[type="password"] { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            box-sizing: border-box;
            background-color: #333;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
        }
        button { 
            background-color: #4CAF50; 
            border: none; 
            color: white; 
            padding: 15px 32px; 
            margin: 20px 0;
            font-size: 16px; 
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
        }
        button:hover { filter: brightness(0.85); }
        .message { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background-color: #4CAF50; }
        .error { background-color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Configurazione WiFi</h1>
        <form action="/save_config" method="get">
            <label for="ssid">Nome rete WiFi (SSID):</label>
            <input type="text" id="ssid" name="ssid" required>
            
            <label for="password">Password WiFi:</label>
            <input type="password" id="password" name="password" required>
            
            <button type="submit">Salva e Riavvia</button>
        </form>
        
        <p style="font-size: 14px; color: #888;">
            Dopo aver salvato la configurazione, il dispositivo si riavviera' 
            e tenterà di connettersi alla rete WiFi specificata.
        </p>
    </div>
</body>
</html>"""
    
    def get_success_page(self):
        """Return success page after saving configuration"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Configurazione Salvata</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; text-align: center; background-color: #1e1e1e; color: white; padding: 20px; }
        .container { max-width: 400px; margin: 0 auto; }
        .success { background-color: #4CAF50; padding: 20px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">
            <h2>Configurazione Salvata!</h2>
            <p>Il dispositivo si riavviera' tra 3 secondi...</p>
        </div>
    </div>
    <script>
        setTimeout(() => {
            fetch('/reboot');
        }, 3000);
    </script>
</body>
</html>"""
    
    def handle_config_request(self, request):
        """Handle configuration requests in hotspot mode"""
        if 'GET /save_config' in request:
            try:
                # Extract parameters from URL
                query_start = request.find('?') + 1
                query_end = request.find(' ', query_start)
                query = request[query_start:query_end]
                
                params = {}
                for param in query.split('&'):
                    key, value = param.split('=')
                    # URL decode the values
                    value = value.replace('%20', ' ').replace('+', ' ')
                    value = value.replace('%21', '!').replace('%40', '@')
                    value = value.replace('%23', '#').replace('%24', '$')
                    params[key] = value
                
                # Save configuration
                if self.save_wifi_config(params['ssid'], params['password']):
                    return self.get_success_page(), 'html'
                else:
                    return "Configuration save failed", 'text'
            except Exception as e:
                print(f"Config error: {e}")
                return "Error parsing configuration", 'text'
                
        elif 'GET /reboot' in request:
            return "reboot", 'reboot'
        else:
            return self.get_config_page(), 'html'