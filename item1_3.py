import time
import board
import adafruit_dht
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import Button
import random
from gpiozero import LED
from time import sleep
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

#diccionario con iformacion de cada habitat
b1 = {"Nombre":"Bulbasaur",
      "tipo":"Planta/Veneno",
      "pts de vida":45,
      "% de captura":0.45 ,
      "cantidad disponible":3,
      "ataques":[{"nombre": "Placaje","daño":10,"tipo":"normal"},
                 {"nombre":"Latigo Cepa","daño":15,"tipo":"planta"}]}
b2={"Nombre":"Oddish",
      "tipo":"Planta/Veneno",
      "pts de vida":45,
      "% de captura":0.60,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Absorber","daño":10,"tipo":"planta"},
                 {"nombre":"acido","daño":12,"tipo":"veneno"}]}
    
b3={"Nombre":"Caterpie",
      "tipo":"Bicho",
      "pts de vida":45,
      "% de captura":0.75,
      "cantidad disponible":4,
      "ataques":[{"nombre":"Placaje","daño":8,"tipo":"normal"},
                {"nombre":"Picadura","daño":12,"tipo":"bicho"}]} 
p1={"Nombre":"Pikachu",
      "tipo":"Electrico",
      "pts de vida":35,
      "% de captura":0.50,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Impactrueno","daño":15,"tipo":"electrico"},
                {"nombre":"Ataque Rapido","daño":10,"tipo":"normal"}]}
p2={"Nombre":"Eevee",
      "tipo":"Normal",
      "pts de vida":55,
      "% de captura":0.40,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Placaje","daño":10,"tipo":"normal"},
                 {"nombre":"Mordisco","daño":12,"tipo":"normal"}]}
p3={"Nombre":"Meowth",
      "tipo":"Normal",
      "pts de vida":40,
      "% de captura":0.60,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Arañazo","daño":10,"tipo":"normal"}
                 ,{"nombre":"Sorpresa","daño":12,"tipo":"normal"}]}
c1={"Nombre":"Geodude",
      "tipo":"Roca/Tierra",
      "pts de vida":40,
      "% de captura":0.60,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Placaje","daño":10,"tipo":"normal"},
                 {"nombre":"Lanzarrocas","daño":15,"tipo":"normal"}]}
c2={"Nombre":"Zubat",
      "tipo":"Veneno/Volador",
      "pts de vida":40,
      "% de captura":0.60,
      "cantidad disponible":4,
      "ataques":[{"nombre":"Absorber","daño":10,"tipo":"bicho"}
                 ,{"nombre":"Mordisco","daño":12,"tipo":"normal"}]}
c3={"Nombre":"Onix",
      "tipo":"Roca/Tierra",
      "pts de vida":35,
      "% de captura":0.30,
      "cantidad disponible":2,
      "ataques":[{"nombre":"Lanzarrocas","daño":15,"tipo":"roca"},
                 {"nombre":"atadura","daño":10,"tipo":"normal"}]}
pa1={"Nombre":"Poliwag",
      "tipo":"Agua",
      "pts de vida":40,
      "% de captura":0.60,
      "cantidad disponible":4,
      "ataques":[{"nombre":"Pistola agua","daño":12,"tipo":"agua"},
                 {"nombre":"Burbuja","daño":10,"tipo":"agua"}]} 
pa2={"Nombre":"Lotad",
      "tipo":"Agua/Planta",
      "pts de vida":40,
      "% de captura":0.65,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Absorber","daño":12,"tipo":"agua"},
                 {"nombre":"absorber","daño":10,"tipo":"planta"}]}
pa3={"Nombre":"Psyduck",
      "tipo":"Agua",
      "pts de vida":50,
      "% de captura":0.50,
      "cantidad disponible":3,
      "ataques":[{"nombre":"Arañazo","daño":12,"tipo":"agua"},
                 {"nombre":"Pistola Agua","daño":10,"tipo":"normal"}]}

zona_safari = {"bosque": {"pokemon":[b1,b2,b3]},
               "pradera": {"pokemon":[p1,p2,p3]},
               "cueva": {"pokemon":[c1,c2,c3]},
               "pantano":{"pokemon":[pa1,pa2,pa3]}}


