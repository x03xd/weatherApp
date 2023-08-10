import tkinter as tk
from tkinter import PhotoImage
from urllib.request import urlopen


def create_notification(response, city):

    notification = tk.Tk()
    notification.overrideredirect(True)

    notification_width = 300
    notification_height = 150

    notification.geometry(f"{notification_width}x{notification_height}")
    notification.attributes("-topmost", True)
    notification.after(5000, notification.destroy)

    city_name_label = tk.Label(notification, text=city, font=("Helvetica", 16, "bold"))
    temperature_label = tk.Label(notification, text=f"{str(response['main']['temp'])}°C",
                                 font=("Helvetica", 12))
    weather_label = tk.Label(notification, text=response['weather'][0]['description'].capitalize(),
                             font=("Helvetica", 12))

    city_name_label.pack(pady=(10, 0))
    temperature_label.pack()
    weather_label.pack(pady=(0, 10))

    img_url = f"http://openweathermap.org/img/w/{response['weather'][0]['icon']}.png"
    u = urlopen(img_url)
    raw_data = u.read()
    u.close()

    photo = PhotoImage(data=raw_data)
    image_label = tk.Label(notification, image=photo)
    image_label.image = photo
    image_label.pack()

    notification.mainloop()