
# These are import statements in Python, used to import necessary modules and packages for the program
# to run.
import tkinter as tk
import util
import cv2
import os
import subprocess
import datetime
from test import test
from PIL import Image, ImageTk

class App:
    def __init__(self):
        # These lines of code are creating a new instance of the Tkinter `Tk` class and setting it as
        # the `main_window` attribute of the `App` class. The `geometry` method is then used to set
        # the size and position of the window on the screen.
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x500+350+100")

        # These lines of code are creating a button labeled "LOGIN" with a green background color and
        # placing it at position (750, 300) on the main window. The button is also assigned to the
        # `self.login_button_main_window` attribute of the `App` class, and when clicked, it will call
        # the `login` method of the `App` class.
        self.login_button_main_window = util.get_button(self.main_window, "LOGIN", "green", self.login)
        self.login_button_main_window.place(x = 750, y= 300)
        
        # This code is creating a button labeled "REGISTER USER" with a white background color and
        # placing it at position (750, 400) on the main window. The button is also assigned to the
        # `self.register_user_button_main_window` attribute of the `App` class, and when clicked, it
        # will call the `register_new_user` method of the `App` class.
        self.register_user_button_main_window = util.get_button(self.main_window, "REGISTER USER", "white",self.register_new_user, fg="black")
        self.register_user_button_main_window.place(x = 750, y= 400)

        # These lines of code are creating a label widget for displaying the live video feed from the
        # webcam. The `util.get_img_label` function is used to create the label widget, and it is
        # placed at position (10, 0) on the main window with a height of 500 pixels and a width of 700
        # pixels. The label widget is then assigned to the `self.webcam_lable` attribute of the `App`
        # class.
        self.webcam_lable = util.get_img_label(self.main_window)
        self.webcam_lable.place(x=10, y =0,height= 500, width = 700)

        # `self.add_webcam(self.webcam_lable)` is calling the `add_webcam` method of the `App` class
        # and passing the `self.webcam_lable` attribute as an argument. This method initializes the
        # webcam capture and continuously updates the `self.most_recent_capture_arr` and
        # `self.most_recent_capture_pil` attributes with the most recent frame from the webcam. It
        # also updates the `self.webcam_lable` attribute with the most recent frame, allowing the live
        # video feed to be displayed on the GUI.
        self.add_webcam(self.webcam_lable)

        # These lines of code are creating a directory named "db" in the current working directory if
        # it does not already exist. The `self.db_dir` variable is set to the path of this directory,
        # which will be used later in the program to store images of registered users.
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, lable):
        # This code block is checking if the `cap` attribute is not already present in the dictionary
        # of instance variables (`__dict__`) of the `App` class. If it is not present, it initializes
        # the `cap` attribute with a new instance of the `cv2.VideoCapture` class, which captures
        # video from the default camera (index 0).
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        # `self.lable = lable` is assigning the `lable` parameter to the `self.lable` attribute of the
        # `App` class. This attribute is used to store the label widget that displays the live video
        # feed from the webcam.
        self.lable = lable
        self.process_webcam()

    def process_webcam(self):
       # This code block is capturing a frame from the webcam using the `cv2.VideoCapture` class and
       # storing it in the `frame` variable. The `ret` variable is a boolean value indicating whether
       # the frame was successfully captured or not.
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        # `img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)` is converting the
        # color space of the most recent frame captured by the webcam from BGR (Blue-Green-Red) to RGB
        # (Red-Green-Blue). This is necessary because OpenCV captures images in the BGR color space by
        # default, while most other image processing libraries and frameworks use the RGB color space.
        # Converting the color space ensures that the image is displayed correctly on the GUI and can
        # be processed by other libraries that use the RGB color space.
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        
        # These lines of code are converting the most recent frame captured by the webcam, which is
        # stored as a NumPy array in the `img_` variable, into a PIL (Python Imaging Library) image
        # object using the `Image.fromarray` method. The resulting PIL image is then stored in the
        # `self.most_recent_capture_pil` attribute of the `App` class.
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        self.lable.imgTk = imgtk
        self.lable.configure(image = imgtk)

        # `self.lable.after(20, self.process_webcam)` is scheduling the `process_webcam` method of the
        # `App` class to be called after a delay of 20 milliseconds. This creates a loop that
        # continuously captures frames from the webcam and updates the live video feed displayed on
        # the GUI. The `after` method is a built-in method of the Tkinter `Label` widget, which allows
        # for scheduling of method calls after a specified delay.
        self.lable.after(20, self.process_webcam)

    def login(self):

        # `lable = test(image = self.most_recent_capture_arr, model_dir = 'E:/python/LIVE
        # PROJECT/Face_Attendence_System/resources/anti_spoof_models', device_id = 0)` is calling the
        # `test` function from the `test` module and passing the most recent frame captured by the
        # webcam (`self.most_recent_capture_arr`), the directory path of the anti-spoofing models
        # (`'E:/python/LIVE PROJECT/Face_Attendence_System/resources/anti_spoof_models'`), and the
        # device ID of the camera (`0`) as arguments. The `test` function uses the anti-spoofing
        # models to determine whether the face in the captured frame is real or fake, and returns a
        # label (`lable`) indicating the result. If the label is `1`, the face is considered real, and
        # the program proceeds with face recognition. If the label is `0`, the face is considered
        # fake, and the program displays a message indicating that the user is a spoofer.
        lable = test(image = self.most_recent_capture_arr, model_dir = 'E:/python/LIVE PROJECT/Face_Attendence_System/resources/anti_spoof_models', device_id = 0)

        if lable == 1:

            unknown_img_path = "./.tmp.jpg"
            cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

            # This code is using the `subprocess` module to run the `face_recognition` command-line
            # tool with the `self.db_dir` and `unknown_img_path` arguments. The output of the command
            # is captured as a byte string and then converted to a regular string using the `str`
            # function. The resulting string is then split using the comma as a delimiter, and the
            # second element of the resulting list (index 1) is selected. This element contains the
            # name of the recognized person, which is extracted by slicing the string to remove any
            # trailing characters (such as whitespace or quotes) using the `[:-3]` syntax. The
            # resulting name is then stored in the `name` variable for further processing.
            output  = str(subprocess.check_output(["face_recognition", self.db_dir,unknown_img_path]))
            name = output.split(',')[1][:-3]

            # This code block is checking if the `name` variable, which contains the name of the
            # recognized person, is equal to either `'unknown_person'` or `'no_person_found'`. If it
            # is, it means that the face in the captured frame was not recognized as belonging to any
            # registered user, and a message box is displayed with the message "Unknown user. Please
            # register and Try Again." If the `name` variable contains the name of a recognized user,
            # a message box is displayed with the message "Welcome back!!!" followed by the name of
            # the recognized user. The name of the recognized user and the current date and time are
            # also written to a log file specified by the `self.log_path` attribute of the `App`
            # class.
            if name in ['unknown_person','no_person_found']:
                util.msg_box("Oops...", "Unknown user. Please register and Try Again.")
            else:
                util.msg_box("Welcome back!!!","Welcome {}".format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{}\n'.format(name,datetime.datetime.now()))
                    f.close()
    
        else:
            util.msg_box("You are a spoofer!!", "You are fake!")

    def register_new_user(self):
        # The below code is creating a new window (Toplevel) in a tkinter GUI application with the
        # name "register_new_user_window". The window is set to have a size of 1200x500 pixels and is
        # positioned at coordinates (350, 100) on the screen.
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x500+350+100")

        # The below code is creating a button named "accept_button_main_window" in a window named
        # "register_new_user_window". The button is colored green and has the text "ACCEPT" on it.
        # When the button is clicked, it will call the function "accept_register_new_user". The button
        # is then placed at coordinates (750, 300) within the window.
        self.accept_button_main_window = util.get_button(self.register_new_user_window, "ACCEPT", "green", self.accept_register_new_user)
        self.accept_button_main_window.place(x = 750, y= 300)
        
        # The below code is creating a button named "TRY AGAIN" with white background and black
        # foreground color on the "register_new_user_window" window. When the button is clicked, it
        # will call the "try_again_register_new_user" function. The button is then placed at the
        # coordinates (750, 400) on the window.
        self.try_again_button_main_window = util.get_button(self.register_new_user_window, "TRY AGAIN", "white",self.try_again_register_new_user, fg="black")
        self.try_again_button_main_window.place(x = 750, y= 400)

        # The below code is setting an image label in a GUI window for registering a new user. The
        # `util.get_img_label()` function is used to retrieve the image label object, which is then
        # assigned to the `self.capture_lable` variable. The `place()` method is then used to position
        # and size the image label within the window.
        self.capture_lable = util.get_img_label(self.register_new_user_window)
        self.capture_lable.place(x=10, y =0,height= 500, width = 700)

        # The below code is calling a method `add_img_to_lable` with an argument `self.capture_lable`.
        # It is likely a method defined in a class and is used to add an image to a label in a
        # graphical user interface (GUI) application. However, without more context or information
        # about the class and its methods, it is difficult to provide a more specific answer.
        self.add_img_to_lable(self.capture_lable)

        # The below code is creating a text entry widget for the "register new user" window and
        # placing it at coordinates (750, 150) on the window. The text entered by the user in this
        # widget can be retrieved using the `get()` method.
        self.entery_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entery_text_register_new_user.place(x=750 ,y=150)

        # The below code is creating a text label widget in a GUI window for registering a new user.
        # The label displays the text "ENTER YOUR NAME". The `util.get_text_label` function is used to
        # create the label widget and the `place` method is used to position the label on the window
        # at coordinates (750, 70).
        self.text_lable_register_new_user = util.get_text_label(self.register_new_user_window, "ENTER YOUR NAME")
        self.text_lable_register_new_user.place(x=750,y=70)

    def try_again_register_new_user(self):
        # The below code is likely a snippet from a Python program and it is calling the `destroy()`
        # method on the `register_new_user_window` object. This method is likely used to close or
        # destroy the window associated with the `register_new_user_window` object.
        self.register_new_user_window.destroy()

    def add_img_to_lable(self, lable):
        # The below code is updating the image displayed in a label widget with the most recent
        # capture image in a Python GUI application. It first creates an ImageTk object from the most
        # recent capture image using the ImageTk.PhotoImage() method. Then it sets the imgTk attribute
        # of the label widget to the created ImageTk object and configures the image displayed in the
        # label widget to be the created ImageTk object.
        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        lable.imgTk = imgtk
        lable.configure(image = imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        # The below code is retrieving the text entered in a tkinter Entry widget with the name
        # "entery_text_register_new_user" and storing it in a variable called "name". The text is
        # retrieved from the first character (1.0) to the end of the text in the widget ("end-1c").
        # The "-1c" is used to exclude the newline character at the end of the text.
        name = self.entery_text_register_new_user.get(1.0, "end-1c")

        # The below code is saving an image of a newly registered user's face capture in a directory
        # specified by `self.db_dir`. The image is saved with the name `name.jpg`. The image is
        # obtained from `self.register_new_user_capture`. The `cv2.imwrite()` function is used to
        # write the image to the specified directory.
        cv2.imwrite(os.path.join(self.db_dir, "{}.jpg".format(name)), self.register_new_user_capture)

        util.msg_box("Success","Registered Successfully!!!")

        self.register_new_user_window.destroy()


    def start(self):
        self.main_window.mainloop()


if __name__ == '__main__':
    app = App()
    app.start()
