"""
Copyright 2026 Alex

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

# DO NOT REMOVE UNTIL FINISHED WITH THE MODULE
#from qanotz_core.parser.qan_parser import parse
from qanotz_core.data.log import Logger
from typing import Any

def get_query_index(parsed_qa: dict[int, dict[str, Any]], query: str) -> list[int]:
    """
    Takes in a formatted query and returns the index of the question in the parsed_qa dictionary.
    The structure of the parsed_qa dictionary is as follows:
    <question_index>:<answer_index>:<metadata_index>

    If you need just the question, you may exclude the answer and metadata indices, same with getting the answer without metadata.
    """
    log = Logger()

    current: str = ""
    l: int = 0
    loc: list[int] = []
    for char in query:
        if l >= 3:
            log.log_message("Internal query had over three sections. From function get_query_item in qanotz_core.")
            break

        match char:
            case ":":
                loc.append(int(current))
                current = ""
                l += 1
            case _:
                if char.isdigit():
                    current += char

    return loc

def get_query_item(parsed_qa: dict[int, dict[str, Any]], query: str) -> dict[str, Any]:
    """
    Takes in a formatted query and returns the index of the question in the parsed_qa dictionary.
    The structure of the parsed_qa dictionary is as follows:
    <question_index>:<answer_index>:<metadata_index>

    If you need just the question, you may exclude the answer and metadata indices, same with getting the answer without metadata.
    """
    log = Logger()

    current: str = ""
    l: int = 0
    loc: list[int] = []
    for char in query:
        if l >= 3:
            log.log_message("Internal query had over three sections. From function get_query_item in qanotz_core.")
            break

        match char:
            case ":":
                loc.append(int(current))
                current = ""
                l += 1
            case _:
                if char.isdigit():
                    current += char

    match len(loc):
        case 1:
            return parsed_qa[loc[0]]
        case 2:
            return parsed_qa[loc[0]]["answers"][loc[1]]
        case 3:
            return parsed_qa[loc[0]]["answers"][loc[1]]["metadata"][loc[2]]
        case _:
            log.log_message("len(loc) is either empty or has more than three values. This is a MAJOR UNHANDLED ERROR; Please report to GitHub. From function get_query_item in qanotz_core.")
            return parsed_qa[loc[0]]
