# AES-over-LAN
*CS-1340 Final Project*

**Description:**
- In this project, we will implement a simple AES encryption/ decryption application using socket programming.
- Upon establishing server and client connection, client can choose to encrypt/ decrypt a message.
- Client then sends the plaintext (or ciphertext) and a valid 16 byte key to the server
- Server performs the encryption (or decryption) and sends the resulting ciphertext (or plaintext) to client
- Client displays the result and disconnects

**Usage:** <br/>
In order to run the project, the user can do one of 2 things.
  - Run both client and server on the same machine (locally), using the local IP 127.0.0.1 and PORT 5545

  - Run server on one machine, and client on another machine (LAN implementation). <br/>
    For this to work, ensure the IP and PORT on the server side are set using the "FOR LAN" portion of the code.
    After starting the server, you can see the IP and PORT that the server is hosted on. Copy this over to the 
    client side and connect to the correct IP and PORT, and run the command line application over LAN

**Example Test Cases:** <br/>
1. 	**Test Msg**  		: *this is a test message* <br/>
    **Test Key**  		: *hdgfetwyusiwacdf*<br/>
    **Encrypted hex**   : *9d12b3b0ed25970fbe4fad7772a827b83d6f96c8696cd6ef1a34f9fc381f72f2*<br/>


2. 	**Test Msg**  		: *networks* <br/>
    **Test Key**  		: *asdfasdfasdfasdf*<br/>
    **Encrypted hex**   : *941870dfe2ed6b14e56409dd1d17abbb*<br/>
