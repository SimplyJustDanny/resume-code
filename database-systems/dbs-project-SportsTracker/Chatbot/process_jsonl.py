
from os import listdir

from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from dao.fragments import FragmentDAO
from sentence_transformers import SentenceTransformer
import json


model = SentenceTransformer("all-mpnet-base-v2")
fraDAO = FragmentDAO()
# emb = model.encode("Benchpress")
# print(fraDAO.getFragments(str(emb.tolist())));
# exit(0)

files = listdir("./jsonl")
print(files)

file = open("./jsonl/" + files[0], 'r');
lines = []
for line in file:
    myjson = json.loads(line)
    lines.append((myjson["id"], myjson["text"]))


print(lines)
print()
print()

ll = len(lines)
i = 0

for id, text in lines:
    text = text.replace("\\n", "\n")
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n", ". ", " ", "", "{", "}", ":", ","],
        chunk_size=len(text),
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False
    )
    character_split_texts = character_splitter.split_text(''.join(text))
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=384)

    token_split_texts = []
    for text in character_split_texts:
        token_split_texts += token_splitter.split_text(text)

    print(ll, ", ", i, "  Progress: ", ((100*i)//ll), "%", sep="", end="\r")

    i += 1
    for t in token_split_texts:
        emb = model.encode(t)
        fraDAO.insertFragment(t, emb.tolist())

print()

