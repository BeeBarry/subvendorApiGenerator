let
  pkgs = import <nixpkgs> {config.allowUnfree = true;};
  nixpkgs-python = import (fetchTarball "https://github.com/cachix/nixpkgs-python/archive/refs/heads/main.zip");

  python-env = (nixpkgs-python.packages.${pkgs.system}."3.11").withPackages (pp:
    with pp; [
      pip
      wheel
      cython
    ]);
in
  pkgs.mkShell {
    packages = with pkgs; [
      vscode
      azure-cli
      azure-functions-core-tools
      bicep
      terraform
      powershell
      terraform-ls
      terraform-lsp
      basedpyright
    ];

    buildInputs = [
      python-env
    ];

    shellHook = ''
      PYTHON_BIN=${python-env}/bin/python
      [[ -d .venv ]] || $PYTHON_BIN -m venv .venv
      source .venv/bin/activate
      .venv/bin/pip install -r requirements.txt
      .venv/bin/python --version
    '';
  }
