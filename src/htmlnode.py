class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join([f' {k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f'''\
tag: {self.tag}
value: {self.value}
children: {self.children and f'{len(self.children)} items'}
props: {self.props}
'''

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("leaf nodes must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children == None or len(children) == 0:
            raise ValueError("parent nodes must have children")
        if tag == None:
            raise ValueError("parent nodes must have a tag")
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
