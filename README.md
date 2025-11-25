# Inverter Safety Expert RAG (Native Copilot Edition)

This workspace is set up to use **GitHub Copilot** as your expert RAG system.

## How it Works
We have populated the `data/` directory with "seed" knowledge about ISO 26262 and Inverter Safety. GitHub Copilot's `@workspace` command indexes these files to answer your questions.

## How to Use
1.  **Open Copilot Chat**: Click the Chat icon in the sidebar.
2.  **Type a Query**: Use the `@workspace` tag to force Copilot to look at your files.

### Example Queries
Try these now:

*   `@workspace What are the 3 levels of the E-Gas monitoring concept?`
*   `@workspace How should I handle a flux weakening failure at high speed?`
*   `@workspace What are the ASIL D requirements for software unit testing according to Part 6?`
*   `@workspace Explain the difference between Level 1 and Level 2 monitoring.`

## Privacy & Collaboration
*   **Private Data**: The `data/` folder is configured in `.gitignore` to be ignored. Any PDFs or documents you put there will **NOT** be uploaded to GitHub.
*   **Sharing**: You can safely commit and push this repository. Others can clone it, but they will need to populate their own `data/` folder to make it work.
