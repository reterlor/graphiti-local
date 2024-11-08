import asyncio
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
import os
from datetime import datetime
from graphiti_core.llm_client import OpenAIClient
from graphiti_core.llm_client import LLMConfig
from graphiti_core.embedder import OpenAIEmbedder, OpenAIEmbedderConfig


os.environ["OPENAI_API_KEY"] = "Anything"

async def initialize_graphiti():
    # Define Graphiti Instance
    graphiti = Graphiti("bolt://localhost:7687", "neo4j", "12345678",
                        llm_client=OpenAIClient(config=LLMConfig(model="ollama/llama3.1", base_url="http://127.0.0.1:4000")),
                        embedder=OpenAIEmbedder(config=OpenAIEmbedderConfig(base_url="http://127.0.0.1:4000", embedding_model="ollama/llama3.1")))
    
    # Initialize the graph database with graphiti's indices. This only needs to be done once.
    await graphiti.build_indices_and_constraints() 
    
    episodes = [
        "Mimikatz targets Windows machines"
        "Mimikatz accesses the lsass.exe process",
        "Mimikatz is a tool used by hackers to obtain credentials",
    ]
    for i, episode in enumerate(episodes):
        await graphiti.add_episode(
            name=f"Cybersecurity {i}",
            episode_body=episode,
            source=EpisodeType.text,
            source_description="Cybersecurity Fact",
            reference_time=datetime.now()
        )

    # Ask questions based on embedded data
    results = await graphiti.search('What does Mimikatz target?')
    print('What does Mimikatz target?')
    print(results[0].fact+'\n')

    results = await graphiti.search('What is Mimikatz?')
    print('What is Mimikatz?')
    print(results[0].fact+'\n')

    results = await graphiti.search('What process does Mimikatz access?')
    print('What process does Mimikatz access?')
    print(results[0].fact+'\n')


# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(initialize_graphiti())


    