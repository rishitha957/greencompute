import ast, astunparse

class StatementVisitor(ast.NodeVisitor):
    """Visits all the other nodes that are not constant nodes in AST"""
    def __init__(self) -> None:
        super(StatementVisitor, self).__init__()
        self.statement_map = {}
    def generic_visit(self,node):
        if not isinstance(node, ast.Constant):
            try:
                self.statement_map[type(node)] = ast.unparse(node)
            except TypeError:
                print("Can't parse ",type(node))
        ast.NodeVisitor.generic_visit(self,node)
    
class FuncVisitor(ast.NodeVisitor):
    """Visits all the FunctionDef Nodes in AST"""
    def __init__(self):
        super(FuncVisitor, self).__init__()
        # self.api_name = api_str
        self.func_map = {}
        self._func_names = []
        self._name_api_map = {}
        self._func_nodes = []
        self.func_dec_map = []
        self.func_call_map = {}

    def flatten_attr(self,node):
        """For Nested Decorators"""
        if isinstance(node, ast.Attribute):
            return str(self.flatten_attr(node.value)) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return str(node.id)
        else:
            pass

    def return_list(self):
        return self.func_dec_map

    def return_decorator_list(self, _func_nodes = None):
        if _func_nodes is None:
            _func_nodes = self._func_nodes
        for node in _func_nodes:
            found_decorators = []
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name):
                    found_decorators.append(decorator.id)
                elif isinstance(decorator, ast.Attribute):
                    found_decorators.append(self.flatten_attr(decorator))
                elif isinstance(decorator, ast.Call):
                    comment = ""
                    id1 = ""
                    attr1 = ""
                    for val_node in ast.walk(decorator):
                        if isinstance(val_node,ast.Name):
                            id1 = val_node.id
                        if isinstance(val_node,ast.Attribute):
                            attr1 = val_node.attr
                        if isinstance(val_node,ast.Constant):
                            comment = val_node.value
                    try:
                        found_decorators.append(id1+"."+attr1+" # "+comment)
                    except:
                        pass
            self.func_dec_map.append((node.name,found_decorators))
        return self.func_dec_map

    def generic_visit(self,node):
        if isinstance(node,ast.Call):
            self.func_call_map[node.func] = node
        elif isinstance(node,ast.FunctionDef):
            if node.name != "__init__":
                self.func_map[node.name] = node
                self._func_names.append(node.name.split(".")[-1])
                self._name_api_map[node.name.split(".")[-1]] = node.name
                self._func_nodes.append(node)
        else:
            sv = StatementVisitor()
            sv.visit(node)
        ast.NodeVisitor.generic_visit(self,node)

        
class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_map = {}
        self.func_def_map = {}
        self.func_call_map = {}
    def generic_visit(self,node):
        if isinstance(node, ast.ClassDef):
            self.class_map[node.name] = node
            fv = FuncVisitor()
            fv.visit(node)
            for f in fv.func_map:
                self.func_def_map[f] = fv.func_map[f]
            for f in fv.func_call_map:
                self.func_call_map[f] = fv.func_call_map[f]
        ast.NodeVisitor.generic_visit(self,node)