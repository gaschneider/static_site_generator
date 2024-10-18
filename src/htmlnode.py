from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        string_props = ""
        for kvp in self.props.items():
            key, value = kvp
            string_props += f' {key}="{value}"'

        return string_props
    
    def __repr__(self):
        tag = "" if self.tag is None else f"<{self.tag}>"
        value = "" if self.value is None else self.value
        children_count = "" if self.children is None else f" - Children count {len(self.children)}"
        props_desc = "" if self.props is None else f" - Props:{list(self.props.items())}"
        return f'{tag}{value}{children_count}{props_desc}'
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode should have value")
        
        if self.tag is None:
            return str(self.value)
        
        props_to_add = "" if self.props is None else self.props_to_html()

        if len(self.value) == 0:
            return f"<{self.tag}{props_to_add} />"

        return f"<{self.tag}{props_to_add}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode should have tag")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode should have children")
        
        props_to_add = "" if self.props is None else self.props_to_html()

        children_html = reduce(lambda c, n: c + n.to_html(), self.children, "")

        return f"<{self.tag}{props_to_add}>{children_html}</{self.tag}>"