from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template="Based on {context}, create a marketing campaign email for {query}."
)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)
