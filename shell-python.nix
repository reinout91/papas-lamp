# python-shell.nix

{ pkgs ? import <nixpkgs> {}, extraBuildInputs ? [], myPython ? pkgs.python3, extraLibPackages ? [], pythonWithPkgs? myPython }:

let
  buildInputs  = with pkgs; [
    clang
    llvmPackages_16.bintools
    rustup
    # stdenvNoCC
    # stdenvNoLibs
    # stdenv_32bit
    # gccStdenv
    # gccStdenvNoLibs
    # libcxxStdenv
    # gccMultiStdenv
  ] ++ extraBuildInputs;

  lib-path = with pkgs; lib.makeLibraryPath buildInputs;

  shell = pkgs.mkShell {
    buildInputs = [
     # my python and packages
      pythonWithPkgs

      # other packages needed for compiling python libs
      pkgs.readline
      pkgs.libffi
      pkgs.openssl

      pkgs.git
      pkgs.openssh
      pkgs.rsync
      pkgs.cowsay
      pkgs.lolcat
      pkgs.nix-index

      # unfortunately needed because of messing with LD_LIBRARY_PATH below
      pkgs.gcc
      pkgs.stdenv
      # pkgs.stdenv-linux
      pkgs.stdenvNoCC
      pkgs.stdenvNoLibs
      pkgs.stdenv_32bit
      pkgs.gccStdenv
      pkgs.gccStdenvNoLibs
      pkgs.libcxxStdenv
      pkgs.gccMultiStdenv
  ] ++ extraBuildInputs;

  GREETING = "Entering papas lamp development shell!";

  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)

    # Augment the dynamic linker path
    export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"

    # https://discourse.nixos.org/t/what-package-provides-libstdc-so-6/18707/4
    # fixes libstdc++ issues and libgl.so issues
    LD_LIBRARY_PATH=lib.makeLibraryPath [ pkgs.stdenv.cc.cc ];

    # Setup the virtual environment if it doesn't already exist.
    VENV=shell-papas-lamp

    if test ! -d $VENV; then
      virtualenv $VENV
    fi

    source ./$VENV/bin/activate
    export PYTHONPATH=$PYTHONPATH:`pwd`/$VENV/${myPython.sitePackages}/
    pip install --upgrade pip
    pip install build123d ocp-vscode cadquery numpy
    echo $GREETING | cowsay | lolcat
    '';
  };

in
  shell
