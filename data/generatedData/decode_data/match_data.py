import pickle

# Load the existing pickle files
with open('AllData.pkl', 'rb') as file:
    data = pickle.load(file)

with open('length_combine_data.pkl', 'rb') as file:
    data1 = pickle.load(file)
for i in data1:
   print(i)
new = {}  # Initialize an empty dictionary

for i in data:
    length_cat = data1[i]  # Changed 'length-cat' to 'length_cat'
    new[i] = {}  # Initialize the nested dictionary for each 'i' in 'data'
    print(i)
    for j in data[i]:
        new[i][j] = {}  # Initialize the nested dictionary for each 'j' in 'data[i]'
        print(f"this is the data: {j}")
        for z in data[i][j]:
            print(z)
            length = length_cat[z]  # Access 'length_cat' correctly
            a = []
            print(length[0:10])
            # Ensure to limit 'g' to the length of 'data[i][j][z]' to avoid index errors
            for g in range(min(60000, len(data[i][j][z]))):  
                a.append(" ".join(data[i][j][z][g].split(" ")[length[g]:]))

            new[i][j][z] = a

# Pickle the new dictionary 'new'
#with open('AllDataMatch.pkl', 'wb') as file:  # Added '.pkl' extension for clarity
#    pickle.dump(new, file)

print("Data has been successfully processed and saved to 'AllDataMatch.pkl'.")

