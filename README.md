# Simplified Tor Network

A Python-based implementation of a simplified Tor-like network, providing anonymous communication and browsing through a series of relay nodes.

## Overview

The simplified Tor network consists of the following components:

- Client: Manages connections, circuit building, and encryption/decryption of data.
- Directory Server: Maintains a list of available relay nodes and their associated information.
- Relay Nodes: Route encrypted data through the network, providing anonymity.
- User Interface: Allows users to interact with the system.

## Project Structure

The project is organized into the following files and folders:

- `client.py`: Implements the client component, including circuit building, key exchange, and onion routing.
- `directory_server.py`: Implements the directory server component, responsible for maintaining a list of available relay nodes and handling client requests for relay node information.
- `relay_node.py`: Implements the relay node component for entry, middle, and exit nodes, including decryption and forwarding of data.
- `user_interface.py`: Implements the user interface, either as a command-line interface (CLI) or a graphical user interface (GUI), for users to interact with the system.
- `monitoring.py` (optional): Contains code for system monitoring and fault tolerance features.
- `requirements.txt`: Lists the project dependencies, such as `cryptography` and `requests`.
- `docs/`: Contains documentation for the project, including this `README.md` file.

## Installation and Setup

1. Clone this repository to your local machine.

```bash
git clone
```

2. Navigate to the project directory and set up a virtual environment.

   ```
   cd simplified_tor
   python3 -m venv venv
   source venv/bin/activate

   ```

3. Install the required dependencies.

   ```
   pip install -r requirements.txt

   ```

## Usage

1. Run the directory server.

```
python directory_server.py
```

2. Run relay nodes (entry, middle, and exit nodes).

```
python relay_node.py
```

3. Launch the user interface.

```
python user_interface.py
```

4. Interact with the system by inputting URLs and viewing the response in the user interface.
