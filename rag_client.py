import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".") 
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)

    # TODO: Loop through each discovered directory
        # TODO: Wrap connection attempt in try-except block for error handling
        
            # TODO: Initialize database client with directory path and configuration settings
            
            # TODO: Retrieve list of available collections from the database
            
            # TODO: Loop through each collection found
                # TODO: Create unique identifier key combining directory and collection names
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
        
        # TODO: Handle connection or access errors gracefully
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information

    # TODO: Return complete backends dictionary with all discovered collections

    # Look for ChromaDB directories
    chroma_dirs = [
        d for d in current_dir.iterdir()
        if d.is_dir() and "chroma" in d.name.lower()
    ]

    # Loop through each discovered directory
    for directory in chroma_dirs:
        try:
            # Initialize database client with directory path
            client = chromadb.PersistentClient(path=str(directory))
            
            # Retrieve list of available collections
            collections = client.list_collections()
            
            # Loop through each collection found
            for collection in collections:
                collection_name = collection.name
                key = f"{directory.name}:{collection_name}"
                
                try:
                    doc_count = collection.count()
                except Exception:
                    doc_count = "unknown"
                
                backends[key] = {
                    "path": str(directory),
                    "collection_name": collection_name,
                    "display_name": f"{directory.name} / {collection_name}",
                    "document_count": str(doc_count),
                }

        except Exception as e:
            key = f"{directory.name}:unavailable"
            backends[key] = {
                "path": str(directory),
                "collection_name": "unavailable",
                "display_name": f"{directory.name} / error: {str(e)[:50]}",
                "document_count": "unknown",
            }

    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient
    # TODO: Return the collection with the collection_name
    client = chromadb.PersistentClient(path=chroma_dir)
    collection = client.get_or_create_collection(name=collection_name)
    return collection

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # TODO: Initialize filter variable to None (represents no filtering)

    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs

    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)

    # TODO: Return query results to caller
    where_filter = None

    if mission_filter and mission_filter.lower() != "all":
        where_filter = {"mission": mission_filter}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )

    return results

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section

    # TODO: Loop through paired documents and their metadata using enumeration
        # TODO: Extract mission information from metadata with fallback value
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        # TODO: Extract source information from metadata with fallback value  
        # TODO: Extract category information from metadata with fallback value
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        
        # TODO: Create formatted source header with index number and extracted information
        # TODO: Add source header to context parts list
        
        # TODO: Check document length and truncate if necessary
        # TODO: Add truncated or full document content to context parts list

    # TODO: Join all context parts with newlines and return formatted string

    context_parts = ["Context:\n"]

    for i, (doc, metadata) in enumerate(zip(documents, metadatas), start=1):
        mission = metadata.get("mission", "Unknown mission")
        mission = mission.replace("_", " ").title()

        source = metadata.get("source", "Unknown source")

        category = metadata.get("category", "Unknown category")
        category = category.replace("_", " ").title()

        source_header = f"[Source {i}] Mission: {mission} | Category: {category} | Source: {source}"
        context_parts.append(source_header)

        if len(doc) > 500:
            context_parts.append(doc[:500] + "...")
        else:
            context_parts.append(doc)

        context_parts.append("")

    return "\n".join(context_parts)