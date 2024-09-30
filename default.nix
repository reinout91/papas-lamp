# shell-build123d.nix

# Shell environment for build123d
# https://build123d.readthedocs.io/en/latest/index.html

# https://wiki.nixos.org/wiki/Python#Using_nix-shell_alongside_pip

{ pkgs ? import <nixpkgs> {} }:

let
  myPython = pkgs.python311;
  pythonPackages = pkgs.python311Packages;

  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    # This list contains tools for Python development.
    # You can also add other tools, like black.
    #
    # Note that even if you add Python packages here like PyTorch or Tensorflow,
    # they will be reinstalled when running `pip -r requirements.txt` because
    # virtualenv is used below in the shellHook.
    ipython
    pip
    setuptools
    virtualenvwrapper
    wheel
    black
    # https://discourse.nixos.org/t/what-package-provides-libstdc-so-6/18707/3
    stdenv
  ]);

  extraBuildInputs = with pkgs; [
    # this list contains packages that you want to be available at runtime and might not be able to be installed properly via pip
    pythonPackages.pandas
    pythonPackages.stdenv
    pythonPackages.requests
    stdenv.cc.cc.lib
    gcc
    expat
    libGL
    xorg.libX11
    zlib
  ];

in
  import ./shell-python.nix {
    extraBuildInputs=extraBuildInputs;
    # extraLibPackages=extraLibPackages;
    myPython=myPython;
    pythonWithPkgs=pythonWithPkgs;
  }
