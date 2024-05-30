from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WikipediaLoader
from qdrant_client import QdrantClient
from dspy.retrieve.qdrant_rm import QdrantRM
import dspy
import openai
from dsp.utils import deduplicate

# Set up text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

# Load and split documents
docs = WikipediaLoader(query="San Francisco").load_and_split(text_splitter=text_splitter)

# List to hold the content and IDs of each document
doc_contents = [doc.page_content for doc in docs]
doc_ids = list(range(1, len(docs) + 1))

# Initialize Qdrant client and add documents
client = QdrantClient(":memory:")
client.add(
    collection_name="leo_collection",
    documents=doc_contents,
    ids=doc_ids,
)

# Set up Qdrant retriever model
qdrant_retriever_model = QdrantRM("leo_collection", client, k=10)

# Set up OpenAI API client
openai.api_key = ""
openai_model = dspy.OpenAI(model="gpt-3.5-turbo", api_key=openai.api_key)
dspy.settings.configure(lm=openai_model, rm=qdrant_retriever_model)

# Function to get top passages for a question
def get_top_passages(question):
    retrieve = dspy.Retrieve(k=10)
    topK_passages = retrieve(question, k=10).passages
    print(f"Top {retrieve.k} passages for question: {question} \n", '-' * 30, '\n')
    for idx, passage in enumerate(topK_passages):
        print(f'{idx + 1}]', passage, '\n')

# # Get top passages for a sample question
# get_top_passages("Where is San Fransisco's airport?")

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
my_question = "How many types of rail public transportation means in San Fransisco?"
uncompiled_baleen = SimplifiedBaleen()
pred = uncompiled_baleen(my_question)

# Print the contexts and the answer
print(f"Question: {my_question}")
print(f"Predicted Answer: {pred.answer}")
print(f"Retrieved Contexts (truncated): {[c[:200] + '...' for c in pred.context]}")

# Inspect OpenAI model history
openai_model.inspect_history(n=3)
