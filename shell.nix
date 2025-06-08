{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python310Full
    #pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
  ];
  
  shellHook = ''
    if [ ! -d .venv ]; then
      echo "Creating Python virtual environment..."
      virtualenv .venv
    fi
    source .venv/bin/activate
    echo "Installing mpremote in virtual environment..."
    pip install mpremote
  '';
}
