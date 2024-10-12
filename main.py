import copy
import time

import pygame
import math
import neat
import sys
import os
import pickle

WIDTH = 1300
HEIGHT = 800

global generation
generation = 0

# Auswahl der drei Strecken die im Programm geladen werden
with open('Parameter.txt', 'r') as file:
    parameter = [str(line.split('#')[0].strip()) for line in file]
track_name_1 = parameter[5]
track_name_2 = parameter[6]
track_name_3 = parameter[7]
track1 = "./tracks/" + str(track_name_1) + ".png"
track2 = "./tracks/" + str(track_name_2) + ".png"
track3 = "./tracks/" + str(track_name_3) + ".png"

# Klassendefinition
class Car:
    def __init__(self):
        # Die verschiedenen Sprites werden geladen
        self.sprite = pygame.image.load('auto.png')
        self.rotated_sprite = self.sprite

        # Autolänge und Autobreite definiert
        self.car_size_x = self.sprite.get_width()
        self.car_size_y = self.sprite.get_height()

        # Startwerte für jedes Auto
        self.angle = 0
        self.speed = 5  # Startgeschwindigkeit
        self.alive = True
        self.distance = 0
        self.time = 0
        self.time_alive = 0
        self.total_speed = 0
        self.update_count = 0
        self.sensor_endpoints = []

        # Startpostion/Winkel für jede Strecke einzeln definiert
        if track_load == "./tracks/gg Uhrzeigersinn.png":
            self.position = [650, 605]
        if track_load == "./tracks/Komplex.png":
            self.position = [650, 580]
        if track_load == "./tracks/Normal.png":
            self.position = [290, 680]
        if track_load == "./tracks/Rechteck.png":
            self.position = [630, 665]
        if track_load == "./tracks/Schmal.png":
            self.position = [650, 675]
        if track_load == "./tracks/Schwache Kurven.png":
            self.position = [595, 580]
        if track_load == "./tracks/Uhrzeigersinn.png":
            self.position = [650, 605]
            self.angle = 180



        if track_load == "./tracks/track1.png":
            self.position = [400, 615]
        if track_load == "./tracks/track2.png":
            self.position = [650, 580]
        if track_load == "./tracks/track2neu.png":
            self.position = [650, 580]
        if track_load == "./tracks/track3.png":
            self.position = [800, 600]
        if track_load == "./tracks/track_alles.png":
            self.position = [600, 590]
        if track_load == "./tracks/track_alles_2.png":
            self.position = [600, 590]
            self.angle = 180
        if track_load == "./tracks/track_links.png":
            self.position = [600, 150]
            self.angle = 180
        if track_load == "./tracks/track_rechts.png":
            self.position = [600, 150]
        if track_load == "./tracks/track3_2.png":
            self.position = [730, 580]
            self.angle = 180
        if track_load == "./tracks/track_wechsel.png":
            self.position = [750, 745]
            self.angle = 0
        if track_load == "./tracks/track_wechsel2.png":
            self.position = [750, 745]
            self.angle = 180
        if track_load == "./tracks/track_ferien.png":
            self.position = [900, 670]
            self.angle = 0
        if track_load == "./tracks/track_switch_1.png":
            self.position = [500, 580]


        # Berechnung des Mittelpunkts des Autos, damit die Drehung funktioniert
        self.center = [self.position[0] + self.car_size_x / 2, self.position[1] + self.car_size_y / 2]

    def draw(self, screen):
        # Auto zeichnen
        blit_position = [self.position[0] - self.rotated_sprite.get_width() / 2,
                         self.position[1] - self.rotated_sprite.get_height() / 2]
        screen.blit(self.rotated_sprite, blit_position)

        # Sensoren zeichnen
        #for endpoint in self.sensor_endpoints:
        #    pygame.draw.line(screen, (00, 139, 255), self.position, endpoint)

    # Funktion, die überprüft, ob das Auto die Wand berührt
    def crash_check(self, track):
        self.alive = True
        for corner in self.corners:
            x = int(corner[0])
            y = int(corner[1])
            if track.get_at((x, y)) == (0, 0, 0):  # Schaut für jede Ecke, ob sie die Farbe Schwarz berührt
                self.alive = False
                break

    # Funktion, welche die Sachen aktualisiert
    def update(self, track):

        if self.alive == False:  # Falls das Auto schon 'tot' ist → nicht mehr updaten
            return

        # Werte erhöhen
        self.distance = self.distance + self.speed
        self.time = self.time + 1
        self.total_speed += self.speed
        self.update_count += 1

        # Neue Position berechnen
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        # Neue Mitte berechnen
        self.center = self.center = [self.position[0], self.position[1]]

        # Koordinaten von den Ecken berechnen
        length = 0.5 * self.car_size_x
        width = 0.5 * self.car_size_y
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 45))) * length,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 45))) * width]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 135))) * length,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 135))) * width]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 225))) * length,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 225))) * width]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 315))) * length,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 315))) * width]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.crash_check(track)

    def turn(self, angle):
        # Falls Auto 'tot' → nicht mehr drehen
        if self.alive == False:
            return

        # Drehen des Sprites
        self.angle = self.angle + angle
        self.angle %= 360
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)

    def accelerate(self, amount):
        # Die Minimal- und Maximalgeschwindigkeit aus der Parameter-Datei holen
        with open('Parameter.txt', 'r') as file:
            parameter = [int(line.split('#')[0].strip()) for line in file.readlines()[:5]]
        min_speed = parameter[0]
        max_speed = parameter[1]

        self.speed += amount  # Erhöhung der Geschwindigkeit
        self.speed = max(min_speed, min(self.speed, max_speed))  # nicht Min- und Maxgeschwindigkeit überschreiten

    # Funktion, um Sensoren Werte zu berechnen
    def get_sensors_and_speed(self, track):
        input_data = []
        sensor_angles = [90, 45, 0, -45, -90]
        self.sensor_endpoints = []  # Damit die Endpunkte immer wieder zurückgesetzt werden

        # Für jeden der 5 Sensoren den Sensorenwert berechnen
        for angle in sensor_angles:
            sensor_length = 0
            x = int(self.position[0])
            y = int(self.position[1])
            while 0 <= x < WIDTH and 0 <= y < HEIGHT:
                x = int(self.position[0] + math.cos(math.radians(360 - (self.angle + angle))) * sensor_length)
                y = int(self.position[1] + math.sin(math.radians(360 - (self.angle + angle))) * sensor_length)
                if track.get_at((x, y)) == (0, 0, 0):
                    break
                sensor_length = sensor_length + 1

            input_data.append(sensor_length)
            self.sensor_endpoints.append((x, y))  # Die Koordinaten der Endpoints in die Liste speichern

        input_data.append(self.speed)  # Die Geschwindigkeit als sechsten Input anfügen
        return input_data  # Die Sensorwerte in einer Liste gespeichert zurückgeben

    def alive_check(self):  # Überprüft, ob das Auto noch am Fahren ist
        return self.alive

    def get_average_speed(self):  # Funktion, die die durchschnittliche Geschwindigkeit zurückgibt
        if self.update_count == 0:
            return 0
        return self.total_speed / self.update_count

    def fitness_reward(self):  # Funktion für die Fitness-Belohnung
        average_speed = self.get_average_speed()
        return (self.distance / 10) + (average_speed * 4)  # Definition des Fitnesswertes


