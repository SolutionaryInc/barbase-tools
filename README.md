# Barbase Tools

**Barbase Tools** is a public repository that contains helper scripts, services, and tools used in the development of the [Barbase](https://barbase.solutionary.me) project — a service that returns accurate and language-specific product names by barcode.

Barbase uses a community-powered system of voting and verification to ensure the highest quality of product names. Each **barcode** may be associated with multiple **names**, and each **name** can be available in several **languages**. Users vote to select the most accurate name for a barcode and the best translation per language.

## What's in this repository?

This repo serves as a home for utilities and tooling that support the Barbase ecosystem. Planned and existing components include:

- **Language Detection Service** — Determines the language of a product name.
- **Camera-Based Recognition Tool** — Captures product names using a smartphone or webcam.
- **Parsers and Crawlers** — Scripts to extract product data from open websites and convert it into Barbase-compatible format.
- **Import Tools** — Scripts and helpers to bulk-import data into the Barbase system.
- **Data Cleaning and Validation Scripts** — Ensure imported data meets formatting and quality standards.

## Contributing

We welcome contributions!  
Whether it's writing a new parser, improving an existing tool, or fixing bugs — your help is appreciated.

**How to contribute via fork and pull request:**

1. **Fork** this repository to your own GitHub account.
2. **Create a new branch** for your changes (for example, `feature/my-parser`).
3. Make your changes or add your new parser/script.
    - **Parser folder naming:** Name your parser folder exactly as the domain you are parsing, and place it inside the `domains` directory (for example, `domains/example.com`).
4. **Open a Pull Request (PR)** from your branch to the `main` branch of this repository.
5. Wait for review and address any feedback.

**Important:**  
Before you start working, please leave a comment with a link to the source you plan to parse in [Discussions #3](https://github.com/SolutionaryInc/barbase-tools/discussions/3).  
This helps avoid duplicate work and lets others know which sources are already being processed. Once your PR is merged, the source will be considered completed.

Let's build the most comprehensive open barcode-to-name database together.

---

💬 Got an idea for a tool or script? Open an [issue](https://github.com/SolutionaryInc/barbase-tools/issues) or start a discussion — let’s build Barbase together.

## License

MIT License.
