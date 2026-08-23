from mcp.server.fastmcp import FastMCP
from vector_db import search
from weather import get_weather
mcp=FastMCP("Smart Knowledge Base Assistant")
@mcp.tool()
def search_documents(query:str)->str:# accepts only string return only string
    """Search the Knowledge base documents for information relevant to the query."""# DOCSTRING explain what function does
    result=search(query,top_k=3)
    return "\n\n".join(result)
@mcp.tool()
def get_weather_tool(city:str)->str:
    """Get the Current Weather for a given city. """
    return get_weather(city)
@mcp.tool()
def save_note(note:str)->str:
    """Save a note to a local notes files."""
    with open("notes.txt","a") as f:
        f.write(note+"\n")
    return "Note saved successfuly."
if __name__=="__main__":
    mcp.run()

