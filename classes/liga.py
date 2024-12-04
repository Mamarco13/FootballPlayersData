class Liga:
    def __init__(self, id, nombre, equipos=None):
        self.id = id
        self.nombre = nombre
        self.equipos = equipos or []

    def agregar_equipo(self, equipo):
        """Añadir un equipo a la liga."""
        self.equipos.append(equipo)

    def obtener_todos_los_jugadores(self):
        """Obtener todos los jugadores de la liga."""
        jugadores = []
        for equipo in self.equipos:
            jugadores.extend(equipo.obtener_jugadores())
        return jugadores
        
    # Getter para el id
    def get_id(self):
        return self.id

    # Getter para el nombre
    def get_nombre(self):
        return self.nombre

    # Getter para los equipos
    def get_equipos(self):
        return self.equipos

    def __str__(self):
        return f"Liga {self.nombre}, con {len(self.equipos)} equipos"
