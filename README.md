# Minecraft Server Discord Status

[![ci](https://github.com/jyooru/minecraft-server-discord-status/actions/workflows/ci.yml/badge.svg)](https://github.com/jyooru/minecraft-server-discord-status/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/jyooru/minecraft-server-discord-status)](LICENSE)

Updates a Discord message with the status of a Minecraft server.

## Usage

1. Create a new Discord webhook. You can do so by going to the channel you would like to use, pressing `Edit Channel` -> `Integrations` -> `Webhooks` -> `New Webhook` -> `Copy Webhook URL`.
2. Create a new Discord message using the webhook:
   ```sh
   curl -H "Accept: application/json" \
        -H "Content-Type:application/json" \
        -X POST \
        --data "{\"content\": \"temporary\"}" \
        https://discord.com/api/webhooks/.../...
   ```
3. Obtain the message ID. You can do so by hovering over the message, pressing `...` -> `Copy ID`. If the option isn't there, you will need to go to your user settings, and enable `Developer Mode` under `Advanced`.
4. Run the service...

   - using your terminal:
     ```sh
     msds --message-id 1234 --server-host example.com --webhook https://discord.com/api/webhooks/.../...
     ```
   - using Docker:
     ```sh
     docker build . -t msds
     docker run --rm -it msds --message-id 1234 --server-host example.com --webhook https://discord.com/api/webhooks/.../...
     ```
   - using Docker Compose:

     ```yml
     version: "3"

     services:
       status:
         build: .
         environment:
           - MESSAGE_ID=1234
           - SERVER_HOST=example.com
           - WEBHOOK=https://discord.com/api/webhooks/.../...
     ```

## License

See [LICENSE](LICENSE) for details.
