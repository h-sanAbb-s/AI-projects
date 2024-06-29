codeGenerationPrompt = """**Role**: You are a expert software python programmer. You need to develop python code
**Task**: As a programmer, you are required to complete the function. Use a Chain-of-Thought approach to break
down the problem, create pseudocode, and then write the code in Python language. Ensure that your code is
efficient, readable, and well-commented.

**Instructions**:
1. **Understand and Clarify**: Make sure you understand the task.
2. **Algorithm/Method Selection**: Decide on the most efficient way.
3. **Pseudocode Creation**: Write down the steps you will follow in pseudocode.
4. **Code Generation**: Translate your pseudocode into executable Python code

*REQURIEMENT*
{requirement}
"""

codeTestingPrompt="""
**Role**: As a tester, your task is to create Basic and Simple test cases based on provided Requirement and Python Code. 
These test cases should encompass Basic, Edge scenarios to ensure the code's robustness, reliability, and scalability.
**1. Basic Test Cases**:
- **Objective**: Basic and Small scale test cases to validate basic functioning 
**2. Edge Test Cases**:
- **Objective**: To evaluate the function's behavior under extreme or unusual conditions.
**Instructions**:
- Implement a comprehensive set of test cases based on requirements.
- Pay special attention to edge cases as they often reveal hidden bugs.
- Only Generate Basics and Edge cases which are small
- Avoid generating Large scale and Medium scale test case. Focus only small, basic test-cases
*REQURIEMENT*
{requirement}
**Code**
{code}
"""
codeExecutorPrompt="""You have to add testing layer in the *Python Code* that can help to execute the code. You need to pass only Provided Input as argument and validate if the Given Expected Output is matched.
*Instruction*:
- Make sure to return the error if the assertion fails
- Generate the code that can be execute
Python Code to excecute:
*Python Code*:{code}
Input and Output For Code:
*Input*:{input}
*Expected Output*:{output}"""

codeDebuggerPrompt = """You are expert in Python Debugging. You have to analysis Given Code and Error and generate code that handles the error
    *Instructions*:
    - Make sure to generate error free code
    - Generated code is able to handle the error
    
    *Code*: {code}
    *Error*: {error}
"""


