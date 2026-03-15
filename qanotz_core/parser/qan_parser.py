"""
Copyright 2026 Alex

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from typing import Any

def _tokenize(text: str) -> list[str]:
    tokens = []
    current = ""
    for char in text:
        if char in "{}":
            if current.strip():
                tokens.append(current.strip())
            tokens.append(char)
            current = ""
        elif char in "\n\t":
            if current and current[-1] != " ":
                current += " "
        else:
            current += char
    if current.strip():
        tokens.append(current.strip())

    tokens: list[str] = [token for token in tokens if token != "{" and token != "}"]
    
    return tokens

def _parse_tokens(tokens: list[str], lookup_mode: bool = False, include_types: str = "tqad") -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    index = 0

    if lookup_mode:
        while index < len(tokens):
            token = tokens[index]
            char_index = 0
            char = token[char_index]

            item = len(result)

            if char == "f":
                result[item] = {}
                char_index += 2

                body: str = ""
                while char_index < len(token):
                    body += token[char_index]
                    char_index += 1

                result[item]["body"] = body
                result[item]["metadata"] = {}
            elif char == "m":
                num_metadata: int = len(result[item - 1]["metadata"])
                result[item - 1]["metadata"][num_metadata] = {}

                char_index += 2
                char = token[char_index]
                if char in "lm": # l for label, m for last modified
                    result[item - 1]["metadata"][num_metadata]["id"] = char
                    char_index += 1
                else:
                    raise ValueError(f"Expected data ID at token '{token}' to be one of 'c', 'h', or 's'")
                
                char_index += 1

                body: str = ""
                while char_index < len(token):
                    body += token[char_index]
                    char_index += 1

                result[item - 1]["metadata"][num_metadata]["body"] = body
            else:
                raise ValueError(f"Expected token type at token '{token}' to be one of 'f' or 'm'. This means there is something seriously wrong with your application. Please report this to the developer on GitHub.")
                
            index += 1
                
        return result
    
    while index < len(tokens):
        token = tokens[index]
        char_index = 0
        char = token[char_index]

        item = result.__len__()

        if char == "q" and char in include_types:
            result[item] = {}
            result[item]["type"] = "question"

            char_index += 2

            body: str = ""
            while char_index < len(token):
                body += token[char_index]
                char_index += 1

            result[item]["body"] = body
            result[item]["answers"] = {}
        elif char == "a" and char in include_types:
            num_answers = len(result[item - 1]["answers"])
            result[item - 1]["answers"][num_answers] = {}

            char_index += 2

            body: str = ""
            while char_index < len(token):
                body += token[char_index]
                char_index += 1

            result[item - 1]["answers"][num_answers]["body"] = body
            result[item - 1]["answers"][num_answers]["metadata"] = {}
        elif char == "d" and char in include_types:
            num_answers = len(result[item - 1]["answers"])
            num_metadata = len(result[item - 1]["answers"][num_answers - 1]["metadata"])
            result[item - 1]["answers"][num_answers - 1]["metadata"][num_metadata] = {}

            char_index += 2
            char = token[char_index]
            if char in "chs":
                result[item - 1]["answers"][num_answers - 1]["metadata"][num_metadata]["id"] = char
                char_index += 1
            else:
                raise ValueError(f"Expected data ID at token '{token}' to be one of 'c', 'h', or 's'")
            
            char_index += 1

            body: str = ""
            while char_index < len(token):
                body += token[char_index]
                char_index += 1

            result[item - 1]["answers"][num_answers - 1]["metadata"][num_metadata]["body"] = body
        elif char == "t" and char in include_types:
            result[item] = {}
            result[item]["type"] = "title"

            char_index += 2

            body: str = ""
            while char_index < len(token):
                body += token[char_index]
                char_index += 1

            result[item]["body"] = body
            
        index += 1
            
    return result

def format_parsed_qafile(qafile_contents: dict[int, dict[str, Any]]) -> str:
    parsed: str = ""
    
    # keys aren’t used, so loop over the values directly
    for item in qafile_contents.values():
        if item["type"] == "title":
            parsed = str(item["body"]) + "\n\n" + parsed
        elif item["type"] == "question":
            parsed += str(item["body"]) + "\n\n"

            i: int = 0
            for answer in item.get("answers", {}).values():
                i += 1
                parsed += f"{i}. {answer['body']}\n"

                for metadata in answer["metadata"].values():
                    match metadata["id"]:
                        case "c":
                            parsed += "  - Comment: " + str(metadata["body"]) + "\n"
                        case "s":
                            parsed += "  - Source: " + str(metadata["body"]) + "\n"
                        case "h":
                            parsed += "  - Helpfulness: " + str(metadata["body"]) + "\n"
                        case _:
                            parsed += "  - Unknown Metadata: " + str(metadata["body"]) + "\n"
            
                parsed += "\n"

        parsed += "\n"

    return parsed


def parse(text: str, lookup_mode: bool = False, include_types: str = "tqad") -> dict[int, dict[str, Any]]:
    tokens = _tokenize(text)
    parsed = _parse_tokens(tokens, lookup_mode, include_types)
    return parsed

if __name__ == "__main__":
    # testing simple example
    sample_text = """
    {t Common Questions}
    {q How do I center a div?
        {a CSS display and justify
            {d c Set 'display' to 'flex' and 'justify-content' to 'center'}
            {d h 1}}
        {a CSS grid
            {d c Set 'display' to 'grid' and 'place-items' to 'center'}
            {d h 0.8}}}

    {q How do I write a print statement in JavaScript?
        {a CSS display and justify
            {d c 'message' must be a string or can be converted into one}
            {d c Don't forget a semicolon (;)}
            {d h 1}}
        {a CSS grid
            {d c Set 'display' to 'grid' and 'place-items' to 'center'}
            {d h 0.8}}}"""
    print(parse(sample_text))

    print("---\n")

    # testing title in location other than first spot, don't include metadata
    sample_text = """
    {q How do I center a div?
        {a CSS display and justify
            {d c Set 'display' to 'flex' and 'justify-content' to 'center'}
            {d h 1}}
        {a CSS grid
            {d c Set 'display' to 'grid' and 'place-items' to 'center'}
            {d h 0.8}}}

    {t Common Questions}

    {q How do I write a print statement in JavaScript?
        {a CSS display and justify
            {d c 'message' must be a string or can be converted into one}
            {d c Don't forget a semicolon (;)}
            {d h 1}}
        {a CSS grid
            {d c Set 'display' to 'grid' and 'place-items' to 'center'}
            {d h 0.8}}}"""
    print(format_parsed_qafile(parse(sample_text, include_types="tqa")))

    print("---\n")

    # example dbl file
    sample_text = """
    {f /home/codespaces/.config/qanotz/qafiles/1.qan
        {m l Common Questions}
        {m m 2/20/2026 2:20 PM}}
    {f /home/codespaces/.config/qanotz/qafiles/2.qan
        {m l CSS Issues}
        {m m 2/20/2026 2:22 PM}}}
    """
    print(parse(sample_text, lookup_mode=True))