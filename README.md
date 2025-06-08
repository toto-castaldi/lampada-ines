lampada-ines
============

Progetto scolastico.
Una lampada a LED controllabile da remoto.

## Hardware

- Raspberry Pi Pico 2W
- NeoPixel LED strip (44 LED, GPIO pin 0)

## Caricamento del software

Prima di caricare il software, assicurati di:
1. Entrare nell'ambiente di sviluppo con `nix-shell` (questo installerà automaticamente mpremote)
2. Creare un file `wifi_config.py` con le credenziali WiFi:
   ```python
   WIFI_SSID = "nome_rete"
   WIFI_PASSWORD = "password"
   ```

Per caricare il software sul Raspberry Pi Pico 2W:

```bash
# Entra nell'ambiente di sviluppo
nix-shell

# Collega il Pico 2W al computer tramite USB
# Identifica la porta seriale (solitamente /dev/ttyACM0 su Linux, COMx su Windows)

# Carica i file sul Pico
mpremote connect /dev/ttyACM0 cp main.py wifi_config.py :

# In alternativa, se mpremote rileva automaticamente la porta:
mpremote cp main.py wifi_config.py :

# Per eseguire il codice immediatamente:
mpremote run main.py

# Per resettare il dispositivo:
mpremote reset
```

## Utilizzo

Una volta caricato il software:
1. Il Pico si connetterà automaticamente alla rete WiFi configurata
2. Accedi all'interfaccia web dal browser all'indirizzo IP mostrato sulla console seriale
3. Seleziona un colore basato sull'emozione o usa il selettore RGB personalizzato

