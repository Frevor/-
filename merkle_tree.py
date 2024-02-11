import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, \
    QTreeWidget, QTreeWidgetItem, QStatusBar
from hashlib import sha256


class MerkleTree:

    def __init__(self):
        self.leaves = []

    def _hash_pair(self, left, right):
        return sha256((left + right).encode()).hexdigest()

    def build_tree(self):
        if not self.leaves:
            return []

        tree = [[(leaf, sha256(leaf.encode()).hexdigest()) for leaf in self.leaves]]

        while len(tree[-1]) > 1:
            level = []
            for i in range(0, len(tree[-1]), 2):
                left = tree[-1][i][1]
                if i + 1 < len(tree[-1]):
                    right = tree[-1][i + 1][1]
                else:
                    right = ''
                combined_hash = self._hash_pair(left, right)
                node = (f"{tree[-1][i][0]}_{right}", combined_hash)
                level.append(node)
            tree.append(level)

        return tree

    def insert_leaf(self, leaf):
        self.leaves.append(leaf)

    def delete_leaf(self, index):
        if 0 <= index < len(self.leaves):
            del self.leaves[index]


class MerkleTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Merkle Tree GUI")
        self.setGeometry(100, 100, 640, 480)
        self.merkle_tree = MerkleTree()
        self._setup_ui()

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.central_widget.setLayout(layout)

        label = QLabel("输入一个值:")
        layout.addWidget(label)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("在这里输入...")
        layout.addWidget(self.input_box)

        insert_button = QPushButton("插入节点")
        insert_button.clicked.connect(self.insert_node)
        layout.addWidget(insert_button)

        delete_button = QPushButton("删除节点")
        delete_button.clicked.connect(self.delete_node)
        layout.addWidget(delete_button)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Merkle Tree")
        layout.addWidget(self.tree_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QLabel {
                font: bold 14px;
            }
            QLineEdit {
                font: 12px;
                border: 1px solid #C0C0C0;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
            QPushButton {
                font: 12px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #39843c;
            }
            QTreeWidget {
                border: 1px solid #c0c0c0;
            }
        """)

    def insert_node(self):
        value = self.input_box.text()
        if value:
            self.merkle_tree.insert_leaf(value)
            self._update_tree()
            self.status_bar.showMessage("Node inserted", 2000)
            self.input_box.clear()

    def delete_node(self):
        item = self.tree_widget.currentItem()
        if item:
            index = self._get_index_of_item(item)
            if index is not None:
                self.merkle_tree.delete_leaf(index)
                self._update_tree()
                self.status_bar.showMessage("Node deleted", 2000)

    def _get_index_of_item(self, item):
        if item.parent() is None:
            return None
        parent_index = self.tree_widget.indexOfTopLevelItem(item.parent())
        if parent_index != 0:
            return None
        return item.parent().indexOfChild(item)

    def _update_tree(self):
        self.tree_widget.clear()
        for i, level in enumerate(self.merkle_tree.build_tree()):
            parent = QTreeWidgetItem(self.tree_widget, [f"Level {i}"])
            for node in level:
                node_text = f"{node[0]} ({node[1]})" if i == 0 else node[1]
                QTreeWidgetItem(parent, [node_text])
        self.tree_widget.expandAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MerkleTreeApp()
    window.show()
    sys.exit(app.exec())
