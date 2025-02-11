import time
import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import pywhatkit
import qrcode
from googletrans import Translator
import requests
from tkinter import Toplevel, Label, Entry, Button, Canvas, Frame, Scrollbar, StringVar, messagebox

# Main interface background images and icon paths
BACKGROUND_IMAGES = {
    "menu": "main background.jpeg",
    "whatsapp": "Sky-Desktop-Backgrounds-Hd-Images.jpg",
    "translation": "moon.jpg",
    "qr_code": "Sky-Desktop-Backgrounds-Hd-Images.jpg",
    "search": "Sky-Desktop-Backgrounds-Hd-Images.jpg"
}

ICONS = {
    "whatsapp": "msgicon.png",
    "translation": "trans.png ",
    "qr_code": "generated_qr.png",
    "search": "searchicon.png"
}


# SerpApi API Key (replace with your valid key)
API_KEY = '7ba7cdb252a832f0b8a0a884c3d47a957e2323dd361dae8d2deb6f61a228004f'

# Function to show success message
def show_success_message(text):
    popup = Toplevel(root)
    popup.geometry("500x500")
    popup.configure(bg="lightgreen")
    popup.title("Success")
    
    msg = tk.Label(popup, text=text, font=("Arial", 12, "bold"), fg="green", bg="lightgreen")
    msg.pack(expand=True)

# Search functionality with option for clickable links or images

from tkinter import Frame
from serpapi import GoogleSearch
import io
# Search Function with SerpApi Integration

import requests
import webbrowser
from io import BytesIO


