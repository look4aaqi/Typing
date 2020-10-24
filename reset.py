letters = ""
for i in range(32,127):
    letters += chr(i)
probability = [1/len(letters)]*len(letters)

import pickle

with open('letters.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(letters, filehandle)

with open('probability.data', 'wb') as filehandle:
    pickle.dump(probability, filehandle)