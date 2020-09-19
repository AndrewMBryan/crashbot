import hashlib
import hmac
import math
import csv
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
import seaborn as sns

#Get the previous hash amount

def getPrevHash(currHash):
	prevHash = hashlib.sha256()
	prevHash.update(currHash)
	return prevHash.hexdigest().encode("utf-8")

#get future hash ammount

def getFutrureHash(currHash):
	futHash = hashlib.sha256()
	futHash.update(currHash)
	return futHash.hexdigest().encode("utf-8")

def hmacDivisible(hmacHash, mod):
	val = 0
	o = len(hmacHash) % 4
	i = o - 4 if o > 0 else 0
	while i < len(hmacHash):
		val = ((val << 16) + int(hmacHash[i : i + 4], 16)) % mod
		i += 4

	#javascript code
	#for (var i = o > 0 ? o - 4: 0; i < hash.length; i += 4) {
	#	val = ((val << 16) + parseInt(hash.substring(i, i + 4), 16)) % mod;
	#}

	return val == 0

def getCrashFromHash(currHash):
	hmacCalculator = hmac.new(currHash, digestmod=hashlib.sha256)
	hmacCalculator.update(b"0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c")
	hmacHash = hmacCalculator.hexdigest().encode("utf-8").decode()
	if hmacDivisible(hmacHash, 101):
		return 0
	h = int(hmacHash[0 : 13], 16)
	e = math.pow(2, 52)
	return (math.floor((100 * e - h) / (e - h)) / 100)


# base 100000
# test 1000
while True:
	limit = 10000
	gameHash = input("Please enter a game hash to start with: ").encode("utf-8")
	print("Writing past crashes to 'crashes.txt'...")
	currHash = gameHash
	outputFilePrev = open(os.path.join(os.path.dirname(__file__), "pastcrashes.csv"), "w")
	csvWriter = csv.writer(outputFilePrev)
	csvWriter.writerow(["Game Hash", "Crash"])
	outputFileFut = open(os.path.join(os.path.dirname(__file__), "futcrashes.csv"), "w")
	futCsvWriter = csv.writer(outputFileFut)
	futCsvWriter.writerow(["Game Hash", "Crash"])

	for i in range(limit):
		csvWriter.writerow([currHash.decode(), str(getCrashFromHash(currHash))])
		currHash = getPrevHash(currHash)
	outputFilePrev.close()

	currHash = '77b271fe12fca03c618f63dfb79d4105726ba9d4a25bb3f1964e435ccf9cb209'.encode("utf-8")

	for i in range(10000):
		futCsvWriter.writerow([currHash.decode(), str(getCrashFromHash(currHash))])
		currHash = getFutrureHash(currHash)
	outputFileFut.close()

	print("Write complete!")

	prevcrashes = pd.read_csv(os.path.join(os.path.dirname(__file__), "pastcrashes.csv"))
	# Crash < 10
	prevcrashes = prevcrashes.query("Crash < 5")

	futcrashes = pd.read_csv(os.path.join(os.path.dirname(__file__), "futcrashes.csv"))
	futcrashes = futcrashes.query("Crash < 5")

	#crashes = crashes.assign(Time=list(range(len(crashes))), Normalized_Crash=crashes["Crash"].apply(np.floor))

	print("Prev: " ,prevcrashes.head(5))
	print("Future: " ,futcrashes.head(5))

	# prev neighbors 20
	#regressor = KNeighborsRegressor(n_neighbors=20)

	#attributes = crashes["Time"].values.reshape(-1, 1)

	#labels = crashes["Crash"]
	# train_x default -44000
	#train_x = attributes[:-50]
	# test_x default -44000
	#test_x = attributes[-50:]
	# train_y default -44000
	#train_y = labels[:-50]
	# test_y default -44000
	#test_y = labels[-50:]

	#regressor.fit(train_x, train_y)

	#prediction = regressor.predict(test_x)

	#print(prediction)

	#plt.scatter(test_x, test_y, color="black")
	# prev line width 3
	#plt.plot(test_x, prediction, color="blue", linewidth=1)

	#plt.show()

