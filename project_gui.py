import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkcalendar import DateEntry, Calendar
from datetime import date
from SQL_Connection_Package.sql_connect import Sql_Server_DataBase
from faker import Faker

#######  Display All Dataframe
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Create faker
faker = Faker()

# Create connection
DB_For_Project = Sql_Server_DataBase("XPS\SQLEXPRESS", "Project_For_DB")

# City By country Dictionary
countries_dict = {'Argentina': ['Buenos Aires', 'Cordoba', 'Rosario', 'Mendoza', 'Mar del' 'Plata', 'Salta'],
                  'Brazil': ['Rio de Janeiro', 'Salvador', 'Fortaleza', 'Manaus', 'Porto Alegre', 'Natal',
                             'Osasco'],
                  "Germany": ["Berlin", "Munich", "Cologne", "Dortmund", "Hamburg", "Bremen", "Hanover", "Bochum"],
                  "Spain": ["Madrid", "Barcelona", "Valencia", "Bilbao", "Las Palmas"],
                  "Israel": ["Tel Aviv", "Haifa", "Eilat", "Beer Sheva", "Jerusalem"],
                  "USA": ["New York", "Los Angeles", "Chicago", "San Antonio", "Philadelphia", "Dallas",
                          "San Diego",
                          "Austin", "San Jose", "El Paso", "Boston", "Denver", "Las Vegas", "Mesa", "Atlanta"],
                  "Russia": ["Moscow", "Kazan", "Novosibirsk", "Omsk", "Ufa", "Perm"]
                  }


# Date Entry Calendar
class MyDateEntry(DateEntry):
    def __init__(self, master=None, **kw):
        DateEntry.__init__(self, master=None, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg='black', bd=1)
        # add label displaying today's date below
        self.cal = tk.Label(self._top_cal, bg='gray90', anchor='w',
                            text='Today: %s' % date.today().strftime('%x')).pack(fill='x')


# Boolean Error Variable
all_good = False

# Create GUI window
root = tk.Tk()
root.geometry('500x200+100+200')
root.title('AirBNB Search Engine')

################    Optional Icon   ###################
# root.iconbitmap('C:/Users/Ganor/Tracing/Downloads/airbnb_icon.ico')
number_of_guests = 0


# Dynamic Language selection function
def change_Language_selection(value):
    selected_type = type_variable.get()
    try:
        if selected_type == "Online Experience":
            language_df = DB_For_Project.query_To_Pandas('SELECT DISTINCT LANGUAGE from OnlineLanguages')['LANGUAGE']
            language_list = language_df.tolist()
        elif selected_type == "Live Experience":
            language_df = DB_For_Project.query_To_Pandas('SELECT DISTINCT LANGUAGE from LiveLanguages')['LANGUAGE']
            language_list = language_df.tolist()
        else:
            language_list = []

        if len(language_list) != 0:
            var = tk.StringVar(root)
            language_option = ttk.OptionMenu(root, var, *language_list).grid(row=0, column=3)
    except Exception as e:
        print(e)


############## Set Order Type Elements #############
type_label = tk.Label(root, text="Pick Order Type:").grid(row=0, column=0)
type_variable = tk.StringVar(root)
type_variable.set("Places To Stay")  # default value
type_option = ttk.OptionMenu(root, type_variable, "Places To Stay", *["Places To Stay", "Live Experience", "Online Experience"],
                             command=change_Language_selection).grid(row=0, column=1)

########## Set Language Elements #############
Country_label = tk.Label(root, text="Pick Language").grid(row=0, column=2)
language_variable = tk.StringVar(root)
language_option = ttk.OptionMenu(root, language_variable, '').grid(row=0, column=3)

####################    Start Date Calender    ############################
ttk.Label(root, text='Start Date:').grid(row=1, column=0)
start_date_cal = DateEntry(root, width=12, background='darkgrey',
                           foreground='white', borderwidth=2)
start_date_cal.grid(row=1, column=1)

####################    End Date Calender    ############################
ttk.Label(root, text='End Date:').grid(row=1, column=2)
end_date_cal = DateEntry(root, width=12, background='darkgrey',
                         foreground='white', borderwidth=2)
end_date_cal.grid(row=1, column=3)


