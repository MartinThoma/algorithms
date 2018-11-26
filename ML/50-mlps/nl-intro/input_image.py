import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np
import keras
import hasy_tools


class ExampleApp(tk.Tk):
    def __init__(self):
        self.width = 128
        self.height = 128
        self.white = 255
        tk.Tk.__init__(self)
        self.previous_x = self.previous_y = 0
        self.x = self.y = 0
        self.points_recorded = []
        self.image1 = Image.new("L", (self.width, self.height), self.white)
        self.draw = ImageDraw.Draw(self.image1)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white", cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        # self.button_print = tk.Button(self, text = "Display points", command = self.print_points)
        # self.button_print.pack(side="top", fill="both", expand=True)
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        self.button_clear.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)
        self.model = keras.models.load_model('model.h5')
        data = hasy_tools.load_data()
        self.labels = data['labels']

    def clear_all(self):
        self.canvas.delete("all")
        self.image1 = Image.new("L", (self.width, self.height), self.white)
        self.draw = ImageDraw.Draw(self.image1)

    # def print_points(self):
    #     print(self.points_recorded)

    def tell_me_where_you_are(self, event):
        self.previous_x = event.x
        self.previous_y = event.y

    def draw_from_where_you_are(self, event):
        width = 10
        self.points_recorded.append([])
        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.previous_x, self.previous_y,
                                self.x, self.y, fill="black", width=width)
        # do the PIL image/draw (in memory) drawings
        black = 0
        self.draw.line([self.previous_x, self.previous_y,
                        self.x, self.y], black, width=width)
        self.points_recorded[-1].append(self.previous_x)
        self.points_recorded[-1].append(self.previous_y)
        self.points_recorded[-1].append(self.x)
        self.points_recorded[-1].append(self.x)
        self.previous_x = self.x
        self.previous_y = self.y

        filename = "my_drawing.png"
        img = autocrop(self.image1)
        img = img.resize((32, 32), Image.ANTIALIAS)
        img.save(filename)
        self.get_prediction(img)

    def get_prediction(self, input_img):
        input_img = np.array(input_img)
        input_img = input_img.reshape(1, 32, 32, 1)
        prediction = self.model.predict(hasy_tools.preprocess(input_img))
        highest_prob_index = prediction.argmax()
        proba = prediction[0][highest_prob_index]
        label = self.labels[highest_prob_index]
        print('{}: {:0.2f}%'.format(label, proba * 100))
        return label


def autocrop(image):
    import PIL.ImageOps
    inverted_image = PIL.ImageOps.invert(image)
    imageBox = inverted_image.getbbox()
    cropped = image.crop(imageBox)
    return cropped


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
