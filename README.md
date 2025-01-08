When on Nixos:

echo use flake >>.envrc  
direnv allow  
nix develop  
code .  

else
uv sync
code .
