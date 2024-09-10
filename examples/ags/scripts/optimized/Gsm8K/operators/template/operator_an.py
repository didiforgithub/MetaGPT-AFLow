from typing import List

from pydantic import BaseModel, Field


class GenerateOp(BaseModel):
    response: str = Field(default="", description="Your solution for this problem")


class FormatOp(BaseModel):
    solution: str = Field(default="", description="Your formatted answer for this problem")


class ReviewOp(BaseModel):
    review_result: bool = Field(
        default=False,
        description="The Review Result (Bool). If you think this solution looks good for you, return 'true'; If not, return 'false'",
    )
    feedback: str = Field(
        default="",
        description="Your FeedBack for this problem based on the criteria. If the review result is true, you can put it 'nothing here'.",
    )


class ReviseOp(BaseModel):
    solution: str = Field(default="", description="Based on the feedback, revised solution for this problem")


class FuEnsembleOp(BaseModel):
    thought: str = Field(
        default="",
        description="Analyze the solutions and think how to combine the advantages of various solutions to form the best possible solution.",
    )
    final_solution: str = Field(default="", description="Output the final solution after analysis and integration")


class MdEnsembleOp(BaseModel):
    thought: str = Field(
        default="""Example thought process:
                1. Examined the 'compare_one' function.
                2. The function correctly handles both numeric and string inputs by converting strings to floats.
                3. It properly compares two values and returns the larger one.
                4. The function returns None if the values are equal, which might be useful in some contexts but could be improved by returning either value.
                5. The use of 'isinstance' for type checking is a good practice.
                6. The function handles decimal separators well by replacing ',' with '.'.
                Overall, this solution effectively solves the problem of comparing two values, with good error handling and flexibility. It could be improved by specifying behavior for equal values, but it's a strong solution as is.""",
        description="Step-by-step analysis of the solutions to determine the best one.",
    )
    solution_letter: str = Field(default="", description="The letter of the chosen best solution (only one letter).")


class RephraseOp(BaseModel):
    rephrased_problem: str = Field(default="", description="Rephrased problem description for this problem")


class ScEnsembleOp(BaseModel):
    solution_letter: str = Field(default="", description="The letter of most consistent solution.")


class MathStepBreakdownOp(BaseModel):
    steps: List[str] = Field(default=[], description="A list of step-by-step instructions to solve the math problem")
    explanation: str = Field(default="", description="A brief explanation of the overall approach")


class MathStepBreakdownOp(BaseModel):
    steps: List[str] = Field(default=[], description="List of step-by-step solutions for the math problem")
    explanations: List[str] = Field(default=[], description="Detailed explanations for each step of the solution")


class MathStepByStepOp(BaseModel):
    steps: List[str] = Field(default=[], description="List of steps to solve the problem")
    final_answer: str = Field(default="", description="The final answer to the problem")
    explanation: str = Field(default="", description="A brief explanation of the solution process")