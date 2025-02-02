import matplotlib.pyplot as plt


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.right = None
        self.left = None


class AVLTree:
    def __init__(self):
        self.root = None

    """Функция получения высоты дерева"""
    def get_height(self, node):
        if node:
            return node.height
        return 0

    """Левый поворот"""
    def left_rotate(self, node):
        y = node.right
        b = y.left
        y.left = node
        node.right = b

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        return y

    """Правый поворот"""
    def right_rotate(self, node):
        x = node.left
        b = x.right
        x.right = node
        node.left = b

        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

        return x

    """Функция получения разницы высот левого и правого поддеревьев"""
    def get_difference(self, node):
        if node:
            return self.get_height(node.left) - self.get_height(node.right)
        return 0

    """Функция балансировки АВЛ дерева"""
    def balance_node(self, node, key):
        difference = self.get_difference(node)

        # Малый левый поворот
        if difference > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Малый левый поворот
        if difference < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Большой правый поворот
        if difference > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Большой левый поворот
        if difference < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    """Функция нахождения узла с минимальным значением в поддереве"""
    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    """Поиск узла с заданным ключом"""
    def find(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self.find(node.left, key)
        return self.find(node.right, key)

    """Функция поиска для пользовательского взаимодействия"""
    def find_key(self, key):
        return self.find(self.root, key)

    """Рекурсивная вставка нового узла в дерево"""
    def insert(self, x, key):
        if not x:
            return AVLNode(key)
        if key < x.key:
            x.left = self.insert(x.left, key)
        else:
            x.right = self.insert(x.right, key)
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        return self.balance_node(x, key)

    """Функция вставки для пользовательского взаимодействия"""
    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    """Функция рекурсивного удаления узла из дерева."""
    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        return self.balance_node(node, key)

    """Функция удаления для пользовательского взаимодействия"""
    def delete_key(self, key):
        self.root = self.delete(self.root, key)

    """Функция подсчета количества узлов в дереве"""
    def count_nodes(self, node):
        if not node:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    """Функция подсчета количества элементов в дереве для пользовательского взаимодействия"""
    def count_elements(self):
        return self.count_nodes(self.root)

    """In-order обход"""
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    """Функция in-order обхода для пользовательского взаимодействия"""
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    """Pre-order обход"""
    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    """Функция pre-order обхода для пользовательского взаимодействия"""
    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    """Post-order обход"""
    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    """Функция post-order обхода для пользовательского взаимодействия"""
    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    """Функция проверки, является ли дерево AVL-деревом (сбалансированным)"""
    def is_balanced(self, node):
        if not node:
            return True
        balance = abs(self.get_difference(node)) <= 1
        return balance and self.is_balanced(node.left) and self.is_balanced(node.right)

    """Функция для визуализации"""
    def visualize(self):
        if not self.root:
            print("Дерево пустое")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        depth = self.get_height(self.root)  # Определяем глубину дерева

        root_x = 0
        root_y = depth * 20  # Поднимаем дерево вверх
        dx = 40  # Ширина ветвей
        dy = 20  # Высота уровней

        self._draw_tree(ax, self.root, root_x, root_y, dx, dy)

        ax.set_xlim(-dx * depth, dx * depth)  # Динамическое ограничение по ширине
        ax.set_ylim(-10, root_y + 10)  # Дерево начинается выше
        ax.axis("off")
        plt.show()

    def _draw_tree(self, ax, node, x, y, dx, dy):
        if node:
            ax.text(x, y, str(node.key), ha="center", va="center",
                    bbox=dict(facecolor="lightblue", edgecolor="black", boxstyle="circle"))

            if node.left:
                ax.plot([x, x - dx], [y - 3, y - dy], "k-")
                self._draw_tree(ax, node.left, x - dx, y - dy, dx * 0.6, dy)

            if node.right:
                ax.plot([x, x + dx], [y - 3, y - dy], "k-")
                self._draw_tree(ax, node.right, x + dx, y - dy, dx * 0.6, dy)


if __name__ == "__main__":
    tree = AVLTree()
    for key in [10, 20, 30, 40, 50, 25]:
        tree.insert_key(key)

    print("In-order:", tree.inorder())
    print("Pre-order:", tree.preorder())
    print("Post-order:", tree.postorder())
    print("Количество элементов в дереве:", tree.count_elements())
    print("Дерево сбалансировано:", tree.is_balanced(tree.root))

    print(tree.find_key(30).key)
    tree.delete_key(30)
    print(tree.inorder())
    tree.insert_key(35)
    print(tree.inorder())
    tree.visualize()
