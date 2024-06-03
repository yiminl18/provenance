from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dspy.retrieve.qdrant_rm import QdrantRM
import dspy
import openai
from dsp.utils import deduplicate
import os


api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# Function to load and split documents from a local text file
def load_and_split_local_file(file_path, text_splitter):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return text_splitter.split_text(content)

# Function to get prediction from a local file
def get_prediction_from_local_file(file_path, question, model_name = "gpt-3.5-turbo"):
    # Set up text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    # Load and split documents from a local file
    docs = load_and_split_local_file(file_path, text_splitter)

    # List to hold the content and IDs of each document
    doc_contents = [doc for doc in docs]
    doc_ids = list(range(1, len(docs) + 1))

    # Initialize Qdrant client and add documents
    client = QdrantClient(":memory:")
    client.add(
        collection_name="collection",
        documents=doc_contents,
        ids=doc_ids,
    )

    # Set up Qdrant retriever model
    qdrant_retriever_model = QdrantRM("collection", client, k=10)

    # Set up OpenAI API client
    openai_model = dspy.OpenAI(model=model_name, api_key=openai.api_key)
    dspy.settings.configure(lm=openai_model, rm=qdrant_retriever_model)

    # Define GenerateAnswer and GenerateSearchQuery classes
    class GenerateAnswer(dspy.Signature):
        context = dspy.InputField(desc="may contain relevant facts")
        question = dspy.InputField()
        answer = dspy.OutputField()

    class GenerateSearchQuery(dspy.Signature):
        context = dspy.InputField(desc="may contain relevant facts")
        question = dspy.InputField()
        query = dspy.OutputField()

    # Define SimplifiedBaleen class
    class SimplifiedBaleen(dspy.Module):
        def __init__(self, passages_per_hop=3, max_hops=2):
            super().__init__()
            self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]
            self.retrieve = dspy.Retrieve(k=passages_per_hop)
            self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
            self.max_hops = max_hops

        def forward(self, question):
            context = []
            for hop in range(self.max_hops):
                query = self.generate_query[hop](context=context, question=question).query
                passages = self.retrieve(query).passages
                context = deduplicate(context + passages)
            pred = self.generate_answer(context=context, question=question)
            return dspy.Prediction(context=context, answer=pred.answer)

    # Ask a question and get a prediction
    uncompiled_baleen = SimplifiedBaleen()
    pred = uncompiled_baleen(question)

    result = {
        "Question": question,
        "Predicted Answer": pred.answer,
        "Retrieved Contexts (truncated)": [c[:200] + '...' for c in pred.context]
    }

    return result

