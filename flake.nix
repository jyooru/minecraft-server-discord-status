{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = { self, nixpkgs, utils } @ inputs:
    utils.lib.mkFlake {
      inherit self inputs;

      outputsBuilder = channels:
        let pkgs = channels.nixpkgs; in
        with pkgs;
        rec {
          devShells = rec {
            default = minecraft-server-discord-status;
            minecraft-server-discord-status = (poetry2nix.mkPoetryEnv { projectDir = ./.; }).env;
          };

          packages = (self.overlays.default pkgs pkgs) // {
            default = packages.minecraft-server-discord-status;
          };
        };

      overlays = rec {
        default = minecraft-server-discord-status;
        minecraft-server-discord-status = final: prev: {
          minecraft-server-discord-status = final.poetry2nix.mkPoetryApplication { projectDir = ./.; };
        };
      };
    };
}
