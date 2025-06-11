import urequests
import network

class DuckDNSManager:
    def __init__(self):
        self.enabled = False
        self.domain = None
        self.token = None
        
        # Try to load DuckDNS configuration
        try:
            from duckdns_config import DOMAIN, TOKEN
            self.domain = DOMAIN
            self.token = TOKEN
            self.enabled = True
            print("DuckDNS config loaded successfully")
        except ImportError:
            print("DuckDNS config not found - DuckDNS updates disabled")
    
    def update(self, ip_address=None):
        """Update DuckDNS with current IP address"""
        if not self.enabled:
            return False
        
        # If no IP provided, get current IP
        if ip_address is None:
            wlan = network.WLAN(network.STA_IF)
            if not wlan.isconnected():
                print("Not connected to WiFi, skipping DuckDNS update")
                return False
            ip_address = wlan.ifconfig()[0]
        
        try:
            # DuckDNS update URL
            url = f"https://www.duckdns.org/update?domains={self.domain}&token={self.token}&ip={ip_address}"
            
            print(f"Updating DuckDNS domain: {self.domain}.duckdns.org")
            response = urequests.get(url, timeout=20)
            
            # Check if update was successful
            if response.text.strip() == "OK":
                print(f"DuckDNS updated successfully! Access at: http://{self.domain}.duckdns.org")
                response.close()
                return True
            else:
                print(f"DuckDNS update failed: {response.text}")
                response.close()
                return False
                
        except Exception as e:
            print(f"Error updating DuckDNS: {e}")
            return False
    
    def get_url(self):
        """Get the DuckDNS URL if configured"""
        if self.enabled and self.domain:
            return f"http://{self.domain}.duckdns.org"
        return None