import math
import copy

class WorldModel:

    #در این تابع مختصات نقاط مکعب ها را میگیریم. در ابتدا اگر این مکعب ها به صورت یک خط باشند و هنوز جمع نشده باشند مکعب ها را از یک سر شماره گذاری میکنیم و مختصات مکعب ها را بر اساس شماره شان در یک آرایه مختصات جدید میگذاریم وگرنه به همان صورتی که مختصات ها را ورودی گرفته ایم آنها را مورد استفاده قرار میدهیم
    def __init__(self, Coordinates, sticky_cubes):
        tmp_cor = copy.deepcopy(Coordinates)
        flag = True
        #در ابتدا سر رشته مکعب ها را پیدا میکنیم. سر رشته، آن مکعبی است که تنها یک مکعب مجاور دارد با مقایسه مکعب ها نسبت به هم سر رشته را پیدا میکنیم. اگر سری وجود نداشت همان آرایه ورودی را برای مکعب ها به کار میگیریم
        for i in range(len(Coordinates)):
            count = 0
            for j in range(len(Coordinates)):
                different = abs(Coordinates[i][0] - Coordinates[j][0]) + abs(Coordinates[i][1] - Coordinates[j][1]) + abs(Coordinates[i][2] - Coordinates[j][2])
                if different == 1:
                    count += 1
            if(count == 1):
                self.Coordinates = []
                self.Coordinates.append(Coordinates[i])
                del Coordinates[i]
                flag = False
                break
        if (flag):
            self.Coordinates = []
            for item in Coordinates:
                cor = [0,0,0]
                cor[0] = item[0]
                cor[1] = item[1]
                cor[2] = item[2]
                self.Coordinates.append(cor)
            self.sticky_cubes = sticky_cubes
            for item in self.sticky_cubes:
                    if (item[0] > item[1]):
                        tmp = item[0]
                        item[0] = item[1]
                        item[1] = tmp
            return
        length = len(Coordinates)
        #حال با پیدا شدن سر رشته مکعب ها به ترتیب آنها را شماره گذاری میکنیم اگر اینکار ممکن نبود از همان آرایه ورودی مختصات مکعب ها بهره میبریم
        for i in range(length):
            last = len(self.Coordinates)
            count = 0
            place = 0
            for j in range(len(Coordinates)):
                different = abs(self.Coordinates[last-1][0] - Coordinates[j][0]) + abs(self.Coordinates[last-1][1] - Coordinates[j][1]) + abs(self.Coordinates[last-1][2] - Coordinates[j][2])
                if different == 1:
                    count += 1
                    place = j
            if(count == 1 or last == 1):
                self.Coordinates.append(Coordinates[place])
                del Coordinates[place]
            if(count != 1):
                self.Coordinates = tmp_cor
                self.sticky_cubes = sticky_cubes
                for item in self.sticky_cubes:
                    if (item[0] > item[1]):
                            tmp = item[0]
                            item[0] = item[1]
                            item[1] = tmp
                return
        self.sticky_cubes = sticky_cubes
        for item in self.sticky_cubes:
            if(item[0] > item[1]):
                tmp = item[0]
                item[0] = item[1]
                item[1] = tmp
        #در ضمن در آرایه مکعب های چسبیده کاری میکنیم که در هر خانه، که دو مکعب چسبیده به هم معرفی شده اند مکعب با شماره کمتر در سمت چپ  مکعب با شماره بیشتر باشد.

    #وضعیت فعلی یعنی مختصات ها و مکعب های چسبیده را به صورت دیکشنری میدهد
    def cur_state(self):
        return {"Coordinates":self.Coordinates,"sticky_cubes":self.sticky_cubes}

    # در حالت نهایی بیشترین فاصله دو مکعب حداکثر جذر 9 است در اینجا فاصله هر دو مکعب داخل شبیه ساز را مقایشه میکنیم اگر تمام فاصله ها از جذر 9 کمتر بودند میگوییم در حالت نهایی هستیم
    def goal_state(self):
        for cube1 in self.Coordinates:
            for cube2 in self.Coordinates:
                if ((((cube1[0] - cube2[0]) ** 2) + ((cube1[1] - cube2[1]) ** 2) + ((cube1[2] - cube2[2]) ** 2)) ** 2) >= 9:
                    return False
        return True

    #این تابع برای اینست که مکعب با شماره cur_cube در راستای مکعب با شماره before_cube به اندازه action دوران پیدا کند
    def take_action(self, cur_cube, before_cube, action):
        # در ابتدا یک کپی از مختصات ها قبل از تغییر میگیریم این برای آن هست که که اگر بعد از تغییر مختصات ها دیدیم مختصات دو مکعب یکی شده است مختصات ها را به حالت اول برگردانیم
        tmp_Coordinates = []
        for section in self.Coordinates:
            point = [0,0,0]
            point[0] = section[0]
            point[1] = section[1]
            point[2] = section[2]
            tmp_Coordinates.append(point)

        #با توجه به cur_cube و before_cube راستای چرخش را بدست می آوریم
        if (self.Coordinates[before_cube - 1][0] != self.Coordinates[cur_cube - 1][0]):
            inline = 'x'
        if (self.Coordinates[before_cube - 1][1] != self.Coordinates[cur_cube - 1][1]):
            inline = 'y'
        if (self.Coordinates[before_cube - 1][2] != self.Coordinates[cur_cube - 1][2]):
            inline = 'z'

        #نسبت به مکعبی که باید چرخش کند(با توجه به مکعب های چسبیده به هم) به سمت راست و چپ میرویم تا در چپ و راست به مکعب هایی برسیم که دم پله ها هستند چرا که مختصات ها هم در چپ و هم در راست مکعب فعلی از این مکعب ها به بعد تغییر میکنند
        lcube = self.find_leftmost_inlineandsticky_cube(cur_cube, inline)
        rcube = self.find_rightmost_inlineandsticky_cube(cur_cube, inline)


        #با توجه به سمت راست یا چپ مکعب  فعلی بودن و راستا، عمل چرخش را انجام میدهیم
        if(lcube != 1):
            if(inline == 'x' and self.Coordinates[lcube - 1][0] == self.Coordinates[lcube - 2][0]):
                self.do_rotate(inline, cur_cube, action, 'left')
            if(inline == 'y' and self.Coordinates[lcube - 1][1] == self.Coordinates[lcube - 2][1]):
                self.do_rotate(inline, cur_cube, action, 'left')
            if(inline == 'z' and self.Coordinates[lcube - 1][2] == self.Coordinates[lcube - 2][2]):
                self.do_rotate(inline, cur_cube, action, 'left')

        if(rcube != 27):
            if (inline == 'x' and self.Coordinates[rcube][0] == self.Coordinates[rcube - 1][0]):
                self.do_rotate(inline, cur_cube, action, 'right')
            if (inline == 'y' and self.Coordinates[rcube][1] == self.Coordinates[rcube - 1][1]):
                self.do_rotate(inline, cur_cube, action, 'right')
            if (inline == 'z' and self.Coordinates[rcube][2] == self.Coordinates[rcube - 1][2]):
                self.do_rotate(inline, cur_cube, action, 'right')

        #اگر بعد از چرخش دو مکعب مختصات یکسان داشتند مختصات ها را به حالت اول برمیگردانیم و خروجی صفر میدهیم تا در تابع ai بفهمانیم که این حالت ها را داخل صف نفرستد چرا که تکراری هستند
        count = 0
        for item1 in self.Coordinates:
            for item2 in self.Coordinates:
                if ((item1[0] == item2[0]) and (item1[1] == item2[1]) and (item1[2] == item2[2])):
                        count += 1
        if count > len(self.Coordinates):
            index = 0
            for item in tmp_Coordinates:
                self.Coordinates[index][0] = item[0]
                self.Coordinates[index][1] = item[1]
                self.Coordinates[index][2] = item[2]
                index += 1
            return 0
        return 1

    def find_leftmost_inlineandsticky_cube(self, cube_number, inline):
        cube_number_cp = cube_number
        leftmost_cube = cube_number_cp
        for item in self.sticky_cubes:
            if(item[1] == leftmost_cube):
                if(inline == 'x'):
                    if(abs(self.Coordinates[item[0]-1][0] - self.Coordinates[item[1]-1][0]) == 1):
                        leftmost_cube = item[0]
                if (inline == 'y'):
                    if (abs(self.Coordinates[item[0] - 1][1] - self.Coordinates[item[1] - 1][1]) == 1):
                        leftmost_cube = item[0]
                if (inline == 'z'):
                    if (abs(self.Coordinates[item[0] - 1][2] - self.Coordinates[item[1] - 1][2]) == 1):
                        leftmost_cube = item[0]
        while(leftmost_cube != cube_number_cp):
            cube_number_cp -= 1
            for item in self.sticky_cubes:
                if (item[1] == leftmost_cube):
                    if (inline == 'x'):
                        if (abs(self.Coordinates[item[0] - 1][0] - self.Coordinates[item[1] - 1][0]) == 1):
                            leftmost_cube = item[0]
                    if (inline == 'y'):
                        if (abs(self.Coordinates[item[0] - 1][1] - self.Coordinates[item[1] - 1][1]) == 1):
                            leftmost_cube = item[0]
                    if (inline == 'z'):
                        if (abs(self.Coordinates[item[0] - 1][2] - self.Coordinates[item[1] - 1][2]) == 1):
                            leftmost_cube = item[0]
        return leftmost_cube

    def find_rightmost_inlineandsticky_cube(self, cube_number, inline):
        cube_number_cp = cube_number
        rightmost_cube = cube_number_cp
        for item in self.sticky_cubes:
            if(item[0] == rightmost_cube):
                if(inline == 'x'):
                    if(abs(self.Coordinates[item[0]-1][0] - self.Coordinates[item[1]-1][0]) == 1):
                        rightmost_cube = item[1]
                if (inline == 'y'):
                    if (abs(self.Coordinates[item[0] - 1][1] - self.Coordinates[item[1] - 1][1]) == 1):
                        rightmost_cube = item[1]
                if (inline == 'z'):
                    if (abs(self.Coordinates[item[0] - 1][2] - self.Coordinates[item[1] - 1][2]) == 1):
                        rightmost_cube = item[1]
        while(rightmost_cube != cube_number_cp):
            cube_number_cp += 1
            for item in self.sticky_cubes:
                if (item[0] == rightmost_cube):
                    if (inline == 'x'):
                        if (abs(self.Coordinates[item[0] - 1][0] - self.Coordinates[item[1] - 1][0]) == 1):
                            rightmost_cube = item[1]
                    if (inline == 'y'):
                        if (abs(self.Coordinates[item[0] - 1][1] - self.Coordinates[item[1] - 1][1]) == 1):
                            rightmost_cube = item[1]
                    if (inline == 'z'):
                        if (abs(self.Coordinates[item[0] - 1][2] - self.Coordinates[item[1] - 1][2]) == 1):
                            rightmost_cube = item[1]
        return rightmost_cube

    def do_rotate(self, inline, cube_number, action, right_or_left):
        if(action == -90):
            if(right_or_left == 'right'):
                for number in range(cube_number, 27):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], -math.pi/2)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]
            if(right_or_left == 'left'):
                for number in range(0, cube_number - 1):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], -math.pi/2)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]
        if(action == 90):
            if (right_or_left == 'right'):
                for number in range(cube_number, 27):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], math.pi/2)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]
            if (right_or_left == 'left'):
                for number in range(0, cube_number - 1):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], math.pi/2)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]
        if(action == 180):
            if (right_or_left == 'right'):
                for number in range(cube_number, 27):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], math.pi)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]
            if (right_or_left == 'left'):
                for number in range(0, cube_number - 1):
                    new_coordinate = self.rotate(inline, self.Coordinates[cube_number - 1], self.Coordinates[number], math.pi)
                    self.Coordinates[number][0] = new_coordinate[0]
                    self.Coordinates[number][1] = new_coordinate[1]
                    self.Coordinates[number][2] = new_coordinate[2]

    #بر اساس ماتریس، چرخش را انجام میدهد
    def rotate(self, inline,origin, point, angle):
        # Rotate a point counterclockwise by a given angle around a given origin.
        # The angle should be given in radians.
        old_x = point[0]
        old_y = point[1]
        old_z = point[2]
        if(inline == 'x'):
            x = old_x
            y = origin[1] + math.cos(angle) * (point[1] - origin[1]) - math.sin(angle) * (point[2] - origin[2])
            z = origin[2] + math.sin(angle) * (point[1] - origin[1]) + math.cos(angle) * (point[2] - origin[2])
            return [round(x), round(y), round(z)]
        if(inline == 'y'):
            y = old_y
            x = origin[0] + math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[2] - origin[2])
            z = origin[2] + math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[2] - origin[2])
            return [round(x), round(y), round(z)]
        if(inline == 'z'):
            z = old_z
            x = origin[0] + math.cos(angle) * (point[0] - origin[0]) - math.sin(angle) * (point[1] - origin[1])
            y = origin[1] + math.sin(angle) * (point[0] - origin[0]) + math.cos(angle) * (point[1] - origin[1])
            return [round(x), round(y), round(z)]