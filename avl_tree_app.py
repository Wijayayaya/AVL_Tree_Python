import tkinter as tk
from tkinter import simpledialog, messagebox

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def find(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self.find(root.left, key)
        return self.find(root.right, key)

    def inorder_traversal(self, root):
        return self.inorder_traversal(root.left) + [root.key] + self.inorder_traversal(root.right) if root else []

    def preorder_traversal(self, root):
        return [root.key] + self.preorder_traversal(root.left) + self.preorder_traversal(root.right) if root else []

    def postorder_traversal(self, root):
        return self.postorder_traversal(root.left) + self.postorder_traversal(root.right) + [root.key] if root else []

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

class AVLTreeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AVL Tree Visualizer")
        self.geometry("800x600")
        self.tree = AVLTree()
        self.root = None

        self.canvas = tk.Canvas(self, width=800, height=500, bg="white")
        self.canvas.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.insert_button = tk.Button(self.button_frame, text="Insert", command=self.insert_value)
        self.insert_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_value)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.find_button = tk.Button(self.button_frame, text="Find", command=self.find_value)
        self.find_button.pack(side=tk.LEFT, padx=5)
        self.inorder_button = tk.Button(self.button_frame, text="Inorder", command=self.show_inorder)
        self.inorder_button.pack(side=tk.LEFT, padx=5)
        self.preorder_button = tk.Button(self.button_frame, text="Preorder", command=self.show_preorder)
        self.preorder_button.pack(side=tk.LEFT, padx=5)
        self.postorder_button = tk.Button(self.button_frame, text="Postorder", command=self.show_postorder)
        self.postorder_button.pack(side=tk.LEFT, padx=5)

    def insert_value(self):
        value = simpledialog.askinteger("Insert", "Enter a value to insert:")
        if value is not None:
            self.root = self.tree.insert(self.root, value)
            messagebox.showinfo("Insert", f"Inserted {value} into the AVL Tree")
            self.update_canvas()

    def delete_value(self):
        value = simpledialog.askinteger("Delete", "Enter a value to delete:")
        if value is not None:
            self.root = self.tree.delete(self.root, value)
            messagebox.showinfo("Delete", f"Deleted {value} from the AVL Tree")
            self.update_canvas()

    def find_value(self):
        value = simpledialog.askinteger("Find", "Enter a value to find:")
        if value is not None:
            node = self.tree.find(self.root, value)
            if node:
                messagebox.showinfo("Find", f"Value {value} found in the AVL Tree")
            else:
                messagebox.showinfo("Find", f"Value {value} not found in the AVL Tree")

    def show_inorder(self):
        nodes = self.tree.inorder_traversal(self.root)
        messagebox.showinfo("Inorder Traversal", f"Inorder: {nodes}")

    def show_preorder(self):
        nodes = self.tree.preorder_traversal(self.root)
        messagebox.showinfo("Preorder Traversal", f"Preorder: {nodes}")

    def show_postorder(self):
        nodes = self.tree.postorder_traversal(self.root)
        messagebox.showinfo("Postorder Traversal", f"Postorder: {nodes}")

    def update_canvas(self):
        self.canvas.delete("all")
        if self.root:
            self.draw_tree(self.root, 400, 30, 200)

    def draw_tree(self, node, x, y, x_offset):
        if node:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node.key), font=("Arial", 15, "bold"))

            if node.left:
                self.canvas.create_line(x-10, y+10, x-x_offset+10, y+60-10)
                self.draw_tree(node.left, x-x_offset, y+60, x_offset//2)

            if node.right:
                self.canvas.create_line(x+10, y+10, x+x_offset-10, y+60-10)
                self.draw_tree(node.right, x+x_offset, y+60, x_offset//2)

if __name__ == "__main__":
    app = AVLTreeApp()
    app.mainloop()