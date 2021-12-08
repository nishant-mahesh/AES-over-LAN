'''
Name 		: Nishant Mahesh, Neil Chowdhary
Github Repo : https://github.com/nishant-mahesh/AES-over-LAN.git 
Code 		: Course Project CS 1340
Description	: 	- In this project, we will implement a simple AES encryption/ decryption application using socket programming.
				- Upon establishing server and client connection, client can choose to encrypt/ decrypt a message.
				- Client then sends the plaintext (or ciphertext) and a valid 16 byte key to the server
				- Server performs the encryption (or decryption) and sends the resulting ciphertext (or plaintext) to client
				- Client displays the result and disconnects

Testing 	:In order to test the project, the evaluator can do one of 2 things.
				a) 	Run both client and server on the same machine (locally), using the local IP 127.0.0.1 and PORT 5545

				b) 	Run server on one machine, and client on another machine (LAN implementation). 
					For this to work, ensure the IP and PORT on the server side are set using the "FOR LAN" portion of the code.
					After starting the server, you can see the IP and PORT that the server is hosted on. Copy this over to the 
					client side and connect to the correct IP and PORT, and run the command line application over LAN

			Some test cases to run encryption/ decryption on are as follows:

				1. 	Test Msg  		: this is a test message
					Test Key  		: hdgfetwyusiwacdf
					Encrypted hex   : 9d12b3b0ed25970fbe4fad7772a827b83d6f96c8696cd6ef1a34f9fc381f72f2


				2.	Test Msg  		: networks
					Test Key  		: asdfasdfasdfasdf
					Encrypted hex  	: 941870dfe2ed6b14e56409dd1d17abbb

'''				

import socket
import json
import pickle


#================Choosing IP and PORT================#
'''
For testing LOCALLY, use (IP = '127.0.0.1' , PORT = 5545)
For testing on LAN, use (IP = server's IP, PORT = 10000)
'''

IP   = '127.0.0.1' # Change from 127.0.0.1 to server's IP if testing on LAN
PORT = 5545

#================Setting up client================#
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
clientsocket.connect((IP, PORT))


#================Client-Server Interaction================#

# printing intro message
print()
print('---------------------------------------')
print(clientsocket.recv(1024).decode()) #receive intro message
print('---------------------------------------')
print()

# sending OK response to ensure connection is successful, and interaction can begin
clientsocket.send('OK'.encode())

choiceMessage = clientsocket.recv(1024).decode() #receive prompt for encryption or decryption

choice = input(choiceMessage)
choice = choice.lower()

while(choice != 'e' and choice != 'd'): # ensure correct input is sent to the server
	print("Incorrect choice! Please re-enter")
	print()
	choice = input(choiceMessage)
	choice = choice.lower()

clientsocket.send(choice.encode()) # send client's choice of encryption/decryption to the server

# Client chooses ENCRYPTION
if(choice == 'e'):

	messageRequest = clientsocket.recv(1024).decode() # receive prompt for plaintext from server
	plaintext = input(messageRequest) # input plaintext from the client

	clientsocket.send(plaintext.encode()) # send the plaintext to server

	keyRequest = clientsocket.recv(1024).decode() # receive prompt for secret key from server
	key = input(keyRequest) # # input secret key from the client


	while(len(key) != 16): # ensure secret key is 16 bytes (required for AES)
		print("Key length is not 128 bits! Please re-enter")
		print()
		key = input(keyRequest)

	clientsocket.send(key.encode()) # send key to server

	ciphertext = clientsocket.recv(1024) # receive ciphertext from server in bytearray fromat

	print(f"The ciphertext in hex is: {ciphertext.hex()}") # convert bytearray string to hex string and print
	print()


# Client chooses DECRYPTION
else:

	messageRequest = clientsocket.recv(1024).decode() # receive prompt for ciphertext from server
	ciphertext = input(messageRequest) # input ciphertext from the client

	clientsocket.send(ciphertext.encode()) # send the ciphertext to server

	keyRequest = clientsocket.recv(1024).decode() # receive prompt for secret key from server
	key = input(keyRequest) # input secret key from the client


	while(len(key) != 16): # ensure secret key is 16 bytes (required for AES)
		print("Key length is not 128 bits! Please re-enter")
		print()
		key = input(keyRequest)

	clientsocket.send(key.encode()) # send valid key to server

	data = json.loads(clientsocket.recv(1024).decode()) # receive decrypted message (or error message) from server
	
	# If error occured during decryption
	if(data[0] == "FAIL"):
		print(data[1]) #print message for client

	# If decryption was successful
	else:
		assert(data[0] == "SUCCESS")
		print(f"The plaintext is: {data[1]}") #print message for client
	print()

