class Equipo:
    def __init__(self, id, nombre, jugadores=None, liga = None):
        self.id = id
        self.nombre = nombre
        self.jugadores = jugadores or []
        self.liga = liga

    def set_liga(self, liga):
        self.liga = liga

    # Getter para id
    def get_id(self):
        """Devuelve el ID del equipo."""
        return self.id

    # Getter para nombre
    def get_nombre(self):
        """Devuelve el nombre del equipo."""
        return self.nombre
    
    # Getter para jugadores
    def get_jugadores(self):
        """Devuelve la lista de jugadores."""
        return self.jugadores

    def agregar_jugador(self, jugador):
        """Añadir un jugador al equipo."""
        self.jugadores.append(jugador)

    def obtener_jugadores(self):
        """Devolver la lista de jugadores."""
        return self.jugadores

    def __str__(self):
        return f"{self.nombre}"
