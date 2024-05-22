import torch
from torch import nn
from torchvision import transforms
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.ReLU()(x)
        x = self.conv2(x)
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2)(x)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = nn.ReLU()(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return nn.LogSoftmax(dim=1)(x)

model = Net()
model.load_state_dict(torch.load("mnist_cnn.pth"))
model.eval()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Digit Classifier")
        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.button_classify = tk.Button(root, text="Classify", command=self.classify)
        self.button_classify.pack()
        self.button_clear = tk.Button(root, text="Clear", command=self.clear)
        self.button_clear.pack()
        self.image = Image.new("L", (200, 200), 255)
        self.draw = ImageDraw.Draw(self.image)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=10)
        self.draw.line([x1, y1, x2, y2], fill="black", width=10)

    def classify(self):
        img = self.image.resize((28, 28)).convert('L')
        img = transforms.ToTensor()(img).unsqueeze(0)
        output = model(img)
        pred = output.argmax(dim=1, keepdim=True).item()
        messagebox.showinfo("Prediction", f"Predicted Digit: {pred}")

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (200, 200), 255)
        self.draw = ImageDraw.Draw(self.image)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