#leyendas de descanso
historias_descanso={
    "bosque":[
        "has decidido descansar bajo un gran arbol del bosque despues de un largo dia de exploración",
        "mientras caminas por el bosque, te encuentras con un grupo de Caterpie descansando entre las hojas",
        "te detienes junto a un arbol para observar a unos Oddish que juegan entre la vegetacion"],
    "pradera":[
        "te has detenido a beber agua mientras admiras el hermoso paisaje de la pradera",
        "te sientas sobre la hierba mientras una suave brisa recorre la pradera",
        "mientras descansas, un grupo de pikachu aparecen corriendo entre las flores"],
    "cueva":["Entras a una cueva para descansar y descubres a varios Onix durmiendo profundamente"
             "te adentras en una cueva y encuentras ubas piedras brillantes iluminando el camino",
             "decidiste detenerte a descansar, pero escuchas un ruido misterioso proveniente del interior de la cueva"],
    "pantano":[
        "descansas a la orrilla del pantano mientras comes un sandwich y escuchas los sonidos del agua",
        "te sientas sobre una roca mientras observas a un grupo de Psyducks jugando en el agua",
        "mientras recoprres el pantano, ves unas burbujas salir del agua  decides acercarte a investigar"]}

equipo_jugador=[]
dht_device=adafruit_dht.DHT11(board.D4,use_pulseio=False)

def leer_clima():
    try:
        temperatura=dht_device.temperature
        humedad=dht_device.humidity
        if temperatura is not None and humedad is not None:
            return temperatura, humedad
    except RuntimeError as e:
        time.sleep(2)
    
    return 20.0, 50.0
#funcion elige el habitat segun los intervalos de temperatura y humedad actuales
def obtener_habitats_disponibles(temp,hum):
    disponibles=[]
    
    if temp<18:
        disponibles.append("cueva")
    if temp>=18:
        disponibles.append("pradera")
    if hum<65:
        disponibles.append("bosque")
    if hum>=65:
        disponibles.append("pantano")
    
    return list(set(disponibles))

temp, hum=leer_clima()

print(f"datos ambientales")

habitats_activos=obtener_habitats_disponibles(temp,hum)
print("\nhabitats habilitados para explorar hoy:")
for h in habitats_activos:
    print(f"-{h}")
    
def zafaris_activos(habitats_activos):
    print(" pokedex safaris activos")
    for zona in habitats_activos:
        if zona in zona_safari:
            print("habitat", zona)
            for pokemn in zona_safari[zona]["pokemon"]:
                print("datos pokemon")
                if pokemn["cantidad disponible"]>0:
                    print(f"{pokemn[Nombre]}, {pokemn['pts de vida']}, {pokemn['cantidad disponible']}")
   
   
   
#sonidos consola
buzzer=TonalBuzzer(18, mid_tone="A4",octaves=3)
#emite sonido al mover la palanca del joystick
def sonido_mover_palanca():
    buzzer.play(Tone("C6"))
    time.sleep(0.04)
    buzzer.stop()
#emite sonido al presionar el boton
   
def sonido_boton():
    for nota in (Tone("E5"),Tone("G5"),Tone("C6")):
        buzzer.play(nota)
        time.sleep(0.06)
    buzzer.stop()    
#sonidos consola

#emite sonido al mover la palanca del joystick

def sonido_comer():
    buzzer.play(Tone("C5"))
    time.sleep(0.1)
    buzzer.stop()
    
def sonido_exito_led():
    led_captura_r.on()
    led_captura_r.off()
    
    for nota in ["C5","E5","G5","C6"]:
        buzzer.play(Tone(nota))
        time.sleep(0.1)
    buzzer.stop()
    time.sleep(1)
    led_captura_v.off()
    
def sonido_captura_fallida():
    
    
    led_rojo.on()
    led_verde.off()
    buzzer.play(Tone("G3"))
    time.sleep(0.2)
    buzzer.play(Tone("C3"))
    time.sleep(0.3)
    buzzer.stop()
    time.sleep(1)
    led_rojo.off()
    
    

#indicador led pokemones disponibles
#enciende verde si hay pokemones disponibles
    #enciende rojo si no hay pokemones disponibles


led_rojo= LED(23)
led_verde= LED(27)
def pokeled(habitat):
    pokemones_zona=zona_safari[habitat]["pokemon"]
    poblacion_tot=0
    
    for pkmn in pokemones_zona:
        poblacion_tot=poblacion_tot+ pkmn["cantidad disponible"]
        
    if poblacion_tot>0:
        led_verde.on()
        led_rojo.off()
    else:
        led_verde.off()
        led_rojo.on()
        
    sleep(2)
    
        
#despliega la informacion de el pokemon seleccionado      


#configuraccion joystick
i2c= busio.I2C(board.SCL, board.SDA)
ads=ADS.ADS1115(i2c, gain=1, data_rate=128)
x= AnalogIn(ads, 1)
y=AnalogIn(ads, 0)
button= Button(17, pull_up=True, bounce_time=0.02)

