import os
import tree_sitter
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import openai
import argparse
from tree_sitter import Language, Parser
import evaluate
from evaluate import load

openai.api_key = 'YOUR_OPENAI_API_KEY'

def traverse_ast_rc(node,function_name,required_callee):
  ##If class is caller then all function becomes its callee else functions which are call within function becomes caller callee
  if (node.type=='function_definition' or node.type=='class_definition') and function_name is None:

    function_name = get_function_name(node)
    caller_callee_relation[function_name] = []
  
  elif node.type=='function_definition':

    if required_callee in node.children[1].text.decode:
      caller_callee_relation[function_name].append(node.children[1].text)
    
    function_name = node.children[1].text
    caller_callee_relation[function_name] = []

  elif node.type=='call':
      
      if required_callee in node.children[0].text.decode('ASCII'):
        caller_callee_relation[function_name].append(node.children[0].text)
  
  for child in node.children:
      traverse_ast_rc(child,function_name,required_callee)

def get_function_name(node):
  if node.type=='function_definition' or node.type=='class_definition':
     return node.children[1].text

def evaluate_correctness(original_code,transformed_code):
  exact_match_metric = load("exact_match")
  results = exact_match_metric.compute(predictions=transformed_code, references=original_code) #Original code here is my code where I have introduced loglevel
  return results

def correct_function_call(code,caller_name, callee_name, loglevel,argument):
    # Create a prompt for the LLM to generate a corrected function call
    prompt = f"Given the code,\n\n" \
             f"{code}" \
             f"Correct the function call:\n" \
             f"Caller: {caller_name}\n" \
             f"Callee: {callee_name}\n" \
             f"Log Level: {loglevel}\n" \
             f"{argument}"

    # Generate a corrected function call using LLM
    response = openai.Completion.create(
        engine="davinci-codex",  
        prompt=prompt,
        max_tokens=100
    )
    corrected_call = response.choices[0].text.strip()
    return corrected_call

def main(repo_path,required_callee,loglevel):
    argument1 = "Add loglevel argument in Caller and  display only the modified code not caller function"
    argument2 = "Add loglevel argument in Callee inside Caller and  display only the modified code not caller function"
    
    Language.build_library(
                            # Store the library in the `build` directory
                            f'{os.getcwd()}/build/my-languages.so',

                            # Include python languages
                            [
                              f'{os.getcwd()}/tree-sitter-python'
                            ]
                          )
    PY_LANGUAGE = Language('build/my-languages.so', 'python')
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    code = f.read()

                with open(os.path.join(root.replace('original','modified'), file), 'r') as f:
                    correct_code = f.read()
                
                # Step 1: Parse the tree
                tree = parser.parse(bytes(code, 'utf-8'))
                root_node = tree.root_node
                
                # Step 2: Identify caller-callee relations between functions
                global caller_callee_relation
                caller_callee_relation = {}
                traverse_ast_rc(root_node,None,required_callee)
                
                # Step 3: Use the LLM to modify the target function and function calls in the other classes as well

                for caller,callees in caller_callee_relation.items():
                   if len(callees)==0 and caller.decode('ASCII')==required_callee:
                      modified_code = correct_function_call(code,caller.decode('ASCII'),None,loglevel,argument1)
                   for callee in callees:
                      modified_code = correct_function_call(modified_code,caller.decode('ASCII'),callee.decode('ASCII'),loglevel,argument2)
                
                # Step4: Write the modified code by llm in modified_file

                with open(os.path.join(root, "modifed_" + file), 'w') as f:
                    f.write(modified_code)
                
                #Step5: Evaluate the correctness whether the modified code matches the generated code
                score = evaluate_correctness(correct_code,modified_code)


if __name__ == "__main__":
    
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--repo_path", type=str, default=".")
    arg_parser.add_argument("--required_callee", type=str, default="log")
    arg_parser.add_argument("--loglevel", type=str, default="debug")

    args = arg_parser.parse_args()

    main(args.repo_path,args.required_callee,args.loglevel)
