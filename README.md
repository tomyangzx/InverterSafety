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

## Next Steps
To make this even smarter:
1.  **Add More Data**: Download the PDF standards and whitepapers mentioned in `docs/research_guide.md`.
2.  **Convert to Markdown**: While Copilot reads code well, converting complex PDFs to Markdown (like the files in `data/`) often improves accuracy.
3.  **Keep it Organized**: Group files by topic in `data/` (e.g., `data/standards/`, `data/hardware/`).
