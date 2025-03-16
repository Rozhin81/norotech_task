import ast

class Analyze:
    def __init__(self,code:str):
        self.code = code

    def analyze_code(self):
        suggestions = []
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # check having docstring
                    if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant)):
                        suggestions.append("Add a docstring for better documentation.")
                    # check having type hints
                    for arg in node.args.args:
                        if arg.annotation is None:
                            suggestions.append("Consider adding type hints.")
        except SyntaxError:
            suggestions.append("Invalid Python syntax.")
        return suggestions