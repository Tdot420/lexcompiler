def compile_to_graph(text: str):
    prompt = f"""
Return ONLY valid JSON.

Schema:
{{
  "nodes": [],
  "edges": []
}}

Do not include explanations.

Text:
{text[:2000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    print("RAW LLM OUTPUT:", repr(content))

    if not content or content.strip() == "":
        raise Exception("LLM returned EMPTY response")

    content = content.strip()

    # attempt parse
    try:
        graph = json.loads(content)
    except Exception:
        # try to extract JSON
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            graph = json.loads(match.group())
        else:
            raise Exception(f"Invalid JSON from LLM: {content}")

    return graph