{
  description = "Updates a Discord message with the status of a Minecraft server";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = { self, nixpkgs, utils, ... } @ inputs:
    utils.lib.mkFlake {
      inherit self inputs;

      outputsBuilder = channels:
        let
          pkgs = channels.nixpkgs;
          overlay = self.overlay pkgs pkgs;
        in
        with pkgs;
        rec {
          defaultPackage = overlay.minecraft-server-discord-status;

          devShell = (poetry2nix.mkPoetryEnv { projectDir = ./.; }).env;

          packages = with overlay; {
            inherit minecraft-server-discord-status;
            docker = minecraft-server-discord-status-docker;
          };
        };

      overlay = final: prev: rec {
        minecraft-server-discord-status-docker = final.dockerTools.streamLayeredImage {
          name = "minecraft-server-discord-status";
          config.Entrypoint = [ "${minecraft-server-discord-status}/bin/msds" ];
        };

        minecraft-server-discord-status = final.poetry2nix.mkPoetryApplication { projectDir = ./.; };
      };
    };
}
