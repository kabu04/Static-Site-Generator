class HTMLNode:
    
    # tag : html tag as string
    # value : string representing value inside html tag
    # children : list of htmlnode objects 
    # props : attributes of the html tag 
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        prop_string = ""

        for prop in self.props:
            prop_string += " " + prop + "=" + f'"{self.props[prop]}"'
        return prop_string
    
    def __repr__(self) -> str:
        return f"HTMLNode:\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    # renders leaf node as HTML string
    def to_html(self):
        if self.value == None:
            raise ValueError("No value for leaf node")

        if self.tag == None:
            return self.value
        else:
            open_tag = f"<{self.tag}{self.props_to_html()}>"
            closing_tag = f"</{self.tag}>"
            return open_tag + self.value + closing_tag
        
    def __repr__(self) -> str:
        return f"LeafNode:\ntag: {self.tag}\nvalue: {self.value}\nprops: {self.props}"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided parent class")
        if self.children == None: 
            raise ValueError("No child of parent class")

        open_tag = f"<{self.tag}{self.props_to_html()}>"
        content = ""
        for c in self.children:
            content += c.to_html()
        closing_tag = f"</{self.tag}>"
        return open_tag + content + closing_tag

