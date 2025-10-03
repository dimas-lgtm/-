class Location:
    def __init__(self, latitude, longitude, address, description=""):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.description = description
        self.id = None

    def __str__(self):
        return f"Location(id={self.id}, address={self.address})"

    def get_coordinates(self):
        """Получить координаты в виде кортежа"""
        return (self.latitude, self.longitude)

    def set_coordinates(self, latitude, longitude):
        """Установить новые координаты"""
        self.latitude = latitude
        self.longitude = longitude

    def update_address(self, new_address, new_description=""):
        """Обновить адрес и описание"""
        self.address = new_address
        if new_description:
            self.description = new_description

    def to_dict(self):
        """Преобразовать в словарь для JSON"""
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """Создать объект из словаря"""
        return cls(
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            address=data.get('address', ''),
            description=data.get('description', '')
        )