# Dynamic City Selection
def change_city_selection(value):
    selected_country = country_variable.get()
    cities = countries_dict.get(selected_country)
    city_variable.set(cities[0])
    city_option = ttk.OptionMenu(root, city_variable, *cities).grid(row=2, column=3)


# Country_label = tk.Label(root, text="Pick country").grid(row=2, column=0)
country_variable = tk.StringVar(root)
countries_df = DB_For_Project.query_To_Pandas('SELECT * from countries')['Country']
countries_list = countries_df.tolist()
country_variable.set(countries_list[0])  # default value
countries_option = ttk.OptionMenu(root, country_variable, *countries_list, command=change_city_selection).grid(row=2,
                                                                                                               column=1)

####### Set City Elements #############
city_label = tk.Label(root, text="Pick city").grid(row=2, column=2)
city_variable = tk.StringVar(root)
city_variable.set('Pick City')  # default value
city_option = ttk.OptionMenu(root, city_variable, '').grid(row=2, column=3)

####### Number Of guests ######
guest_entry = tk.StringVar(root)
number_of_guests_label = tk.Label(root, text='Number of guests:').grid(row=3, column=0)
number_of_guests_entry = tk.Entry(root, textvariable=guest_entry).grid(row=3, column=1)


# Returns Relevant Table From User Selection
def get_result_df(selected_type, start_date, end_date, language, country, city, number_of_guests):
    if selected_type == 'Properties':
        query_string = 'SELECT Prod.ProductID, P.Style,p.NumOfBathrooms,p.NumOfBedrooms, prod.price, p.GuestCapacity, L.Street, Prod.[averagerating]' \
                       ' FROM Properties AS P JOIN LOCATIONS AS L on P.Location=L.Locationid  join Products AS Prod on Prod.ProductID=P.PropertyID ' + \
                       'WHERE L.Country=\'' + country + '\' AND L.City=\'' + city + '\';'
        return DB_For_Project.query_To_Pandas(query_string)

    elif selected_type == 'OnlineExperience':
        query_string = 'SELECT P.ProductID, Ex.Tonnage, ex.MaxCapacity, P.Price, P.HostEmail, p.[averagerating] ' \
                       ' FROM OnlineExperiences AS Ex join OnlineLanguages AS Lan on ' \
                       'Ex.OnlineExperienceID=Lan.OnlineExperienceID join Products AS P on P.ProductID=Ex.OnlineExperienceID' \
                       ' WHERE Lan.Language =\'' + language + '\';'

        return DB_For_Project.query_To_Pandas(query_string)

    elif selected_type == 'LiveExperience':
        query_string = 'SELECT P.ProductID, [Gathering Location]= concat(L.Street,\' \',L.houseNum), Ex.[Duration(min.)],' \
                       ' P.Price, [Total Price]=P.Price*' + number_of_guests + ' ,P.HostEmail, P.[averagerating] FROM LiveExperiences AS Ex join LiveLanguages AS Lan on' \
                                                                               ' Ex.LiveExperienceID=Lan.LiveExperienceID join Products AS P ON P.ProductID=Ex.LiveExperienceID' \
                                                                               ' JOIN Locations AS L ON L.LocationID=Ex.Location WHERE Lan.Language =\'' + language + '\' AND  ' \
                                                                                                                                                                      'L.Country=\'' + country + '\' AND L.City=\'' + city + '\';'

        return DB_For_Project.query_To_Pandas(query_string)


