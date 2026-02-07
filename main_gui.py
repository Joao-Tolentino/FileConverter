# UI for the file conversion program, allowing user interactivity.
# Imports
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from functions import *

# Root window
root = Tk()

# Window title and dimension
root.title("File Converter App")
root.geometry("750x300")

# Labels
label = Label(root, text="Welcome to the file converter app! \nSelect a file and choose the desired output format.")
label.grid(row=0, column=0, padx=10, pady=10)

selector_lbl = Label(root, text="Select file to convert:")
selector_lbl.grid(row=1, column=0, padx=10, pady=10)

file_types_lbl = Label(root, text="Select output file type:")
file_types_lbl.grid(row=2, column=0, padx=10, pady=10)

# Items in the listboxes
documents = [  '.doc', '.docx', '.pdf', '.txt']
image = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
audio = ['.mp3', '.wav', '.aac', '.flac', '.ogg']
video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
archives = ['.zip', '.rar', '.tar', '.gz', '.7z']

# Functions
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select the file to convert",
        initialdir="/",
        filetypes=(("Documents", ".doc *.docx *.pdf *.txt"),
                   ("Image", "*.jpg *.jpeg *.png *.bmp *.gif"),
                   ("Audio", ".mp3 *.wav *.aac *.flac *.ogg"),
                   ("Video", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                   ("Compressed", "*.zip *.rar *.tar *.gz *.7z"))
    )
    pick_type(file_path)  # Update the file type options based on the selected file
    selector.configure(text = file_path) # Update the text to display the selected file_path

def pick_type(input_file):
    input_file = "." + input_file.rsplit('.', 1)[1].lower()  # Get the input file extension

    if input_file in documents:
        file_types_list["values"] = documents
    elif input_file in image:
        file_types_list["values"] = image
    elif input_file in audio:
        file_types_list["values"] = audio
    elif input_file in video:
        file_types_list["values"] = video
    elif input_file in archives:
        file_types_list["values"] = "Decompress"
    
    file_types_list.current(0)  # Set the default selection and update the box

def clicked():
    # Get the input and output file types
    input_file = selector.cget("text")
    input_file_type = "." + selector.cget("text").rsplit('.', 1)[1].lower()
    output_file_type = file_types_list.get()
    output_folder = selector.cget("text").rsplit('.', 1)[0]  # Remove the extension for the output folder
    # Select the proper function and perform the conversion or decompression
    if input_file_type in archives and output_file_type == "Decompress":
        decompress_file(input_file_type, input_file, output_folder)
    elif input_file_type in documents and output_file_type in documents:
        convert_document(input_file, input_file_type, output_file_type, output_folder)
    elif input_file_type in image and output_file_type in image:
        convert_image(input_file, output_file_type, output_folder)
    elif input_file_type in audio and output_file_type in audio:
        convert_audio(input_file, input_file_type, output_file_type, output_folder)
    elif input_file_type in video and output_file_type in video:    
        convert_video(input_file, output_file_type, output_folder)
    else:
        # Error Message in case of unsupported file type as input
        messagebox.showerror(message="Unsupported input file type.")
        return

    # Select the output message based on the conversion or decompression
    if input_file_type in archives:
        output_type = "Decompressed file"
    else:
        output_type = "Converted file"

    messagebox.showinfo(message=f'{output_type} downloaded successfully! Path:{output_folder}')

# Buttons
selector = Button(root, text="Select File", command=select_file)
selector.grid(row=1, column=1, padx=10, pady=10)

button = Button(root, text="Convert", command=clicked)
button.grid(row=3, column=0, padx=10, pady=10)

# Selector of file type
file_types_list = ttk.Combobox(root)
file_types_list.grid(row=2, column=1, padx=10, pady=10)

# Run the application
root.mainloop()