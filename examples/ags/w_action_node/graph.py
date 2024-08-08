# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 22:07 PM
# @Author  : didi
# @Desc    : graph & an instance - humanevalgraph

from typing import List



from evalplus.data import get_human_eval_plus

from examples.ags.w_action_node.operator import (
    FuEnsemble,
    Generate,
    GenerateCode,
    GenerateCodeBlock,
    MdEnsemble,
    Rephrase,
    Review,
    Revise,
    Test,
)
from examples.ags.w_action_node.utils import extract_test_cases_from_jsonl
from metagpt.llm import LLM


class Graph:
    def __init__(self, name: str, llm: LLM) -> None:
        self.name = name
        self.model = llm

    def __call__():
        NotImplementedError("Subclasses must implement __call__ method")

    def optimize(dataset: List):
        pass


class HumanEvalGraph(Graph):
    def __init__(self, name: str, llm: LLM, criteria: str, vote_count: int = 5) -> None:
        super().__init__(name, llm)
        self.criteria = criteria  # TODO 自动构建图时，图的初始参数与图所使用的算子要求的外部参数相匹配
        self.generate_code = GenerateCode(llm=llm)
        self.generate_code_block = GenerateCodeBlock(llm=llm)
        self.review = Review(llm=llm, criteria=criteria)
        self.revise = Revise(llm=llm)
        self.rephrase = Rephrase(llm=llm)
        self.tester = Test(llm=llm)
        self.fuensemble = FuEnsemble(llm=llm)
        self.mdensemble = MdEnsemble(llm=llm, vote_count=vote_count)

    async def __call__(self, problem: str, ensemble_count: int = 3):
        solution_list = []
        for _ in range(ensemble_count):
            solution = await self.generate_code_block(problem)
            solution = solution.get("code_solution")
            solution_list.append(solution)
        solution = await self.mdensemble("code", solution_list, problem)
        return solution

    async def alpha_codium(self, problem_id: str, problem: str, ensemble_count: int = 3):
        """
        Paper: Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering
        Link: https://arxiv.org/abs/2404.14963
        Flow: An incomplete version of alpha codium, implementing the basic process of rephrase -> code ensemble -> tes
        """
        test_cases = extract_test_cases_from_jsonl(problem_id)
        entry_point = get_human_eval_plus()[problem_id]["entry_point"]
        rephrase_problem = await self.rephrase(problem)  # 在rephrase 中拼接原始的问题描述
        solution_list = []
        for _ in range(ensemble_count):
            solution = await self.generate_code_block.rephrase_generate(
                problem, rephrase_problem, function_name=entry_point
            )
            solution = solution.get("code_solution")
            solution_list.append(solution)
        solution = await self.mdensemble("code", solution_list, problem)
        solution = await self.tester(problem_id, problem, rephrase_problem, solution, test_cases)
        return solution

    async def review_revise_ensemble(self, problem: str, ensemble_count: int = 2, revise_round: int = 3):
        solution_list = []
        for _ in range(ensemble_count):
            solution = await self.single_solve(problem, revise_round)
            solution_list.append(solution)
        solution = await self.ensemble(solution_list, problem)
        return solution

    async def simple_ensemble(self, problem: str, ensemble_count: int = 3):
        solution_list = []
        for _ in range(ensemble_count):
            solution = await self.generate_code(problem)
            # solution = await self.generate_code_block(problem)
            solution = solution.get("code_solution")
            solution_list.append(solution)
        solution = await self.fuensemble(solution_list, problem)
        return solution

    async def single_solve(self, problem: str, max_loop: int):
        solution = await self.generate_code(problem)
        solution = solution.get("code_solution")
        for _ in range(max_loop):
            review_feedback = await self.review(problem, solution)
            if review_feedback["review_result"]:
                break
            solution = await self.revise(problem, solution, review_feedback["feedback"])
            solution = solution.get("revised_solution")
        return solution


