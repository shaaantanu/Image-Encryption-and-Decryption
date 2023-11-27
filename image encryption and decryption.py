import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np

class ImageEncryptDecryptApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Image Encryption Decryption")

        # Initialize variables
        self.panelA = None
        self.panelB = None
        self.image_path = None
        self.encrypted_image = None
        self.key = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for buttons
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Right frame for image display
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(left_frame, text="IMAGE ENCRYPTION\nDECRYPTION", font=("Arial", 30), fg="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Buttons
        choose_button = tk.Button(left_frame, text="Choose", command=self.open_image, font=("Arial", 16), bg="orange", fg="blue", borderwidth=3, relief="raised")
        choose_button.grid(row=1, column=0, pady=(0, 10), sticky="w")

        save_button = tk.Button(left_frame, text="Save", command=self.save_image, font=("Arial", 16), bg="orange", fg="blue", borderwidth=3, relief="raised")
        save_button.grid(row=2, column=0, pady=(0, 10), sticky="w")

        encrypt_button = tk.Button(left_frame, text="Encrypt", command=self.encrypt_image, font=("Arial", 16), bg="light green", fg="blue", borderwidth=3, relief="raised")
        encrypt_button.grid(row=3, column=0, pady=(0, 10), sticky="w")

        decrypt_button = tk.Button(left_frame, text="Decrypt", command=self.decrypt_image, font=("Arial", 16), bg="orange", fg="blue", borderwidth=3, relief="raised")
        decrypt_button.grid(row=4, column=0, pady=(0, 10), sticky="w")

        reset_button = tk.Button(left_frame, text="Reset", command=self.reset_image, font=("Arial", 16), bg="yellow", fg="blue", borderwidth=3, relief="raised")
        reset_button.grid(row=5, column=0, pady=(0, 10), sticky="w")

        exit_button = tk.Button(left_frame, text="EXIT", command=self.exit_app, font=("Arial", 16), bg="red", fg="blue", borderwidth=3, relief="raised")
        exit_button.grid(row=6, column=0, pady=(0, 10), sticky="w")

        # Image display
        self.panelA = tk.Label(right_frame, width=500, height=500)
        self.panelA.pack(side="left", padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.panelB = tk.Label(right_frame, width=500, height=500)
        self.panelB.pack(side="right", padx=10, pady=10, fill=tk.BOTH, expand=True)

    def open_image(self):
        try:
            file_path = filedialog.askopenfilename(title="Open")
            if file_path:
                self.image_path = file_path
                img = Image.open(self.image_path)
                img = ImageTk.PhotoImage(img)
                self.display_image(img)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the image:\n{str(e)}")

    def encrypt_image(self):
        try:
            if self.image_path:
                image_input = cv2.imread(self.image_path, 0)
                (x1, y) = image_input.shape
                image_input = image_input.astype(float) / 255.0

                mu, sigma = 0, 0.1
                self.key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
                self.encrypted_image = image_input / self.key

                encrypted_img = Image.fromarray((self.encrypted_image * 255).astype(np.uint8))
                encrypted_img = ImageTk.PhotoImage(encrypted_img)
                self.display_image(encrypted_img, panel_name="panelB")

                messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during encryption:\n{str(e)}")

    def decrypt_image(self):
        try:
            if self.encrypted_image is not None and self.key is not None:
                decrypted_image = self.encrypted_image * self.key
                decrypted_image *= 255.0

                decrypted_img = Image.fromarray(decrypted_image.astype(np.uint8))
                decrypted_img = ImageTk.PhotoImage(decrypted_img)
                self.display_image(decrypted_img, panel_name="panelB")

                messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption:\n{str(e)}")

    def reset_image(self):
        try:
            if self.image_path:
                img = Image.open(self.image_path)
                img = ImageTk.PhotoImage(img)
                self.display_image(img, panel_name="panelB")

                messagebox.showinfo("Success", "Image reset to original format!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while resetting the image:\n{str(e)}")

    def save_image(self):
        try:
            if self.encrypted_image is not None:
                save_path = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
                if save_path:
                    Image.fromarray((self.encrypted_image * 255).astype(np.uint8)).save(save_path.name)
                    messagebox.showinfo("Success", "Encrypted Image Saved Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image:\n{str(e)}")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.root.destroy()

    def display_image(self, img, panel_name="panelA"):
        if getattr(self, panel_name) is not None:
            getattr(self, panel_name).configure(image=img)
            getattr(self, panel_name).image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptDecryptApp(root)
    root.mainloop()
