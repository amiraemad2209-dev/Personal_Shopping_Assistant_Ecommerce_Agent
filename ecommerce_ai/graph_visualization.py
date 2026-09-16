


# ===============================================================================#
# ========================== Graph Visualization ================================#
# ===============================================================================#

from agent import workflow


def create_graph_html():

    # Compile the LangGraph
    graph = workflow.compile()

    # Get Mermaid representation
    mermaid_code = graph.get_graph().draw_mermaid()

    # HTML page
    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <title>LangGraph Visualization</title>

    <script type="module">
        import mermaid from
        'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark'
        }});
    </script>

    <style>

        body {{
            margin: 0;
            padding: 40px;

            background: #0f172a;
            color: white;

            font-family: Arial, sans-serif;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 40px;
        }}

        .graph-container {{
            background: #1e293b;

            border-radius: 20px;

            padding: 40px;

            overflow: auto;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.4);
        }}

    </style>

</head>

<body>

    <h1>LangGraph Visualization</h1>

    <div class="graph-container">

        <div class="mermaid">

{mermaid_code}

        </div>

    </div>

</body>

</html>
"""

    # Save HTML file
    with open(
        "langgraph_visualization.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    print(
        "\n✅ Graph visualization created successfully!"
    )

    print(
        "📁 langgraph_visualization.html"
    )


if __name__ == "__main__":

    create_graph_html()