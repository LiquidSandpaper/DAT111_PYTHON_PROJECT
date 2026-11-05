# importerer modules og packages
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
from Semester26_Model import  predict_price
from Semester26_Model import r2_print
from Semester26_Model import mae_print

# Tegner/Oppdaterer viduet vi får opp når plt.show() kjører
# Alle events, alle klikk på kartet eller på knapper kaller denne funksjonen
def draw_the_map():
    ax_map.cla()
    ax_map.imshow(img, extent=(0, 100, 0, 100), aspect='auto')
    x,y = marked_point
    ax_map.scatter(x, y, marker='+', c='darkblue', s=170)
    print(f"marked_point: {marked_point}")
    if marked_point == (0, 0):
        return

    # display_price er stringen som blir vist ved markøren på kartet.
    # den baserer seg på deafault_m2. Eksempelvis 100 kvadratmeter
    default_m2_price:float = predict_price(x, y, default_m2, house_type, standard_type) / default_m2
    display_price = f"{round(default_m2_price * 1000, -2):,.0f}\n kr/m2".replace(",", " ")

    # bar grafen viser priser per kvadratmeter
    # history_price_bars gir verdiene og dermed høyden til stolpene på bar grafen
    history_m2_list = [50,100,150,200]
    history_price_bars = [predict_price(x, y,  _m2, house_type, standard_type)/_m2 for _m2 in history_m2_list]
    # _m2 er bare en temp veriabel

    ax_map.text(x - 7, y - 14, display_price, color='darkblue', fontsize=17, bbox=dict(facecolor="white", alpha=0.3, edgecolor="none")) # tekst ved markør på kart
    ax_history.cla()
    bars_colors = ["darkblue" if size == default_m2 else "#35a68f" for size in history_m2_list]
    ax_history.bar(history_m2_list, history_price_bars, color=bars_colors, width=20) # bar stolper
    ax_history.set_ylabel("Pris per m2 (tusen kr)", color='white') # Legger til en label på y aksen til grafen
    ax_history.set_xlabel("m2", color='white')  # Legger til en label på x aksen til grafen
    fig.canvas.manager.set_window_title("Bolig priser i Bergen")

    plt.draw()

def on_click_map(event) :
    global marked_point
    if event.inaxes != ax_map:
        return
    marked_point = (event.xdata, event.ydata)
    draw_the_map()
    return

def on_house_type(key):
    global house_type
    house_type = house_types[key]
    draw_the_map()

def on_standard(key):
    global standard_type
    standard_type = standard_types[key]
    draw_the_map()

house_types = {
    'Enebolig': 1,
    'Rekke': 2,
    'Leilighet': 3
}
standard_types = {
    'Dårlig': 1,
    'God': 2,
    'Meget God': 3,
    'Luksus': 4
}

# Setter start-verdier for hustype, husstandard, kvadratmeter, og punkt i kartet
house_type = 1
standard_type = 1
default_m2 = 100 # Bestemmer hva slags kvadratmeter pris som vises ved marked_point på kartet
marked_point = (43,57)

# Create the figures
fig = plt.figure(figsize=(10.0, 7.0),facecolor='#053028')  # Endret startstørrelse på vinduet, og fargeinnhold
fig.suptitle(f"Bolig priser i Bergen", color='white', fontsize=20, x=0.67, y=0.97)
fig.text(0.12, 0.51,f"r2: {r2_print}   MAE: {mae_print}", color='white', fontsize=12)

# Bestemmer hvor figurene / elementene ligger i vinduet
ax_map = fig.add_axes((0.42, 0.10, 0.50, 0.80))
ax_radio_house_type = fig.add_axes((0.08, 0.75, 0.25, 0.15))
ax_radio_standard = fig.add_axes((0.08, 0.57, 0.25, 0.15))
ax_history = fig.add_axes((0.08, 0.10, 0.25, 0.40))

# skifter bakgrunnsfarge på figurene
ax_radio_house_type.set_facecolor('#dadce6')
ax_radio_standard.set_facecolor('#dadce6')
ax_history.set_facecolor('#dadce6')

# skifter farge på tallene rundt figurene
ax_map.tick_params(axis='both', colors='white')
ax_history.tick_params(axis='both', colors='white')

radio_button_category = RadioButtons(ax_radio_house_type, list(house_types.keys()))
radio_button_standard = RadioButtons(ax_radio_standard, list(standard_types.keys()))
radio_button_category.on_clicked(on_house_type)
radio_button_standard.on_clicked(on_standard)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0) # Adjust the figure to fit the image
ax_map.margins(x=0.01, y=0.01)  # Adjust x and y margins
img = mpimg.imread('Semester26_Bergen.jpg')
ax_map.imshow(img, aspect='auto')

draw_the_map()
plt.connect('button_press_event', on_click_map)
plt.show()


