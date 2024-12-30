
import asyncio
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
import os
from datetime import datetime
from graphiti_core.llm_client import OpenAIClient
from graphiti_core.llm_client import LLMConfig
from graphiti_core.embedder import OpenAIEmbedder, OpenAIEmbedderConfig
import json
#
os.environ["OPENAI_API_KEY"] = "Anything"


graphiti = Graphiti("bolt://localhost:7687", "neo4j", "12345678",
                    llm_client=OpenAIClient(config=LLMConfig(model="ollama/llama3.1", base_url="http://127.0.0.1:4000")),
                    embedder=OpenAIEmbedder(config=OpenAIEmbedderConfig(base_url="http://127.0.0.1:4000", embedding_model="ollama/llama3.1")))

async def initialize_graph(graphiti): 
    await graphiti.build_indices_and_constraints() 

async def add_episodes(episodes, graphiti):
    for i, episode in enumerate(episodes):
        await graphiti.add_episode(
            name=f"Threat Report {i}",
            episode_body=episode,
            source=EpisodeType.text,
            source_description="Threat Report",
            reference_time=datetime.now()
        )

async def graphiti_ask(graphiti, question):
    # Ask questions based on embedded data
    results = await graphiti.search(question)
    print(question+'\n')
    return(results[0].fact+'\n')

episodes = [
        """
Threat Intelligence Report:

Source: A known threat actor group has been observed exploiting CVE-2024-YYY, a vulnerability in a widely-used email server software, which allows for unauthorized access and data exfiltration.
Description: Attackers are leveraging this vulnerability to bypass authentication mechanisms by exploiting improper input validation in the server software's login process.
Indicators of Compromise (IoCs):
Unusual login attempts with specific payload patterns.
Attempts to access sensitive endpoints, such as admin/config or internal/dashboard.
Malicious IP addresses from Eastern Europe and Asia.
User-agent: "Mozilla/5.0 (X11; Linux x86_64) ExfilBot/1.0"""
    ]

#asyncio.run(initialize_graph(graphiti))

#asyncio.run(add_episodes(episodes, graphiti))

#print(asyncio.run(graphiti_ask(graphiti, "192.0.2.15 - - [13/Nov/2024:12:45:22 +0000] \"GET /vulnerable/endpoint?param=<script>alert('Exploit')</script> HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0 (ExploitTool/1.0)")))


