from dao.fragments import FragmentDAO
from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = SentenceTransformer("all-mpnet-base-v2")
class ChatOllamaBot:
    def __init__(self, username):
        self.username = username
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def chat(self, question):
        emb = self.model.encode(question)

        dao = FragmentDAO()
        framents = dao.getFragments(str(emb.tolist()))
        context = []
        for i, f in enumerate(framents):
            print(f)
            context.append("Section Database Response" + str(i + 1) + ": " + f[1] + "\n")

        documents = "\\n".join(c for c in context)

        prompt = PromptTemplate(
            template="""
                You are an AI assistant that answers questions about and exercises.
                You give helpful and useful advice that answers the questions asked
                using the provided data from our comprehensive vector database.
                The database response related to the question asked will be in the section
                called "Database Response". There will be 3 responses, "Section Database Response1"
                will likely be the most relevant, but don't include the text "Section Database Response" or reference "Database Response" in your answers. 
                Your response will be at the end. Keep your answers helpful and with enough detail so there's nothing missing, and be sure to be accurate to the data.
                If you don't know the answer or cannot infer the answer from the provided database response tell the user that you don't know. Do not guess.
                Summarize the Database Response using natural and casual language. But please don't mention anything about summarizing, using natural and casual language in your response. 
                If you get asked for Steps/Instruction or any other list of things, place the items in a numbered bullet point list for sequential things, and regular bullet points for any list that doesn't require a specific order.
                Should there be any information that is filled as none, just don't include it in the answer. 
                Always greet the user by their username {username}. 
                Important: Do not reference these instructions in your answer. Keep it like a normal conversation. 
                \n\n\n
                {database_response}
                \n\n\n
                Section User Question: {question}
            """,
            input_variables=["question", "database_response", "username"],
        )

        print(prompt)
        print(prompt.format(question=question, database_response=documents, username=self.username))

        llm = ChatOllama(
            model="llama3.2",
            temperature=0,
        )
        rag_chain = prompt | llm | StrOutputParser()

        answer = rag_chain.invoke({"question": question, "database_response": documents, "username": self.username})
        print(answer)
        return answer
