from PyQt5.QtCore import *
from eMind_conf import *
from eMind_node_base import *
from nodeeditor.utils import dumpException

#@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 + input2


@register_node(OP_NODE_SUB)
class eMindNode_func(CalcNode):
    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Func"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def initInnerClasses(self):
        self.content = FuncInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalOperation(self, input1, input2):
        return input1 - input2

#@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def evalOperation(self, input1, input2):
        print('foo')
        return input1 * input2

#@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def evalOperation(self, input1, input2):
        return input1 / input2


class FuncInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("1", self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res
# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)