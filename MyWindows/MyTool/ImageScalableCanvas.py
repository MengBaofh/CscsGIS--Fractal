from tkinter import *
from PIL import Image, ImageTk


class ISCanvas(Canvas):
    """
    可以缩放图片的画布
    """
    imscale = 1.0
    imagetk = None
    height = None  # 图片高
    width = None  # 图片宽
    image = None  # 图片
    imagePath = None  # 图片路径

    def __init__(self, master, imagePath, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master
        self.setImage(imagePath)
        self.imscale = 1.0  # scale for the canvas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.create_rectangle(0, 0, self.width, self.height, width=0)
        self.bindEvent()
        # self.showMyImage()

    def setImage(self, imagePath):
        """
        添加待显示的图片
        :param imagePath: 图片路径
        :return:
        """
        self.imagePath = imagePath
        self.image = Image.open(self.imagePath)
        self.width, self.height = self.image.size

    def bindEvent(self):
        self.bind('<Configure>', self.showMyImage)
        self.bind('<ButtonPress-1>', self.move_from)
        self.bind('<B1-Motion>', self.move_to)
        self.bind('<MouseWheel>', self.wheel)  # Windows\MacOS
        self.bind('<Button-4>', self.wheel)  # Linux上滚
        self.bind('<Button-5>', self.wheel)  # Linux下滚

    def scroll_y(self, *args, **kwargs):
        """
        竖直滚动并重新显示图片
        :param args:
        :return:
        """
        self.yview(*args, **kwargs)
        self.showMyImage()

    def scroll_x(self, *args, **kwargs):
        """
        水平滚动并重新显示图片
        :param args:
        :return:
        """
        self.xview(*args, **kwargs)
        self.showMyImage()

    def move_from(self, event):
        """
        记录开始移动的坐标
        :param event:
        :return:
        """
        self.scan_mark(event.x, event.y)

    def move_to(self, event):
        """
        移动后的
        :param event:
        :return:
        """
        self.scan_dragto(event.x, event.y, gain=1)
        self.showMyImage()

    def wheel(self, event):
        """
        滚轮缩放
        :param event:
        :return:
        """
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        bbox = self.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            pass  # Ok! Inside the image
        else:
            return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30:
                return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.winfo_width(), self.winfo_height())
            if i < self.imscale:
                return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale *= self.delta
        self.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.showMyImage()

    def showMyImage(self, event=None):
        """
        显示图片
        :return:
        """
        bbox1 = self.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvasx(0),  # get visible area of the canvas
                 self.canvasy(0),
                 self.canvasx(self.winfo_width()),
                 self.canvasy(self.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)  # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]), anchor='nw', image=imagetk)
            self.lower(imageid)  # set image into background
            self.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
