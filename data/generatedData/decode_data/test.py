import pickle

# Replace 'your_file.pickle' with your file name
file_path = 'AllData.pkl'
# Open and load the pickle file
#with open("PubMed.pkl", 'rb') as file:
#    data = pickle.load(file)
#with open("hn.pkl", 'rb') as file:
#    data1 = pickle.load(file)
#with open("wiki.pkl", 'rb') as file:
#    data2 = pickle.load(file)
#with open("book2.pkl", 'rb') as file:
#    data3 = pickle.load(file)
with open("AllDataMatch.pkl", 'rb') as file:
    data = pickle.load(file)
#data["PubMed"]["gptneo-2.7B"]["zeroshot"] = data["PubMed"]["gptneo-2.7b"]["zeroshot"] 
#data["hn"]["opt-2.7b"]["fewshot"] = data["hn"]["opt-2.7b"]["hn"]
#data["hn"]["opt-1.3b"]["fewshot"] = data["hn"]["opt-1.3b"]["hn"]
#data["hn"]["opt-125m"]["fewshot"] = data["hn"]["opt-125m"]["hn"]
#data["hn"]["opt-350m"]["fewshot"] = data["hn"]["opt-350m"]["hn"]
#del data["hn"]["opt-2.7b"]["hn"]
#del data["hn"]["opt-1.3b"]["hn"]
#del data["hn"]["opt-125m"]["hn"]
#del data["hn"]["opt-350m"]["hn"]

#data["wiki"]["gptneo-2.7B"]["zeroshot"] = data["wiki"]["gptneo-2.7b"]["zeroshot"]
#data["book2"]["gptneo-2.7B"]["zeroshot"] = data["book2"]["gptneo-2.7b"]["zeroshot"]
#del data["PubMed"]['gptneo-2.7b']
#del data["hn"]['gptneo-2.7b']
#del data["wiki"]['gptneo-2.7b']
#del data["book2"]['gptneo-2.7b']
#hehe ={}
#hehe ["PubMed"] = data["PubMed"]
#hehe["hn"] = data1["hn"]
#hehe["wiki"] = data2["wiki"]
#hehe["book2"] = data3["book2"]
#for key  in data:
#    for keys in data[key]:
#        for keyss in data[key][keys]:
#            print(keyss)
#            break
for key in data["wiki"]:
     print(f"key: {key}")
     print("------------")
     for i in data["hn"][key]:
         print(data["hn"][key][i][0])
     break
     print("_______")
# Print the loaded data

#from transformers import GPTNeoXForCausalLM, AutoTokenizer
#tokenizer = AutoTokenizer.from_pretrained(
#  "EleutherAI/pythia-2.8b-deduped",
#  revision="step143000",
#  cache_dir="./pythia-2.8b-deduped/step143000",
#)
#def save_to_pickle(obj, filename):
#    with open(filename, 'wb') as file:  # 'wb' means write in binary mode
#        pickle.dump(obj, file)
#    print(f"Object saved to {filename} successfully.")
#save_to_pickle(data, f"AllData.pkl")