# Simulationsschleife
def run_simulation(genomes, config):
    nets = []  # Liste für alle Netze
    cars = []  # Liste für alle Autos

    pygame.init()  # Initialisierung von Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    track = pygame.image.load(track_load)

    global generation
    generation += 1

    # Netze und Autos werden erstellt
    for i, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        cars.append(Car())

    clock = pygame.time.Clock()

    counter = 0

    # Werte für die Steuerung der Autos aus der Parameter-Datei holen
    with open('Parameter.txt', 'r') as file:
        parameter = [int(line.split('#')[0].strip()) for line in file.readlines()[:5]]
    acceleration = parameter[2]
    brake = parameter[3]
    left_steering = parameter[4]
    right_steering = -parameter[4]

    while True:

        # Um die Simulation zu schliessen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        for i, car in enumerate(cars):
            car.time_alive += 1

            output = nets[i].activate(car.get_sensors_and_speed(track))  # Output-Knoten werden berechnet
            choice = output.index(max(output))  # Es nimmt den Output mit dem höchsten Wert und führt diesen dann aus
            if choice == 0:
                car.accelerate(acceleration)  # Beschleunigung
            elif choice == 1:
                car.accelerate(brake)  # Bremsen
            elif choice == 2:
                car.turn(left_steering)  # nach links steuern
            else:
                car.turn(right_steering)  # nach rechts steuern

        still_alive = 0
        for i, car in enumerate(cars):
            if car.alive_check():
                still_alive += 1
                car.update(track)  # Updatefunktion für das Auto
                car.draw(screen)  # Zeichnungsfunktion für das Auto
                genomes[i][1].fitness = car.fitness_reward()  # Der Fitness-Wert wird erhöht


        #  Berechnungen für die durchschnittliche Distanz/Fitness
        sum_distance = 0
        sum_fitness = 0
        for car in cars:
            sum_fitness += car.fitness_reward()
            sum_distance += car.distance

        # Block, der die Generation stoppt, wenn sie zu lange dauert
        counter += 1
        if counter == 1500:
            print(sum_fitness/30)
            break

        # Block, der die Generation stoppt, wenn die Leertaste gedrückt wird
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print(sum_fitness/30)
            time.sleep(0.15)
            break

        # Printed die durchschnittliche Fitness nach jeder Generation
        if still_alive == 0:
            print(sum_fitness/30)
            break

        # Die Autos werden gezeichnet
        screen.blit(track, (0, 0))
        for car in cars:
            if car.alive_check() == True:
                car.draw(screen)

        #  Display Aktuelle Generation
        font = pygame.font.Font(None, 32)
        text_generation = font.render("Aktuelle Generation:     " + str(generation), True, (255, 255, 255))
        screen.blit(text_generation, (10, 769))

        # Knopf zum Abspeichern eines Genomes
        button_saveGenome = pygame.Rect(0, 720, 156, 40)
        pygame.draw.rect(screen, darkgreen, button_saveGenome)
        text_saveGenome = font.render("Abspeichern", True, (255, 255, 255))
        screen.blit(text_saveGenome, text_saveGenome.get_rect(center=button_saveGenome.center))

        # Überprüft, ob der Knopf angeklickt wird
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_saveGenome.collidepoint(event.pos):
                    best_genome = population.best_genome
                    with open('best_genome.pkl', 'wb') as f:
                        pickle.dump(best_genome, f)

        pygame.display.flip()
        clock.tick(60)  # Damit es nur 60 Mal pro Sekunde aktualisiert