def atrapar(habitat):
    print("[evento:atrapar]")
    pokemones_disponibles=[p for p in zona_safari[habitat]["pokemon"] if p["cantidad disponible"]>0]
    if not pokemones_disponibles:
        print("no quedan pokemones en este habitat")
        time.sleep(1)
        return
    pokemon=random.choice(pokemones_disponibles)
    prob_captura=pokemon["% de captura"]
    #sonido_evento("aparicion")
    print(f"un {pokemon['Nombre']} salvaje aparecio!")
    
    opciones=["lanzar poke ball","dar de comer","escapar"]
    j=0
    encuentro=True
    ultima_opcion=None
    while encuentro:
        x_value=x.value
        y_value=y.value
        btn=button.is_pressed
        if opciones[j]!=ultima_opcion:
            print(f"opcion actual: {opciones[j]}")
            ultima_opcion=opciones[j]
        
        if y_value>18000:
            #if
            j=(j+1)%len(opciones)
            print(f"opcion actual: {opciones[j]}")
            time.sleep(0.3)
        elif y_value<7000:
            j=(j-1)%len(opciones)
            print(f"opcion actual: {opciones[j]}")
            time.sleep(0.3)
        elif x_value>18000 or btn:
            time.sleep(0.3)
            
            if j==0:
                print("lanzaste una poke ball")
                if random.random()<=prob_captura:
                    #sonido_evento("exito")
                    led_verde.on()
                    led_rojo.off()
                    
                    pokemon["cantidad disponible"]-=1
                    print(f"atrapaste a {pokemon['Nombre']}")
                    
                    if len(equipo_jugador)<6:
                        equipo_jugador.append(pokemon)
                        print(f"agregado al equipo ({len(equipo_jugador)}/6")
                        
                        time.sleep(1.5)
                        led_verde.off()
                        encuentro=False
                    
                    else:
                        sonido_captura_fallida()
                        led_rojo.on()
                        led_verde.off()
                        print("el pokemon escapo de la poke ball")
                        time.sleep(1.5)
                        led_rojo.off()
                
                if random.random()<0.4:
                    print("el pokemon huyo")
                    sonido_captura_fallida()
                    encuentro=False
            elif j==1:
                sonido_comer()
                prob_captura=min(1.0, prob_captura + 0.15)
                porcentaje=int(prob_captura*100)
                print(f"diste de comer a {pokemon['Nombre']}! probabilidad de captura: {porcentaje}")
                time.sleep(0.5)
            
            elif j==2:
                     #sonido_evento("escape")
                print("escapaste")
                encuentro=False
                time.sleep(0.5)
            
            time.sleep(0.1)
            
def descanso(habitat):
    if habitat in historias_descanso:
        leyenda=random.choice(historias_descanso[habitat])
        
    print("[evento: descanso]")
    print(f" {leyenda}")
    
    time.sleep(3)
    
def nueva_aventura(habitat):
    evento=random.choice(["atrapar","descanso"])
    if evento=="descanso":
        descanso(habitat)
    else:
        atrapar(habitat)

    
def mover_en_habitats():
    contador=0
    
    while True:
        x_value=x.value
        y_value=y.value
        btn=button.is_pressed
        
        if y_value>18000:
            
            contador=(contador+1)%len(habitats_activos)
            sonido_mover_palanca()
            print(habitats_activos[contador])
            time.sleep(0.3)
            
        elif y_value<8000:
            
            contador=(contador-1)%len(habitats_activos)
            sonido_mover_palanca()
            print(habitats_activos[contador])
            time.sleep(0.3)
        elif x_value<8000:
            print("izquierda")
            time.sleep(0.3)
            
        elif x_value>18000 or btn:
            sonido_boton()
            habitat_seleccionado=habitats_activos[contador]
            print(f"entrando a {habitat_seleccionado}")
            time.sleep(0.5)
            nueva_aventura(habitat_seleccionado)
            time.sleep(0.3)
            
        elif btn:
            print("boton presionado")
            time.sleep(0.3)
        
            
        
        time.sleep(0.5)      
        
mover_en_habitats()  
def descanso(habitat):
    if habitat in historias_descanso:
        leyenda=random.choice(historias_descanso[habitat])
        
    print("[evento: descanso]")
    print(f" {leyenda}")
    
    time.sleep(3)
    
def nueva_aventura(habitat):
    evento=random.choice["atrapar","descanso"]
    if evento=="descanso":
        descanso(habitat)
    else:
        atrapar(habitat)

    