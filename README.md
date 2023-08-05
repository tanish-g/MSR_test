# MSR Internship Assignment

## Problem 

In this assignment, you will be developing a small end to end module to transform files in code repository using large language models.

Use TreeSitter (Tree-sitter｜Introduction) to parse an example code repository (C#/Java/Python) and form a graph structure on top it. 
Nodes of this graph can be AST nodes and edges can be various relations you define using these nodes.
We are particularly interested in function nodes and caller-callee relations. Feel free to introduce other relations.
Here is an example scenario. 
Let's say we have a function log(str) defined in one of the class, and it gets called at various locations across classes.
Using an LLM, construct appropriate calls and add a "loglevel" argument into this method, and change the logging statement accordingly. So the function now looks like log(str, loglevel)
Using TreeSitter based output and LLM, correct the function calls in the other classes as well
The problem statement is left intentionally vague. Please make appropriate assumptions while implementing this. 
Your code should run out of the box. We will be examining the implementation quality and test cases which you write.
You can use different models hosted in HuggingFace, two of them are
https://huggingface.co/WizardLM/WizardCoder-15B-V1.0 and https://huggingface.co/Salesforce/instructcodet5p-16b. But you are free to use other models.
Design a suitable method/metric/test to evaluate the correctness of your transform

### Requirement installation

```
bash install.sh
```

### How to run file

```
python run.py --repo_path 'path_to_repo' --corr_repo_path 'path_to_correct_repo' --required_callee 'log' --loglevel 'debug'
```


Used Chat gpt api because was not able to use heavy transformer models like wizard coder and  instruct code on free tier of colab

https://github.com/tanish-g/MSR_test/assets/55942819/e5e450d1-3fdc-4210-a0e5-8345d03d2457










