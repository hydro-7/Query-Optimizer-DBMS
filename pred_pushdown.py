from graphviz import Digraph
import uuid
from parse import RANode, Relation, Selection, Projection, Join, Subquery, COLOR_MAP
import re

def extract_columns(condition: str):
    """Roughly extract identifiers like sq.a, t1.b from condition."""
    tokens = condition.replace('=', ' ').replace('<', ' ').replace('>', ' ').replace('<=', ' ').replace('>=', ' ').split()
    columns = set()
    for token in tokens:
        if '.' in token:
            # token should not be a a constant
            if not re.match(r'^\d+(\.\d+)?$', token):
                columns.add(token.strip())
    return columns

def get_aliases(node: RANode):
    """Collect the table‑alias identifiers in scope under this RA node."""
    # --- Relation case ---
    if isinstance(node, Relation):

        label = node._dot_label()        # e.g. "Table: foo AS bar"
        label = label.split('\n')[0]      # split off the cost
        name  = label.split("Table:")[1].strip()

        # Now `name` might be "foo", "foo AS bar", or "foo bar"
        alias = set()
        if ' AS ' in name:
            # explicit SQL alias            
            alias.add(name.split(' AS ')[1].strip())
            alias.add(name.split(' AS ')[0].strip())
        elif ' ' in name:
            # space‑separated fallback
            alias.add(name.split(' ')[1].strip())
            alias.add(name.split(' ')[0].strip())
        else:
            # no alias, use table name itself
            alias.add(name.strip())

        return alias

    if isinstance(node, Subquery):
        return {node.alias}

    if isinstance(node, (Selection, Projection)):
        return get_aliases(node.child)

    if isinstance(node, Join):
        return get_aliases(node.left) | get_aliases(node.right)

    return set()



def pushdown_selections(node: RANode) -> RANode:
    if isinstance(node, Selection):
        cond = node.condition.strip()
        if cond.upper().startswith("WHERE "):
            cond = cond[6:].strip()
        child = pushdown_selections(node.child)
        if re.search(r'\bAND\b', cond, flags=re.IGNORECASE):
            parts = [part.strip() for part in re.split(r'\bAND\b', cond, flags=re.IGNORECASE)]
            result = node.child
            for part in parts:
                result = pushdown_selections(Selection("WHERE " + part, result))
            return result

        if isinstance(child, Join):
            cond_cols = extract_columns(cond)
            left_aliases = get_aliases(child.left)
    
            if all(
                any(col.startswith(alias + '.') for alias in left_aliases)
                for col in cond_cols
            ):
                new_left = pushdown_selections(Selection("WHERE " + cond, child.left))
                return Join(new_left, child.right, child.condition)
            
        
            right_aliases = get_aliases(child.right)
            if all(
                any(col.startswith(alias + '.') for alias in right_aliases)
                for col in cond_cols
            ):
                new_right = pushdown_selections(Selection("WHERE " + cond, child.right))
                return Join(child.left, new_right, child.condition)

        return Selection("WHERE " + cond, child)

    elif isinstance(node, Projection):
        child = pushdown_selections(node.child)
        return Projection(node.columns, child)

    elif isinstance(node, Join):
        left  = pushdown_selections(node.left)
        right = pushdown_selections(node.right)
        return Join(left, right, node.condition)

    elif isinstance(node, Subquery):
        child = pushdown_selections(node.child)
        return Subquery(node.alias, child)
    
    else:
        return node

def visualize(ra_root: RANode, filename: str):
    dot = ra_root.to_dot()
    dot.format = 'png'
    dot.render(filename, view=False)
