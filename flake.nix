{
  description = "QClip dev flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
    python = pkgs.python312;
    flaskEnv = python.withPackages (ps:
      with ps; [
        flask
        flask-sqlalchemy
        flask-migrate
        flask-bcrypt
        flask-login
        flask-wtf
        email_validator
        python-magic
        gunicorn
        pytest
        pytest-cov
      ]);

    # Flask start script
    flaskApp = pkgs.writeShellScriptBin "start-qclip" ''
      export $(grep -v '^#' .env | sed 's/#.*//' | xargs)
      exec ${flaskEnv}/bin/gunicorn --config gunicorn-cfg.py run:app
    '';
  in {
    # Interactive shell
    devShell.${system} = pkgs.mkShell {
      buildInputs = [flaskEnv];
      shellHook = ''
        echo "QClip dev environment started."
      '';
    };

    # Flask app as shell script
    packages.${system}.default = flaskApp;
  };
}
