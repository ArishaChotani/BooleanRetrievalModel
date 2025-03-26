import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, messagebox
import query_processor
import main 

# UI
BG_COLOR = "#1E1E2E"  # Background color (Dark Theme)
TEXT_COLOR = "#EAEAEA"  # Light-colored text for contrast
BUTTON_COLOR = "#5E81AC"  # Standard button color
BUTTON_HOVER = "#81A1C1"  # Button hover effect color
INPUT_BG = "#2E3440"  # Input field background color
RESULT_BG = "#3B4252"  # Results frame background color
CARD_COLOR = "#434C5E"  # Document card background color
CARD_HOVER = "#4C566A"  # Hover effect for document cards

DOCS_PER_ROW = 8  # Number of documents to display per row in the results

#GUI Window
def run_gui():
    # Load inverted and positional indexes from JSON files
    index = query_processor.load_index("inverted_index.json")
    positional_index = query_processor.load_index("positional_index.json")

    def search_query():
        nonlocal index, positional_index  # Access the loaded indexes

        query = query_entry.get().strip()  # Get user input and remove extra spaces
        if not query:
            messagebox.showwarning("⚠ Input Error", "Query cannot be empty!")
            return

        # Fetch the search results from query_processor
        result = query_processor.process_query(query, index, positional_index)

        # Clear previous search results
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Display new search results
        if result:
            display_results(result)
        else:
            # no results are found
            no_result_label = tk.Label(scrollable_frame, text="❌ No matching documents found.", 
                                       font=("Arial", 12), fg=TEXT_COLOR, bg=RESULT_BG)
            no_result_label.grid(row=0, column=0, columnspan=DOCS_PER_ROW, pady=10, padx=10)

        # Refresh canvas to update the UI
        result_canvas.update_idletasks()
        result_canvas.yview_moveto(0)  

    def display_results(doc_list):
        doc_list = sorted(doc_list, key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else x)
        row, col = 0, 0  # Start placing results from the first row and column

        for doc in doc_list:
            # Create a styled label (document card) for each result
            doc_card = tk.Label(scrollable_frame, text=f"📄 {doc}", font=("Arial", 12, "bold"), fg=TEXT_COLOR,
                                bg=CARD_COLOR, padx=14, pady=9, relief="ridge", borderwidth=2)
            doc_card.grid(row=row, column=col, padx=9, pady=4, sticky="w")
            #hover effect 
            doc_card.bind("<Enter>", lambda e, w=doc_card: w.config(bg=CARD_HOVER))
            doc_card.bind("<Leave>", lambda e, w=doc_card: w.config(bg=CARD_COLOR))

            col += 1
            if col >= DOCS_PER_ROW:  # Move to the next row after filling the current row
                col = 0
                row += 1

    def on_mouse_wheel(event):
        result_canvas.yview_scroll(-1 * (event.delta // 120), "units")  # Enable mouse scroll

    def exit_app():
        root.destroy()  # Close the application

    def fade_in(window, alpha=0):
        if alpha < 1:
            window.attributes("-alpha", alpha) 
            window.after(20, fade_in, window, alpha + 0.05)  

    #Initialize the Main Window
    root = tk.Tk()
    root.title("🔍 Information Retrieval System by 22K-4569")  
    root.geometry("700x500")   
    root.configure(bg=BG_COLOR)  
    root.attributes("-alpha", 0)  
    fade_in(root)  # Trigger fade-in effect

    #Title Label
    title_label = tk.Label(root, text="🔍 Search Engine", font=("Times New Roman", 18, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
    title_label.pack(pady=10)

    #Input Frame
    query_frame = tk.Frame(root, bg=BG_COLOR)
    query_frame.pack(pady=10)
    
    tk.Label(query_frame, text="Enter Query:", font=("Times New Roman", 12), fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, padx=5)
    query_entry = tk.Entry(query_frame, width=50, font=("Arial", 12), bg=INPUT_BG, fg=TEXT_COLOR, insertbackground="white", relief=tk.FLAT)
    query_entry.grid(row=0, column=1, padx=5, pady=5)
    query_entry.bind("<Return>", lambda event: search_query())  # Press Enter to search

    #Search Button
    search_button = tk.Button(root, text="🔍 Search", font=("Arial", 12, "bold"), bg=BUTTON_COLOR, fg="white", padx=10, pady=5, command=search_query)
    search_button.pack(pady=5)
    search_button.bind("<Enter>", lambda e: search_button.config(bg=BUTTON_HOVER))
    search_button.bind("<Leave>", lambda e: search_button.config(bg=BUTTON_COLOR))

    #Scrollable Results Frame
    result_canvas = Canvas(root, bg=RESULT_BG, highlightthickness=0)
    scrollbar = Scrollbar(root, orient="vertical", command=result_canvas.yview)
    scrollable_frame = Frame(result_canvas, bg=RESULT_BG)

    scrollable_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))
    result_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    result_canvas.configure(yscrollcommand=scrollbar.set)
    
    result_canvas.pack(fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")
    result_canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Enable mouse scrolling

    #Exit
    exit_button = tk.Button(root, text="❌ Exit", font=("Arial", 12, "bold"), bg="red", fg="white", padx=10, pady=5, command=exit_app)
    exit_button.pack(pady=10)
    exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#D32F2F"))
    exit_button.bind("<Leave>", lambda e: exit_button.config(bg="red"))


    root.mainloop()  # Run the GUI event loop

if __name__ == "__main__":
    #main.main1()
    run_gui()  # Start the application