# Function to open new GUI window
def openNewWindow():
    global all_good, number_of_guests

    if type_variable.get() == 'Places To Stay':
        selected_type = 'Properties'
    elif type_variable.get() == 'Online Experience':
        selected_type = 'OnlineExperience'
    else:
        selected_type = 'LiveExperience'

    ######## Get User Selection  #######
    start_date = start_date_cal.get_date()
    end_date = end_date_cal.get_date()
    language = language_variable.get()
    country = (country_variable.get())
    city = city_variable.get()
    number_of_guests = guest_entry.get()
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_query = 'INSERT INTO SEARCHS VALUES (\'' + str(
        faker.ipv4()) + '\',' + '\'aarondominguez@yahoo.com\', \'' + date_time + '\', \'' + type_variable.get() + '\', ' + \
                   str(number_of_guests) + ', \'' + str(start_date) + '\', \'' + str(end_date) + '\')'

    try:
        # Try to insert query
        DB_For_Project.send_Query(insert_query)
        DB_For_Project.myDB.commit()
        all_good = True

    except:
        # If couldn't insert, message pops and new window not opened
        all_good = False

    if all_good:
        # Toplevel object which will be treated as a new window
        newWindow = tk.Toplevel(root)

        # Get Result dataframe
        full_result_df = get_result_df(selected_type, start_date, end_date, language, country, city, number_of_guests)

        # Drop irrelevant data
        result_df = full_result_df.drop(['ProductID'], axis=1)

        # for i in range(result_df.shape[0]):
        def show():
            count = 0
            for j in result_df.values.tolist():
                listBox.insert("", "end", iid='%s' % count, values=j)
                count += 1

        # A Label widget to show in toplevel
        result_label = tk.Label(newWindow, text="Results", font=("Arial", 30)).grid(row=0, columnspan=3)

        # create Treeview with 3 columns
        cols = result_df.columns.tolist()
        listBox = ttk.Treeview(newWindow, columns=cols, show='headings')

        # set column headings
        for col in cols:
            listBox.heading(col, text=col, anchor='center')
            listBox.column(col, anchor='center')

        # Show more details function
        def more_details():
            try:  # If no selection made, alert
                row_selection = int(listBox.selection()[0])
            except:
                messagebox.showerror("Failed", "You did something wrong\n You Must Select a product.")
                return

            product_id = (full_result_df.iloc[row_selection]['ProductID'])
            if selected_type == 'LiveExperience':
                query_string = 'select p.HostEmail, p.Price, [Total Price]= p.price*' + number_of_guests + \
                               ', l.Country, l.City, [Street Address] = CONCAT(l.Street ,\' \',l.houseNum), , P.AverageRating ' \
                               'from Products as p join LiveExperiences as live on ' \
                               'live.LiveExperienceID=p.ProductID ' \
                               'join Locations as l on l.LocationID=live.Location' \
                               'where p.ProductID=' + str(product_id)

            elif selected_type == 'Properties':
                number_of_days = end_date - start_date
                query_string = 'select p.HostEmail, p.Price, [Total Price]= p.price*' + str(
                    number_of_days.days) + ' , l.Country, l.City, ' \
                                           '[Street Address] =  CONCAT(l.Street ,\' \',l.houseNum), P.AverageRating ' \
                                           'from Products as p join Properties as prop on prop.PropertyID=p.ProductID join ' \
                                           'Locations as l on l.LocationID=prop.Location ' \
                                           'where p.ProductID=' + str(product_id)
            else:
                query_string = 'select p.HostEmail, p.Price, [Total Price]= p.price*' + number_of_guests + '' \
                                                                                                           ', o.Tonnage, o.MaxCapacity, , P.AverageRating from Products as p join OnlineExperiences ' \
                                                                                                           'as o on ' \
                                                                                                           'o.OnlineExperienceID=p.ProductID where p.ProductID=' + str(product_id)
            # Get data from query
            more_det_df = DB_For_Project.query_To_Pandas(query_string)

            listBox.delete()

            details_label = tk.Label(newWindow, text="Details For Product", font=("Arial", 30)).grid(row=0, columnspan=3)

            cols = more_det_df.columns.tolist()
            details_box = ttk.Treeview(newWindow, columns=cols, show='headings')
            # set column headings
            for col in cols:
                details_box.heading(col, text=col, anchor='center')
                details_box.column(col, anchor='center')

            for j in more_det_df.values.tolist():
                details_box.insert("", "end", values=j)

            details_box.grid(row=1, column=0, columnspan=2)

        show()
        listBox.grid(row=1, column=0, columnspan=2)
        closeButton = tk.Button(newWindow, text="Close", width=15, command=exit).grid(row=4, column=1)
        closeButton = tk.Button(newWindow, text="More Details", width=15, command=more_details).grid(row=4,
                                                                                                     column=0)

    # If Search Query Not Valid, pop message
    else:
        messagebox.showerror("Failed", "You did something wrong\n Make sure dates are correct and all details are "
                                       "filled.")


# Submit Search Button
buttonCal = tk.Button(root, text="Submit", command=openNewWindow).grid(row=7, column=0)

root.mainloop()
