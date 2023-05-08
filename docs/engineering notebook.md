# Brain storming

Design Decisions for the Simplified Tor Network

1. Hardcoded relay nodes: For this simpler version, we decided to use 5 hardcoded machines (1 client, 1 server, and 3 relay nodes). This decision simplifies the initial setup and reduces complexity in the early stages of development.
2. gRPC for communication: gRPC was chosen as the communication framework to facilitate connections between the clients, relay nodes, and the directory server. gRPC offers efficient, language-agnostic communication, allowing us to easily extend our project and implement additional services if needed.
3. Protocol Buffers for service definition: we used Protocol Buffers to define the gRPC services and their methods. This provides a clear, structured format for defining services and messages, making it easy to understand and maintain.
4. Basic circuit building: In this simplified version, the client requests a circuit from the directory server and receives a list of relay nodes to use. This basic approach allows us to focus on core functionality before implementing more advanced features, such as dynamic circuit selection or load balancing.
5. Single SendMessage method for clients: The client sends messages through the Tor network using a single SendMessage method. This simplifies the initial implementation while still demonstrating the core functionality of encrypted communication through the network.
6. Terminal tool instead of a user interface: A simple terminal tool was implemented for user interaction, rather than a graphical user interface. This decision reduces complexity and allows us to focus on the core functionality of the simplified Tor network.

Installing gRPC and a brief description of the .proto file:

1. To install gRPC and its required tools, run the following command:

```
./install_package.sh grpcio grpcio-tools
```

2. The `tor.proto` file is a Protocol Buffers file that defines the gRPC services and messages for the simplified Tor network. It includes three services:
   * `Client`: Methods for requesting a circuit and sending messages through the network.
   * `Rresponse.responseelay`: A method for processing encrypted messages at each relay node.
   * `DirectoryServer`: A method for clients to retrieve a list of available relay nodes.

The `.proto` file also defines message types for requests and responses, as well as an enum for node types (entry, middle, and exit). By using Protocol Buffers, the gRPC services are clearly defined, making it easy to understand their functionality and structure.

To create the required files from the grpc use the command

```
cd
```
