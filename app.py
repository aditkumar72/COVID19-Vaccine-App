import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter.constants import FLAT, RAISED
import pytz
import requests

IST = pytz.timezone('Asia/Kolkata')

# App version
app_version = 'v1.0'

# Color value refrence
top_left_frame_bg = '#5c4ce1'
top_right_frame_bg = '#867ae9'


app = tk.Tk()

# App Geometry and components
app.geometry("700x480+600+300")
app.title(f"COVID19 Vaccine App {app_version}")
app.iconbitmap("graphics/covid-vaccine.ico")
app.resizable(False, False)
app.config(background='#293241')

# App Frames
frame1 = tk.Frame(app, height=120, width=180, bg=top_left_frame_bg, bd=1, relief=FLAT)
frame1.place(x=0,y=0)

frame2 = tk.Frame(app, height=120, width=520, bg=top_right_frame_bg, bd=1, relief=FLAT)
frame2.place(x=180, y=0)

frame3 = tk.Frame(app, height=30, width=700, bg='black', bd=1, relief=RAISED)
frame3.place(x=0, y=120)

# Entry boxes
pincode_text_var = tk.StringVar()
pincode_textbox = tk.Entry(app, width=11, bg='#eaf2ae', fg='black', textvariable=pincode_text_var, font='verdana 11')
pincode_textbox['textvariable'] = pincode_text_var
pincode_textbox.place(x= 220, y=40)

date_text_var = tk.StringVar()
date_textbox = tk.Entry(app, width=12, bg='#eaf2ae', fg='black', textvariable=date_text_var, font='verdana 10')
date_textbox['textvariable'] = date_text_var
date_textbox.place(x=380, y=40)

def refresh_api_call(PINCODE, DATE):
    # header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link)
    resp_json = response.json()
    return resp_json

def clear_result_box():
    result_box_avl.delete('1.0', tk.END)
    result_box_cent.delete('1.0', tk.END)
    result_box_age.delete('1.0', tk.END)
    result_box_vacc.delete('1.0', tk.END)
    result_box_D1.delete('1.0', tk.END)
    result_box_D2.delete('1.0', tk.END)
    result_box_D1_D2.delete('1.0', tk.END)

def search_vaccine_avl():
    clear_result_box()
    PINCODE = pincode_text_var.get().strip()
    DATE = date_text_var.get()
    resp_JSON = refresh_api_call(PINCODE, DATE)

    try:
        if len(resp_JSON['sessions']) == 0:
            messagebox.showinfo("INFO","Vaccine not yet arrived for the given date")

        for sess in resp_JSON['sessions']:
            age_limit           = sess['min_age_limit']
            center_name         = sess['name']
            vaccine_name        = sess['vaccine']
            available_capacity  = sess['available_capacity']
            qnty_dose_1         = sess['available_capacity_dose1']
            qnty_dose_2         = sess['available_capacity_dose2']

            if available_capacity > 0:
                curr_status = 'Available'
            else:
                curr_status = 'NA'
            
            if age_limit == 45:
                age_grp = '45+'
            else:
                age_grp = '18-44'

            result_box_avl.insert(tk.END, f"{curr_status:^6s}")
            result_box_avl.insert(tk.END,"\n")
            result_box_cent.insert(tk.END, f"{center_name:<30.29s}")
            result_box_cent.insert(tk.END,"\n")
            result_box_age.insert(tk.END, f"{age_grp:<6s}")
            result_box_age.insert(tk.END,"\n")
            result_box_vacc.insert(tk.END, f"{vaccine_name:<8s}")
            result_box_vacc.insert(tk.END,"\n")
            result_box_D1.insert(tk.END, f"{qnty_dose_1:>5}")
            result_box_D1.insert(tk.END,"\n")
            result_box_D2.insert(tk.END, f"{qnty_dose_2:>5}")
            result_box_D2.insert(tk.END,"\n")
            result_box_D1_D2.insert(tk.END, f"{available_capacity:<5}")
            result_box_D1_D2.insert(tk.END,"\n")
    except KeyError:
        messagebox.showerror("ERROR","No Available center(s) for the given Pincode and date")
        print (pincode_text_var.get())
# Buttons
search_vaccine_image = tk.PhotoImage(file="graphics/search-icon.png")
search_vaccine_btn = tk.Button(app, image=search_vaccine_image, bg=top_right_frame_bg, command=search_vaccine_avl, relief=RAISED)
search_vaccine_btn.place(x=600, y=25)

# Labels
label_date_now = tk.Label(text="Current Date", bg = top_left_frame_bg, font = 'Verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = tk.Label(text="Current Time", bg = top_left_frame_bg, font = 'Verdana 12')
label_time_now.place(x=20, y=60)

label_pincode = tk.Label(text="Pincode", bg = top_right_frame_bg, font = 'Verdana 11')
label_pincode.place(x=220, y=15)

label_date = tk.Label(text="Date", bg = top_right_frame_bg, font = 'Verdana 11')
label_date.place(x=380, y=15)

label_dateformat = tk.Label(text="[dd-mm-yyyy]", bg = top_right_frame_bg, font = 'Verdana 7')
label_dateformat.place(x=420, y=18)

label_search_vacc = tk.Label(text="Search \nAvailable Vaccine", bg = top_right_frame_bg, font = 'Verdana 8')
label_search_vacc.place(x=570, y=70)

label_head_result = tk.Label(text=" Status       \tCentre-Name\t              Age-Group    Vaccine       Dose_1     Dose_2     Total", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)

## TEXT BOX - for RESULTs
result_box_avl = tk.Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_avl.place(x= 3 , y= 152)

result_box_cent = tk.Text(app, height = 20, width = 30, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_cent.place(x= 75 , y= 152)

result_box_age = tk.Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_age.place(x= 330 , y= 152)

result_box_vacc = tk.Text(app, height = 20, width = 10, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_vacc.place(x= 400 , y= 152)

result_box_D1 = tk.Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1.place(x= 490 , y= 152)

result_box_D2 = tk.Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D2.place(x= 555 , y= 152)

result_box_D1_D2 = tk.Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1_D2.place(x= 630 , y= 152)

# Defining Functions

def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    formatted_now = raw_TS.strftime("%d-%m-%Y")
    label_date_now.config(text = date_now)
    label_time_now.config(text = time_now)
    label_time_now.after(1000, update_clock)
    return formatted_now

def insert_today_date():
    formatted_now = update_clock()
    date_text_var.set(formatted_now)    

# Check Box 
chkbox_today_var = tk.IntVar()
today_date_chkbox = tk.Checkbutton(app, text='Today', bg= top_right_frame_bg, variable=chkbox_today_var, onvalue= 1, offvalue=0, command = insert_today_date)
today_date_chkbox.place(x= 375, y= 65)

# Detect Automatic Pincode
url = 'https://ipinfo.io/postal'
def get_pincode_ip_service(url):
    response_pincode = requests.get(url).text
    return response_pincode

def fill_pincode_with_radio():
    curr_pincode = get_pincode_ip_service(url)
    pincode_text_var.set(curr_pincode)


# Radio Buttons
curr_loc_var = tk.StringVar()
radio_location = tk.Button(app, text="Current Location", bg=top_right_frame_bg, command=fill_pincode_with_radio, relief=RAISED)
radio_location.place(x=220, y=65)

update_clock()


app.mainloop()

