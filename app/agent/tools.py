from app.agent.retriever import retrieve_docs

def calculator_tool(expression: str):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

def retriever_tool(query: str):
    return retrieve_docs(query)

TOOLS = {
    "calculator": calculator_tool,
    "retriever": retriever_tool,
}
