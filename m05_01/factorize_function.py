from multiprocessing import Process, Pool
from time import time



def factorize(*numbers):
	""""
	Get list of numbers and for each input number
	returns a list of numbers that a given number could be devided without rest
	"""
	results = []
	for number in numbers:
		result = []
		for i in range(1, number + 1):
			if number % i == 0:
				result.append(i)

		results.append(result)
		#print(result)
	return results




if __name__ == "__main__":
	start = time()
	a, b, c, d = factorize(128, 255, 99999, 10651060)
	print(f"1. Synchronize implementation time: {time() - start} \n")
	#print(f"{a, b, c ,d} \n")

	"""
	Multiprocessing Pool
	"""
	#Pool.map
	start_poolMap = time()
	with Pool(3) as pool:
		r = pool.map(factorize, (128, 255, 99999, 10651060))
		# print(f"{r} \n")
	print(f"2. Multiprocessing Pool.map, parallel implementations time: {time() - start_poolMap} \n")

	#Pool.imap
	start_poolIMap = time()
	with Pool(3) as pool:
		iterator = pool.imap(factorize, (128, 255, 99999, 10651060))
		#print(iterator)
		# for el in iterator:
		# 	print(el)
	print(f"3. Multiprocessing Pool.imap, parallel implementations time: {time() - start_poolIMap} \n")

	#Pool.apply_async
	start_poolApply_async = time()
	with Pool(3) as pool:
		for i in (128, 255, 99999, 10651060):
			result = pool.apply_async(factorize, (i,))
	print(f"4. Multiprocessing Pool.apply_async, parallel implementations time: {time() - start_poolApply_async} \n")


	"""
	Multiprocessing Process
	"""
	#Process
	start_Process = time()
	for i in (128, 255, 99999, 10651060):
		pr = Process(target=factorize, args=(i,))
		pr.start()
	print(f"5. Multiprocessing Process, parallel implementations time: {time() - start_Process} \n")