class Gsm8kGraph(Graph):
    def __init__(self, name: str, llm: LLM, criteria: str, vote_count: int = 5) -> None:
        super().__init__(name, llm)
        self.criteria = criteria
        self.generate = Generate(llm=llm)
        self.rephrase = Rephrase(llm=llm)
        self.fuensemble = FuEnsemble(llm=llm)
        self.mdensemble = MdEnsemble(llm=llm, vote_count=vote_count)
        self.review = Review(llm=llm, criteria=criteria)
        self.revise = Revise(llm=llm)

    async def __call__(self, problem: str):
        formatted_problem = await self.rephrase.math_rephrase(problem)
        solution = await self.generate.math_generate(formatted_problem)  # 等待 generate 方法完成
        solution0 = solution['solution']
        formatted_solution = await self.generate.math_answer_format(solution0)
        return formatted_solution

    async def direct_test(self, problem: str):
        solution = await self.generate.direct_test(problem)  # 等待 generate 方法完成
        solution0 = solution['solution']
        formatted_solution = await self.generate.math_answer_format(solution0)
        return formatted_solution

    async def simple_ensemble(self, problem: str, ensemble_count: int = 3):
        formatted_problem = await self.rephrase.math_rephrase(problem)
        solution_list = []
        answer_list = []
        answer0_list = []
        for _ in range(ensemble_count):
            solution = await self.generate.math_generate(formatted_problem)
            # solution = await self.generate_code_block(problem)
            solution = solution.get("solution")
            answer = await self.generate.math_answer_format(solution)
            answer0 = answer.get("solution")
            solution_list.append(solution)
            answer_list.append(answer)
            answer0_list.append(answer0)

        if len(set(answer0_list)) == 1:
            formatted_solution = answer_list[0]
        else:
            solution = await self.mdensemble("math", solution_list, problem)
            solution0 = solution.get("final_solution")
            formatted_solution = await self.generate.math_answer_format(solution0)

        return formatted_solution

    async def single_solve(self, problem: str, max_loop: int = 3):
        formatted_problem = await self.rephrase.math_rephrase(problem)
        solution = await self.generate.math_generate(formatted_problem)  # 等待 generate 方法完成
        solution0 = solution['solution']
        for _ in range(max_loop):
            review_feedback = await self.review(formatted_problem, solution0)
            if review_feedback["review_result"]:
                break
            solution = await self.revise(formatted_problem, solution0, review_feedback["feedback"])
            solution = solution.get("revised_solution")
        formatted_solution = await self.generate.math_answer_format(solution)
        return formatted_solution

    async def cot_ensemble(self, problem: str, ensemble_count: int = 1):

        solution_list = []
        for _ in range(ensemble_count):
            core = await self.rephrase.math_core(problem)
            extract = await self.rephrase.math_extract(problem)
            formatted_problem = f"### Problem\n{problem}\n### Problem-Solving Info\n{extract}\n### Core Question\n{core}\n"
            solution = await self.generate.math_generate(formatted_problem)  # 等待 generate 方法完成
            # solution = await self.generate_code_block(problem)
            solution0 = solution.get("solution")
            solution_list.append(solution0)
        solution = await self.fuensemble(solution_list, problem)
        solution0 = solution['solution']
        formatted_solution = await self.generate.math_answer_format(solution0)

        return formatted_solution

    async def cot(self, problem: str):

        core = await self.rephrase.math_core(problem)
        extract = await self.rephrase.math_extract(problem)
        formatted_problem = f"### Problem\n{problem}\n### Problem-Solving Info\n{extract}\n### Core Question\n{core}\n"
        solution = await self.generate.math_generate(formatted_problem)  # 等待 generate 方法完成
        # solution = await self.generate_code_block(problem)
        solution0 = solution.get("solution")
        formatted_solution = await self.generate.math_answer_format(solution0)

        return formatted_solution


class HotpotQAGraph(Graph):
    def __init__(self, name: str, llm: LLM) -> None:
        super().__init__(name, llm)
        self.generate = Generate(llm=llm)
        self.rephrase = Rephrase(llm=llm)

    async def __call__(self, problem: str):
        solution = self.generate(problem)
        return solution