# Replay-Funktion
def replay_genome(config_path, population_size=30):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    track = pygame.image.load(track_load)

    # Laden der Konfigurationsdatei
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Abgespeichertes Genom wird geladen
    genome_path = "best_genome.pkl"
    with open(genome_path, "rb") as f:
        saved_genome = pickle.load(f)

    # Neue Population erstellen
    new_population = neat.Population(config)
    new_population.population = {}
    for i in range(30):
        genome_id = i
        genome_copy = copy.deepcopy(saved_genome)
        genome_copy.key = genome_id
        new_population.population[genome_id] = genome_copy

    new_population.species.speciate(config, new_population.population, generation=0)
    new_population.run(run_simulation, 1000)  # Mit der neuen Population die Simulation starten

# Initialisierung des Programms
if __name__ == "__main__":
    pygame.init()  # Initialisierung von Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.Font(None, 32)
    darkgreen = (41, 56, 43)

    screen.fill((255, 255, 255))  # Weisser Hintergrund

    # Streckenauswahl-Text
    text_track = font.render("Streckenauswahl:", True, (41, 56, 43))
    screen.blit(text_track, (553, 200))

    # Track 1
    button_track1 = pygame.Rect(WIDTH / 2 - 350, 240, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_track1)
    text_track1 = font.render(track_name_1, True, (255, 255, 255))
    screen.blit(text_track1, text_track1.get_rect(center=button_track1.center))

    big_track1 = pygame.image.load(track1)
    image_track1 = pygame.transform.scale(big_track1, (200, 123.1))
    screen.blit(image_track1, (WIDTH / 2 - 350, 300))

    button_replay1 = pygame.Rect(WIDTH / 2 - 350, 435, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_replay1)
    text_replay1 = font.render("Genom laden", True, (255, 255, 255))
    screen.blit(text_replay1, text_replay1.get_rect(center=button_replay1.center))

    #  Track 2
    button_track2 = pygame.Rect(WIDTH / 2 - 100, 240, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_track2)
    text_track2 = font.render(track_name_2, True, (255, 255, 255))
    screen.blit(text_track2, text_track2.get_rect(center=button_track2.center))

    big_track1 = pygame.image.load(track2)
    image_track1 = pygame.transform.scale(big_track1, (200, 123.1))
    screen.blit(image_track1, (WIDTH / 2 - 100, 300))

    button_replay2 = pygame.Rect(WIDTH / 2 - 100, 435, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_replay2)
    text_replay2 = font.render("Genom laden", True, (255, 255, 255))
    screen.blit(text_replay2, text_replay2.get_rect(center=button_replay2.center))

    #  Track 3
    button_track3 = pygame.Rect(WIDTH / 2 + 150, 240, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_track3)
    text_track3 = font.render(track_name_3, True, (255, 255, 255))
    screen.blit(text_track3, text_track3.get_rect(center=button_track3.center))

    big_track1 = pygame.image.load(track3)
    image_track1 = pygame.transform.scale(big_track1, (200, 123.1))
    screen.blit(image_track1, (WIDTH / 2 + 150, 300))

    button_replay3 = pygame.Rect(WIDTH / 2 + 150, 435, 200, 50)
    pygame.draw.rect(screen, darkgreen, button_replay3)
    text_replay3 = font.render("Genom laden", True, (255, 255, 255))
    screen.blit(text_replay3, text_replay3.get_rect(center=button_replay3.center))

    running = True
    while running == True:

        # Config wird geladen und NEAT übergeben
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config_path)
        population = neat.Population(config)  # Erstellen einer Population
        #population.add_reporter(neat.StdOutReporter(True))  # Dieser Reporter printed hilfreiche Sachen

        # Pygame-Events überprüfen
        for event in pygame.event.get():

            # Um die Simulation zu schliessen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Überprüft, ob die Knöpfe angeklickt wurden und startet demnach die Simulation mit der richtigen Strecke
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_track1.collidepoint(event.pos):
                    track_load = track1
                    population.run(run_simulation, 1000)
                if button_track2.collidepoint(event.pos):
                    track_load = track2
                    population.run(run_simulation, 1000)
                if button_track3.collidepoint(event.pos):
                    track_load = track3
                    population.run(run_simulation, 1000)
                if button_replay1.collidepoint(event.pos):
                    track_load = track1
                    replay_genome(config_path)
                if button_replay2.collidepoint(event.pos):
                    track_load = track2
                    replay_genome(config_path)
                if button_replay3.collidepoint(event.pos):
                    track_load = track3
                    replay_genome(config_path)

        pygame.display.flip()