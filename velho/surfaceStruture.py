class SurfaceStruture:
    surfaceStruture = {}

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_value(self, valueText, base=0):
        if "%" in valueText:
            return (base * (float(valueText.split('%')[0]) / 100))
        elif "size" in valueText:
            return float(valueText.split('size')[0])
        else:
            return 0

    def get_local(self, params, contentWidth, contentHeight, orientation):
        if self.surfaceStruture.get(params[1]):
            width = self.surfaceStruture[params[1]]["width"]
            height = self.surfaceStruture[params[1]]["height"]
            x = self.surfaceStruture[params[1]]["local"][0]
            y = self.surfaceStruture[params[1]]["local"][1]

            if params[0] == "right" and orientation == "x":
                return x + width
            elif params[0] == "left" and orientation == "x":
                return x - contentWidth
            elif params[0] == "top" and orientation == "y":
                return y - contentHeight
            elif params[0] == "bottom" and orientation == "y":
                return y + height
            else:
                return 0

    def get_color(self, colorName):
        if colorName == "BLACK": return (0, 0, 0)
        elif colorName == "GRAY": return (40, 40, 40)
        elif colorName == "RED": return (255, 0, 0)
        elif colorName == "GREEN": return (0, 255, 0)
        elif colorName == "BLUE": return (0, 0, 255)
        elif colorName == "VIOLET": return (255, 0, 255)
        else: return (0, 0, 0)

    def get(self, name):
        if self.surfaceStruture.get(name):
            return self.surfaceStruture[name]
        else:
            return False

    def add_struture(self, name, struture):

        if not self.surfaceStruture.get(name):
            border = 0
            local = 0
            width = 0
            height = 0
            fillColor = 0
            color = 0
            xLocal = 0
            yLocal = 0

            if struture.get("border"):
                border = self.get_value(struture["border"],
                                             ((self.width + self.height) / 2))

            width = self.get_value(struture["width"], self.width) + (-1 * border)
            height = self.get_value(struture["height"], self.height) + (-1 * border)

            if struture.get("x-local"):
                xLocal = self.get_local(struture["x-local"], width, height,
                                        "x")
            if struture.get("y-local"):
                yLocal = self.get_local(struture["y-local"], width, height,
                                        "y")

            local = [xLocal, yLocal]

            if struture.get("local"):
                local = struture["local"]

            if type(local[0]) is str:
                local[0] = self.get_value(local[0], self.width)
                if local[0] == self.width:
                    local[0] -= width

            if type(local[1]) is str:
                local[1] = self.get_value(local[1], self.height)
                if local[1] == self.height:
                    local[1] -= height

            local[0] += border
            local[1] += border

            if struture.get("fill-color"):
                fillColor = self.get_color(struture["fill-color"])

            if struture.get("color"):
                color = self.get_color(struture["color"])

            self.surfaceStruture[name] = {
                "local": local,
                "width": width,
                "height": height,
                "fillColor": fillColor,
                "color": color
            }

            return True
        else:
            return False
