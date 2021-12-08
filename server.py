'''
Name 		: Nishant Mahesh, Neil Chowdhary
Github Repo 	: https://github.com/nishant-mahesh/AES-over-LAN.git 
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
import string
import random
from os import urandom
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

#================Choosing IP and PORT================#


# For testing LOCALLY (not LAN), use the IP and PORT below

# ----- FOR LOCAL ----- #
IP   = '127.0.0.1'
PORT = 5545


# For testing on LAN, use the code section below

# ------- FOR LAN ------ #
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# IP = s.getsockname()[0]
# s.close()
# PORT = 10000


#================Setting up server================#

#server socket instantiation
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server
serversocket.bind((IP, PORT))

# start listening
serversocket.listen()

print(f'Server is running! Listening for transmission from client at: ({IP}, {PORT})')
print()

#================Server-Client Interaction================#

# Default initialisation vector
iv = b'ghidhjuwvxgshwak' 


def handle_client(clientsocket, address):
	global iv
	print(f'New connection made with client at address {address}') 

	introMessage = 'Welcome to the AES encryption/ decryption portal!'

	clientsocket.send(introMessage.encode()) #send introductory message to client

	if(clientsocket.recv(1024).decode() != 'OK'):
		print('Connection failed! Disconnecting...')
		clientsocket.close()

	choiceMessage = 'Do you want to encrypt or decrypt? (Enter E/D): '	
	clientsocket.send(choiceMessage.encode()) #Ask client to choose between encryption and decryption


	choice = (clientsocket.recv(1024).decode()).lower()

	assert(choice == 'e' or choice == 'd')

	# Client chooses ENCRYPTION
	if(choice == 'e'):

		messageRequest = 'Enter the plaintext: '
		clientsocket.send(messageRequest.encode()) # prompt client for the plaintext

		plaintext = clientsocket.recv(1024).decode() # receive the plaintext from client


		keyRequest= 'Enter the secret key: ' 
		clientsocket.send(keyRequest.encode()) # prompt client for the key

		key = clientsocket.recv(1024).decode() # receive the key from client

		assert(len(key) == 16)

		plaintext = bytearray(plaintext.encode()) # convert plaintext from string to bytearray for encryption operation

		paddedPt = pad(plaintext, AES.block_size) # pad the bytearray to ensure it is a multiple of 16

		key = bytearray(key.encode()) # convert key from string to bytearray for encryption operation

		aes_obj = AES.new(key, AES.MODE_CBC, iv) 

		ciphertext = aes_obj.encrypt(paddedPt) #produce encrypted bytearray

		clientsocket.send(ciphertext) #send bytearray string to client to convert to hex on client side

	# Client chooses DECRYPTION
	else:
		messageRequest = 'Enter the ciphertext (in hex): '
		clientsocket.send(messageRequest.encode()) # prompt client for the ciphertext (in hex format)

		ciphertext = clientsocket.recv(1024).decode() # receive the ciphertext from client


		keyRequest= 'Enter the secret key: '
		clientsocket.send(keyRequest.encode()) # prompt client for the key

		key = clientsocket.recv(1024).decode() # receive the key from client

		ciphertext = bytes.fromhex(ciphertext) # convert hex cipher to byte format

		key = bytearray(key.encode()) # convert to bytearrray for decryption

		try: 

			aes_obj = AES.new(key, AES.MODE_CBC, iv) 
			
			plaintext = aes_obj.decrypt(ciphertext) # decrypt the ciphertext
			
			plaintext = unpad(plaintext, AES.block_size) # unpad the padding added during encyption to produce the original message
			
			plaintext = plaintext.decode('utf-8') # convert from bytearray to utf8 encoded string

			data = ["SUCCESS", plaintext]
			data = json.dumps(data)

			clientsocket.send(data.encode()) 
			
		except:
			error_msg = "Error detected, please ensure that cipher entered and secret key are valid!"

			data = ["FAIL", error_msg]

			data = json.dumps(data)

			clientsocket.send(data.encode())


#================Server Starts Listening================#

while True:

	# wait until a client connects
	(clientsocket, address) = serversocket.accept()

	# call the "handle_client" function to interact with the client
	handle_client(clientsocket, address)

	# close the connection and start the next iteration of the loop to wait for the next client
	clientsocket.close()


print('Server is closing...')
serversocket.close()



'''
Seqeunce of Events:
1. Client connects to server
2. Server accepts connection 

3. Server asks if client wants to encrypt/ decrypt
4. 	a. (Client wants to encrypt:)
		- Client sends plaintext
		- Server receives plaintext
		- Client sends secret key
		- Server receives secret key
		- Server computes encryption
		- Server sends ciphertext (in hex) to client 
		- Client displays cipher and disconnects
	b. (Client wants to decrypt)
		- Client sends ciphertext (in hex)
		- Server receives ciphertext
		- Client sends secret key
		- Server receives secret key
		- Server decrypts
		If decryption succesful, server sends to client, client dsiplays and disconnects
		(if error, error message is displayed and then disconnects)
'''