def open_search():
    def perform_search():
        """Perform search based on the query and selected search type."""
        for widget in results_frame.winfo_children():
            widget.destroy()

        query = search_entry.get()
        search_type = search_option.get()

        if not query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        if search_type == "Images":
            engine = "google_images"
        elif search_type == "Web":
            engine = "google"
        elif search_type == "YouTube":
            engine = "youtube"

        # Set up the search parameters
        params = {
            "q": query,
            "api_key": API_KEY,
            "engine": engine
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            if engine == "google_images" and "images_results" in results:
                display_images(results["images_results"][:10])
            elif engine == "google" and "organic_results" in results:
                display_websites(results["organic_results"][:10])
            elif engine == "youtube" and "video_results" in results:
                display_youtube(results["video_results"][:10])
            else:
                messagebox.showinfo("Info", "No results found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def display_websites(results):
        for idx, result in enumerate(results):
            title = result.get("title", "No Title")
            link = result.get("link", "No Link")
        snippet = result.get("snippet", "No Description")

        # Create a frame for each website
        frame = tk.Frame(results_frame)
        frame.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

        # Title and snippet in a horizontal layout
        title_label = tk.Label(frame, text=title, font=("Arial", 12), fg="blue", cursor="hand2", wraplength=400)
        title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        title_label.bind("<Button-1>", lambda e, url=link: open_link(url))

        snippet_label = tk.Label(frame, text=snippet, font=("Arial", 10), fg="gray", wraplength=500)
        snippet_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Ensure the text spans across the available space
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
    def display_images(results):
        row, col = 0, 0  # Starting row and column for the grid layout
        for idx, result in enumerate(results):
            img_url = result['original']
            response = requests.get(img_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.thumbnail((150, 150))  # Adjust image size
            img = ImageTk.PhotoImage(img)
            frame = tk.Frame(results_frame)
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            img_label = tk.Label(frame, image=img, cursor="hand2")
            img_label.image = img  # Keep reference to image
            img_label.grid(row=0, column=0, padx=10, pady=5)
            title_label = tk.Label(frame, text=result['title'], font=("Arial", 10), fg="blue", cursor="hand2", wraplength=300)
            title_label.grid(row=0, column=1, padx=10, pady=5)
            title_label.bind("<Button-1>", lambda e, url=result['link']: open_link(url))

        # Update the column and row for the grid layout
            col += 1
            if col == 4:  # If we reach 4 columns, go to the next row
              col = 0
              row += 1


    def display_websites(results):
        for idx, result in enumerate(results):
            title = result.get("title", "No Title")
            link = result.get("link", "No Link")
            snippet = result.get("snippet", "No Description")
        
            # Create a frame for each website
            frame = tk.Frame(results_frame)
            frame.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

            # Title and snippet in a horizontal layout
            title_label = tk.Label(frame, text=title, font=("Arial", 12), fg="blue", cursor="hand2", wraplength=400)
            title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            title_label.bind("<Button-1>", lambda e, url=link: open_link(url))

            snippet_label = tk.Label(frame, text=snippet, font=("Arial", 10), fg="gray", wraplength=500)
            snippet_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Ensure the text spans across the available space
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=2)

       

    def display_youtube(results):
        """Display YouTube results with clickable links and thumbnails."""
        for idx, video in enumerate(results):
            title = video.get("title", "No Title")
            link = video.get("link", "No Link")
            thumbnail = video.get("thumbnail", None)

            frame = tk.Frame(results_frame)
            frame.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

            if thumbnail:
                img_data = requests.get(thumbnail).content
                img = Image.open(BytesIO(img_data)).resize((100, 100))
                img_photo = ImageTk.PhotoImage(img)

                img_label = Label(frame, image=img_photo, cursor="hand2")
                img_label.image = img_photo
                img_label.grid(row=0, column=0, padx=10, pady=5)

            title_label = tk.Label(frame, text=title, font=("Arial", 12), fg="blue", cursor="hand2", wraplength=300)
            title_label.grid(row=0, column=1, padx=10, pady=5)
            title_label.bind("<Button-1>", lambda e, url=link: open_link(url))

    def open_link(url):
        """Open the given URL in the web browser."""
        webbrowser.open(url)

    # Search window setup
    search_window = Toplevel(root)
    search_window.title("Enhanced Search")
    search_window.geometry("900x700")

    Label(search_window, text="Search Query:", font=("Arial", 12)).pack(pady=5)
    search_entry = Entry(search_window, font=("Arial", 12), width=60)
    search_entry.pack(pady=5)

    # Dropdown for selecting search type
    search_option = StringVar(value="Web")
    search_frame = Frame(search_window)
    search_frame.pack(pady=5)

    Button(search_frame, text="Web", command=lambda: search_option.set("Web"), font=("Arial", 10), bg="lightblue").pack(side="left", padx=10)
    Button(search_frame, text="Images", command=lambda: search_option.set("Images"), font=("Arial", 10), bg="lightgreen").pack(side="left", padx=10)
    Button(search_frame, text="YouTube", command=lambda: search_option.set("YouTube"), font=("Arial", 10), bg="lightcoral").pack(side="left", padx=10)

    search_button = Button(search_window, text="Search", command=perform_search, font=("Arial", 12), bg="#4A90E2", fg="white")
    search_button.pack(pady=10)

    # Scrollable frame for results
    canvas = Canvas(search_window)
    scroll_y = Scrollbar(search_window, orient="vertical", command=canvas.yview)
    results_frame = Frame(canvas)

    results_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=results_frame,
     anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

# Initialize main window


# Open the search window


import datetime

def open_message_delivery():
    def send_whatsapp_message():
        try:
            phone_number = phone_entry.get()
            message = message_entry.get()
            scheduled_time = time_entry.get()
            translate_option = translate_var.get()
            
            if translate_option == 1:
                target_lang = lang_entry.get()
                translator = Translator()
                message = translator.translate(message, dest=target_lang).text
            
            hour, minute = map(int, scheduled_time.split(':'))
            pywhatkit.sendwhatmsg(phone_number, message, hour, minute)

            # Calculate time difference
            now = datetime.datetime.now()
            scheduled_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if scheduled_datetime < now:  # If scheduled time is before current time, add 1 day
                scheduled_datetime += datetime.timedelta(days=1)

            time_diff = scheduled_datetime - now
            time_to_delivery = str(time_diff).split(".")[0]  # Exclude microseconds
            time_label.config(text=f"Message will be delivered in: {time_to_delivery}")

            show_success_message("Message scheduled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule message: {e}")

    delivery_window = Toplevel(root)
    delivery_window.title("WhatsApp Message Delivery")
    delivery_window.geometry("800x600")
    set_background(delivery_window, BACKGROUND_IMAGES["whatsapp"])

    icon_label = tk.Label(delivery_window, image=icons["whatsapp"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(delivery_window, text="Phone Number (with country code):", font=("Arial", 12), bg="white").pack(pady=5)
    phone_entry = tk.Entry(delivery_window, font=("Arial", 12))
    phone_entry.pack()

    tk.Label(delivery_window, text="Message:", font=("Arial", 12), bg="white").pack(pady=5)
    message_entry = tk.Entry(delivery_window, font=("Arial", 12))
    message_entry.pack()

    tk.Label(delivery_window, text="Scheduled Time (HH:MM):", font=("Arial", 12), bg="white").pack(pady=5)
    time_entry = tk.Entry(delivery_window, font=("Arial", 12))
    time_entry.pack()

    # Checkbox for translation option
    translate_var = tk.IntVar()
    translate_checkbox = tk.Checkbutton(delivery_window, text="Translate message before sending?", variable=translate_var, font=("Arial", 12), bg="white")
    translate_checkbox.pack(pady=5)

    # Entry for language code, shown only if the user wants translation
    lang_label = tk.Label(delivery_window, text="Target Language Code:", font=("Arial", 12), bg="white")
    lang_entry = tk.Entry(delivery_window, font=("Arial", 12))
    
    def toggle_lang_entry():
        if translate_var.get() == 1:
            lang_label.pack(pady=5)
            lang_entry.pack()
        else:
            lang_label.pack_forget()
            lang_entry.pack_forget()

    translate_checkbox.config(command=toggle_lang_entry)

    send_button = tk.Button(delivery_window, text="Schedule Message", command=send_whatsapp_message, font=("Arial", 12), bg="#4A90E2", fg="white")
    send_button.pack(pady=20)

    # Label to display the time remaining for message delivery
    time_label = tk.Label(delivery_window, text="", font=("Arial", 12), bg="white")
    time_label.pack(pady=10)

import datetime
import pywhatkit

from googletrans import Translator
import threading
import time

def open_message_delivery():
    def send_whatsapp_message():
        try:
            phone_number = phone_entry.get()
            message = message_entry.get()
            scheduled_time = time_entry.get()
            translate_option = translate_var.get()

            if translate_option == 1:
                target_lang = lang_entry.get()
                translator = Translator()
                message = translator.translate(message, dest=target_lang).text

            hour, minute = map(int, scheduled_time.split(':'))

            # Calculate time difference from current time
            now = datetime.datetime.now()
            scheduled_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the scheduled time is before the current time, add 1 day to make it future
            if scheduled_datetime < now:
                scheduled_datetime += datetime.timedelta(days=1)

            # Calculate the difference
            time_diff = scheduled_datetime - now
            time_to_delivery = str(time_diff).split(".")[0]  # Exclude microseconds

            # Update the time_label with the time remaining for message delivery
            time_label.config(text=f"Message will be delivered in: {time_to_delivery}")

            # Start sending message in a separate thread to avoid freezing the UI
            threading.Thread(target=send_message, args=(phone_number, message, hour, minute)).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule message: {e}")

    def send_message(phone_number, message, hour, minute):
        """This function runs in a separate thread and sends the message."""
        try:
            pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
            show_success_message("Message scheduled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    # Creating the window
    delivery_window = tk.Toplevel(root)
    delivery_window.title("WhatsApp Message Delivery")
    delivery_window.geometry("800x600")
    set_background(delivery_window, BACKGROUND_IMAGES["whatsapp"])

    icon_label = tk.Label(delivery_window, image=icons["whatsapp"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(delivery_window, text="Phone Number (with country code):", font=("Arial", 12), bg="white").pack(pady=5)
    phone_entry = tk.Entry(delivery_window, font=("Arial", 12))
    phone_entry.pack()

    tk.Label(delivery_window, text="Message:", font=("Arial", 12), bg="white").pack(pady=5)
    message_entry = tk.Entry(delivery_window, font=("Arial", 12))
    message_entry.pack()

    tk.Label(delivery_window, text="Scheduled Time (HH:MM):", font=("Arial", 12), bg="white").pack(pady=5)
    time_entry = tk.Entry(delivery_window, font=("Arial", 12))
    time_entry.pack()

    # Checkbox for translation option
    translate_var = tk.IntVar()
    translate_checkbox = tk.Checkbutton(delivery_window, text="Translate message before sending?", variable=translate_var, font=("Arial", 12), bg="white")
    translate_checkbox.pack(pady=5)

    # Entry for language code, shown only if the user wants translation
    lang_label = tk.Label(delivery_window, text="Target Language Code:", font=("Arial", 12), bg="white")
    lang_entry = tk.Entry(delivery_window, font=("Arial", 12))

    def toggle_lang_entry():
        if translate_var.get() == 1:
            lang_label.pack(pady=5)
            lang_entry.pack()
        else:
            lang_label.pack_forget()
            lang_entry.pack_forget()

    translate_checkbox.config(command=toggle_lang_entry)

    send_button = tk.Button(delivery_window, text="Schedule Message", command=send_whatsapp_message, font=("Arial", 12), bg="#4A90E2", fg="white")
    send_button.pack(pady=20)

    # Label to display the time remaining for message delivery
    time_label = tk.Label(delivery_window, text="", font=("Arial", 12), bg="white")
    time_label.pack(pady=10)

# QR Code Generation function with multiple WhatsApp sending option
from PIL import Image, ImageDraw, ImageFont
import qrcode
import pywhatkit
import time
import tkinter as tk
from tkinter import messagebox, Toplevel

def open_qr_code():
    def generate_qr():
        try:
            url = url_entry.get()
            custom_text = custom_text_entry.get()

            # Generate QR Code
            qr = qrcode.make(url)
            qr_path = "generated_qr_with_text.png"

            # Add custom text below QR Code
            qr_image = qr.convert("RGB")
            draw = ImageDraw.Draw(qr_image)
            font = ImageFont.load_default()  # Use a default font

            # Calculate text size
            bbox = draw.textbbox((0, 0), custom_text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Create a new image with space for text
            new_image_height = qr_image.size[1] + text_height + 10  # Add padding
            new_image = Image.new("RGB", (qr_image.size[0], new_image_height), "white")
            new_image.paste(qr_image, (0, 0))

            # Add text to the new image
            text_x = (new_image.size[0] - text_width) // 2
            text_y = qr_image.size[1] + 5
            draw = ImageDraw.Draw(new_image)
            draw.text((text_x, text_y), custom_text, fill="black", font=font)

            # Save the final image
            new_image.save(qr_path)
            show_success_message("QR code with custom text generated successfully!")

           
            whatsapp_message = f" {custom_text}"
           
            whatsapp_message = f"Here is the QR code for: {custom_text} ({url})"

            # WhatsApp Message Sending
            send_qr_var = messagebox.askyesno("Send QR Code", "Do you want to send this QR Code via WhatsApp?")
            if send_qr_var:
                try:
                    num_contacts = int(number_of_contacts_entry.get())
                    if num_contacts > len(phone_entries):
                        raise ValueError("Number of contacts exceeds available input fields.")

                    phone_numbers = [entry.get() for entry in phone_entries[:num_contacts]]

                    for phone_number in phone_numbers:
                        if phone_number.strip():
                            # Use the detected WhatsApp message
                            pywhatkit.sendwhats_image(phone_number, qr_path, whatsapp_message)
                            time.sleep(10)  # Wait for 10 seconds to ensure message delivery
                        else:
                            messagebox.showerror("Error", "Phone number cannot be empty.")

                    show_success_message("QR code sent to all specified contacts successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send QR code to contacts: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")

    def update_phone_entries():
        try:
            num_contacts = int(number_of_contacts_entry.get())
            for i, entry in enumerate(phone_entries):
                if i < num_contacts:
                    entry.pack(pady=5)  # Show entry
                else:
                    entry.pack_forget()  # Hide entry
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of contacts.")

    qr_window = Toplevel(root)
    qr_window.title("QR Code Generator")
    qr_window.geometry("800x600")
    set_background(qr_window, BACKGROUND_IMAGES["qr_code"])

    icon_label = tk.Label(qr_window, image=icons["qr_code"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(qr_window, text="Enter URL:", font=("Arial", 12), bg="white").pack(pady=5)
    url_entry = tk.Entry(qr_window, font=("Arial", 12), width=40)
    url_entry.pack()

    tk.Label(qr_window, text="Enter Custom Text (e.g., YouTube Channel):", font=("Arial", 12), bg="white").pack(pady=5)
    custom_text_entry = tk.Entry(qr_window, font=("Arial", 12), width=40)
    custom_text_entry.pack()

    tk.Label(qr_window, text="How many numbers to send QR Code to?", font=("Arial", 12), bg="white").pack(pady=5)
    number_of_contacts_entry = tk.Entry(qr_window, font=("Arial", 12), width=5)
    number_of_contacts_entry.pack()
    number_of_contacts_entry.bind("<KeyRelease>", lambda _: update_phone_entries())

    phone_entries = []
    for _ in range(10):  # Allow up to 10 numbers
        phone_entry = tk.Entry(qr_window, font=("Arial", 12), width=30)
        phone_entries.append(phone_entry)

    generate_button = tk.Button(
        qr_window, 
        text="Generate QR Code and Send", 
        command=generate_qr, 
        font=("Arial", 12), 
        bg="#4A90E2", 
        fg="white"
    )
    generate_button.pack(pady=20)

# Translation Feature
def open_translation():
    def translate_text():
        try:
            text_to_translate = source_text.get("1.0", tk.END)
            target_lang = target_lang_entry.get()
            translator = Translator()
            translated_text = translator.translate(text_to_translate, dest=target_lang).text
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, translated_text)
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {e}")

    translation_window = Toplevel(root)
    translation_window.title("Text Translator")
    translation_window.geometry("800x600")
    set_background(translation_window, BACKGROUND_IMAGES["translation"])

    icon_label = tk.Label(translation_window, image=icons["translation"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(translation_window, text="Enter text to translate:", font=("Arial", 12), bg="white").pack(pady=5)
    source_text = tk.Text(translation_window, font=("Arial", 12), height=10, width=60)
    source_text.pack()

    tk.Label(translation_window, text="Target Language Code (e.g., 'es' for Spanish):", font=("Arial", 12), bg="white").pack(pady=5)
    target_lang_entry = tk.Entry(translation_window, font=("Arial", 12))
    target_lang_entry.pack()

    tk.Button(translation_window, text="Translate", command=translate_text, font=("Arial", 12), bg="#4A90E2", fg="white").pack(pady=10)

    tk.Label(translation_window, text="Translated Text:", font=("Arial", 12), bg="white").pack(pady=5)
    result_text = tk.Text(translation_window, font=("Arial", 12), height=10, width=60)
    result_text.pack()

# Function to set background image for a window
def set_background(window, image_path):
    bg_image = Image.open(image_path)
    bg_photo = ImageTk.PhotoImage(bg_image.resize((800, 600)))
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

# Main Menu
def main_menu():
    set_background(root, BACKGROUND_IMAGES["menu"])
    title = tk.Label(root, text="Choose an Option", font=("Arial", 24, "bold"), bg="white")
    title.pack(pady=30)

    message_button = tk.Button(root, image=icons["whatsapp"], command=open_message_delivery, width=120, height=120, compound="top", text="Message \nSheduling",  bg="#4A90E2",font=("Arial", 12),fg="white")
    message_button.pack(pady=20)

    translation_button = tk.Button(root, image=icons["translation"], command=open_translation, width=120, height=120, compound="top", text="Translation", font=("Arial", 12), bg="#4A90E2", fg="white")
    translation_button.pack(pady=20)

    qr_button = tk.Button(root, image=icons["qr_code"], command=open_qr_code, width=120, height=120, compound="top", text="Generate QR", font=("Arial", 12), bg="#4A90E2", fg="white")
    qr_button.pack(pady=20)

    # Add the search button to the main menu
    search_button = tk.Button(root, image=icons["search"], command=open_search, width=120, height=120, compound="top", text="Search", font=("Arial", 12), bg="#4A90E2", fg="white")
    search_button.pack(pady=20)
    search_button.place(x=650, y=20)  # Adjust x and y for precise positioning


# Initialize main window
root = tk.Tk()
root.title("AUTOMATER-Makes Life Easy")
root.geometry("800x600")
root.resizable(False, False)

# Load icons
icons = {name: ImageTk.PhotoImage(Image.open(path).resize((80, 80))) for name, path in ICONS.items()}

main_menu()
root.mainloop()
