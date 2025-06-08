lampada-ines
============

Progetto scolastico.
Una lampada a LED controllabile da remoto.

[Modello 3D](https://www.tinkercad.com/things/bfledCoUZFf-lampada-ines)



## Hardware

- Raspberry Pi Pico 2W
- NeoPixel LED strip (44 LED, GPIO pin 0)

## Caricamento del software

Prima di caricare il software, assicurati di:
1. Entrare nell'ambiente di sviluppo con `nix-shell` (questo installerà automaticamente mpremote)
2. Creare un file `wifi_config.py` con le credenziali WiFi:
   ```python
   SSID = "nome_rete"
   PASSWORD = "password"
   ```
3. (Opzionale) Per accesso remoto, creare un file `duckdns_config.py`:
   ```python
   DOMAIN = "tuo-dominio"  # es. "lampada" per lampada.duckdns.org
   TOKEN = "tuo-token"     # Token da https://www.duckdns.org/
   ```

Per caricare il software sul Raspberry Pi Pico 2W:

```bash
# Entra nell'ambiente di sviluppo
nix-shell

# Collega il Pico 2W al computer tramite USB
# Identifica la porta seriale (solitamente /dev/ttyACM0 su Linux, COMx su Windows)

# Carica i file sul Pico
mpremote connect /dev/ttyACM0 cp *.py :

# In alternativa, se mpremote rileva automaticamente la porta:
mpremote cp *.py :


# Per eseguire il codice immediatamente:
mpremote run main.py

# Per resettare il dispositivo:
mpremote reset
```

## Utilizzo

Una volta caricato il software:
1. Il Pico si connetterà automaticamente alla rete WiFi configurata
2. Accedi all'interfaccia web dal browser:
   - Rete locale: usa l'indirizzo IP mostrato sulla console seriale
   - Accesso remoto (se configurato DuckDNS): `http://tuo-dominio.duckdns.org`
3. Seleziona un colore basato sull'emozione o usa il selettore RGB personalizzato

## Funzionalità

- **Controllo emozioni**: 7 colori predefiniti associati a emozioni (gioia, rabbia, paura, disgusto, tristezza, ansia, noia)
- **Effetto arcobaleno**: Animazione colorata
- **Colore personalizzato**: Selettore RGB per qualsiasi colore
- **Accesso remoto**: Supporto DuckDNS per controllo da internet (opzionale)
- **Aggiornamento automatico IP**: Se configurato, l'IP viene aggiornato ogni 5 minuti su DuckDNS

