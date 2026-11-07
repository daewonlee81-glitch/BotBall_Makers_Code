import ast, sys, builtins, json
names = set(open(sys.argv[1]).read().split())
codes = json.load(open(sys.argv[2]))
bad = 0
for label, code in codes.items():
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print("SYNTAX", label, e); bad += 1; continue
    defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            f = n.func.id
            if f not in names and f not in defined and not hasattr(builtins, f):
                print("UNKNOWN FUNC", label, f); bad += 1
print("checked", len(codes), "programs; problems:", bad)
