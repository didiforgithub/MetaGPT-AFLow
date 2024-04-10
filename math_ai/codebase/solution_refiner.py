# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @ Yi Huang @ Xin Cheng
# email      :
# Description: Solution Refiner Refine the results generated by the Math Resolver

from typing import Dict
from math_ai.codebase.engine.llm import OpenAILLM


class SolutionRefiner:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "<TODO Here is Solution Refiner's system prompt>"
        self.llm.set_role(self.role)
    def run(self, problem: Dict) -> str:

        return "final result"

