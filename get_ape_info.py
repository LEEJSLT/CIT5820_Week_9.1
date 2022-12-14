from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.toChecksumAddress(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = f"https://mainnet.infura.io/v3/d1e4ee56d41f4009837f757a1ccfef86" #YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
	assert isinstance(apeID,int), f"{apeID} is not an int"
	assert 1 <= apeID, f"{apeID} must be at least 1"

	data = {'owner': "", 'image': "", 'eyes': "" }
	
	# YOUR CODE HERE
	contract = web3.eth.contract(address=contract_address, abi=abi) #Get the ethereum contract
	owner = contract.functions.ownerOf(apeID).call() #Get the owner of the apeID

	targetApeID = 'QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/' + str(apeID) #Create the target ape ID string
	response = requests.get(f"https://gateway.pinata.cloud/ipfs/{targetApeID}") # Get the response from the IPFS
	response_data = response.json()

	# Owner Value
	data["owner"] = owner

	# Image Data
	for index, (key, value) in enumerate(response_data.items()):
		if key == 'image':
			data[key] = str(value)

	# Eyes Data	
	for item in response_data['attributes']:
		if item['trait_type'] == 'Eyes':
			data['eyes'] = str(item['value'])

	assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
	assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
	return data

